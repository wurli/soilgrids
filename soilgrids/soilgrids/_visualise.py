from .._utils import _rescale

import numpy as np
import plotly.express as px
import plotly.graph_objects as go


def plot_ocs_property_relationships(self, 
                                    top_depth: int | None=None, 
                                    bottom_depth: int | None=None) -> go.Figure:
    """Plot the relationships between OCS and other soil properties.
    
    Produces a plot with multiple panels, where each panel
    shows a scatterplot with an overlayed line of best fit, i.e. a modelled
    linear regression. Different panels are shown for each soil property
    besides OCS which is present in the data. The mean OCS is shows on the
    y-axis, and the other property is shown on the x-axis.
    
    Before plotting, the data is aggregated so that a single value is given
    for each point (i.e. combination of latitude and longitude). The values
    included in the aggregated data can be controlled using `top_depth` and
    `bottom_depth`.
    
    Args:
        `top_depth` (`float | None`): The minimum top depth to include in the 
            aggregated results. Note that the value returned in the output 
            may be higher. Defaults to `None`, in which case all 
            values are incuded. 
        `bottom_depth` (`float | None`): The maximum bottom depth to include 
            in the aggregated results. Note that the value returned in the 
            output may be lower. Defaults to `None`, in which case all 
            values are incuded.
            
    Returns:
        `plotly.graph_objects.Plot`: An object representing the plot. Use 
        the `show()` method to display this graphically in an interactive
        context.
    """
    data = self.aggregate_means(top_depth, bottom_depth) 
        
    soil_types_data = data \
        .query("soil_property != 'ocs'") \
        .reset_index()

    ocs_data = data \
        .query("soil_property == 'ocs'") \
        .rename(columns={'mean': 'mean_ocs'}) \
        .reset_index()
        
    plot_data = soil_types_data \
        .merge(
            ocs_data.filter(['lat', 'lon', 'mean_ocs']), 
            on=['lat', 'lon'], 
            how = 'left'
        ) \
        .assign(soil_property=lambda x: 
            x['soil_property'] + ' (' + x['mapped_units'] + ')'
        ) \
        .reset_index()

    plot = px.scatter(
        plot_data,
        x='mean', y='mean_ocs', 
        facet_col='soil_property', 
        trendline='ols', 
        color='soil_property'
    )
    
    # Slight hack to set axis titles using panel titles - no easy way to do this. Yuck!
    panel_titles = []
    plot.for_each_annotation(lambda p: panel_titles.append(p.text))
    axis_titles = ['Mean ' + x.split('=')[-2].capitalize() for x in reversed(panel_titles)]
    plot = plot.for_each_xaxis(lambda x: x.update(title={'text': axis_titles.pop()}))
        
    plot = plot \
        .update_xaxes(matches=None) \
        .for_each_annotation(lambda p: p.update(text='')) \
        .update_traces(showlegend=False) \
        .update_layout(
            title='Organic Carbon Stock vs Other Properties',
            yaxis_title='Organic Carbon Stock ({})'.format(
                ocs_data['mapped_units'][0]
            )
        ) 
        
    return plot


def plot_property_map(self, 
                        soil_property: str, 
                        top_depth: int | None=None,
                        bottom_depth: int | None=None,
                        zoom: int=2) -> go.Figure:
    """Plot points on a map.
    
    Produces a plot of points on a map, sized according to the 
    `soil_property` selected, with other properties viewable through the
    plot tooltip when viewing in an interactive context.
    
    Before plotting, the data is aggregated to get representative figures
    for soil between `top_depth` and `bottom_depth`. Note that any points
    which have missing values for the selected property will be silently
    dropped.

    Args:
        `soil_property` (`str`): The property to use to scale the plotted
            points. This should correspond to one of the values for
            `soil_property` selected in the last call to `get_points()`
            or `get_points_sample()`.
        `top_depth` (`float | None`): The minimum top depth to include in the 
            aggregated results. Note that the value returned in the output 
            may be higher. Defaults to `None`, in which case all 
            values are incuded. 
        `bottom_depth` (`float | None`): The maximum bottom depth to include 
            in the aggregated results. Note that the value returned in the 
            output may be lower. Defaults to `None`, in which case all 
            values are incuded.
        `zoom` (`int`): _description_. The initial zoom level for the 
            output. Can be set to a higher value to get a more zoomed-in
            map.

    Returns:
        `plotly.graph_objects.Plot`: An object representing the plot. Use 
        the `show()` method to display this graphically in an interactive
        context.
    """
    agg = self.aggregate_means(top_depth, bottom_depth).dropna(subset='mean')

    property_data = agg \
        .query(f"soil_property == '{soil_property}'") \
        .reset_index()
    
    label_order = [soil_property] + sorted(list(set(agg['soil_property'])))

    label_data = agg \
        .sort_values('soil_property', key=lambda col: col.apply(label_order.index)) \
        .assign(
            label=lambda x: 
                x['soil_property'] + 
                ': ' + 
                x['mean'].astype(str) + 
                x['mapped_units']
        ) \
        .assign(
            label=lambda x: np.where(
                x['soil_property'] == soil_property, 
                '<b>' + x['label'] + '</b>', 
                '<i>' + x['label'] + '</i>'
            )
        ) \
        .groupby(['lat', 'lon']) \
        .agg(dict(label=lambda x: '<br>'.join(x)))
        
    plot_data = property_data.merge(label_data, how='left', on=['lat', 'lon'])

    trace = go.Scattermapbox(
        lat=plot_data['lat'],
        lon=plot_data['lon'],
        mode='markers',
        marker=dict(size=_rescale(plot_data['mean'], 10, 20), color='red', opacity=0.5),
        text=plot_data['soil_property'], 
        hovertext=plot_data['label']
    )
    
    latmin, latmax = plot_data['lat'].min(), plot_data['lat'].max()
    lonmin, lonmax = plot_data['lon'].min(), plot_data['lon'].max()
    window_expansion = 2
    
    title = '<br>'.join([
        '<b>Mean Soil {prop} at {depth_min}-{depth_max}{unit}</b>'.format(
            prop='Organic Carbon Stock' if soil_property == 'ocs' else soil_property.captilize(),
            depth_min=agg['top_depth'].min(), 
            depth_max=agg['bottom_depth'].max(), 
            unit=agg['unit_depth'][0]
        ),
        'Showing points between ({}, {}) and ({}, {})'.format(
            latmin, lonmin, latmax, lonmax,
        ),
        'Range for the region ({unit}): [{prop_min}, {prop_max}]'.format(
            unit=property_data['mapped_units'][0],
            prop_min=int(property_data['mean'].min()), 
            prop_max=int(property_data['mean'].max())
        )
    ])
    
    layout = go.Layout(
        title=title,
        mapbox=dict(
            style='carto-positron',
            zoom=zoom,
            center=dict(
                lat=(latmax + latmin) / 2,
                lon=(lonmax + lonmin) / 2
            ),
            bounds=dict(
                north=latmax + (latmax - latmin) * window_expansion, 
                east =lonmax + (lonmax - lonmin) * window_expansion, 
                south=latmin - (latmax - latmin) * window_expansion, 
                west =lonmin - (lonmax - lonmin) * window_expansion 
            )
        )
    )
    
    return go.Figure(data=[trace], layout=layout)


