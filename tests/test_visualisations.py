from soilgrids import SoilGrids
import pandas as pd
import plotly.graph_objects as go

# These tests don't verify rendering of plots - this is outside of the
# scope of this package. Insted, they check the structure of the 
# (plotly.graph_objects.Plot) outputs to see if they contain the expected 
# data.

def test_plot_ocs_property_relationships():
    sg = SoilGrids()
    sg._data = pd.DataFrame({
        'lat': {0: 8.663411, 1: 8.663411, 3: 8.663411, 10: 8.680699, 11: 8.680699, 13: 8.680699}, 
        'lon': {0: 56.323929, 1: 56.323929, 3: 56.323929, 10: 56.441106, 11: 56.441106, 13: 56.441106}, 
        'soil_property': {0: 'clay', 1: 'sand', 3: 'ocs', 10: 'clay', 11: 'clay', 13: 'ocs'}, 
        'd_factor': {0: 10, 1: 10, 3: 10, 10: 10, 11: 10, 13: 10}, 
        'mapped_units': {0: 'g/kg', 1: 'g/kg', 3: 't/ha', 10: 'g/kg', 11: 'g/kg', 13: 't/ha'}, 
        'target_units': {0: '%', 1: '%', 3: 'kg/m²', 10: '%', 11: '%', 13: 'kg/m²'}, 
        'uncertainty_unit': {0: '', 1: '', 3: '', 10: '', 11: '', 13: ''}, 
        'depth': {0: '0-5cm', 1: '5-15cm', 3: '0-30cm', 10: '0-5cm', 11: '5-15cm', 13: '0-30cm'}, 
        'top_depth': {0: 0, 1: 5, 3: 0, 10: 0, 11: 5, 13: 0}, 
        'bottom_depth': {0: 5, 1: 15, 3: 30, 10: 5, 11: 15, 13: 30}, 
        'unit_depth': {0: 'cm', 1: 'cm', 3: 'cm', 10: 'cm', 11: 'cm', 13: 'cm'}, 
        'mean': {0: 63.0, 1: 64.0, 3: 60.0, 10: 128.0, 11: 124.0, 13: 55.0}
    })

    fig = sg.plot_ocs_property_relationships()

    assert type(fig) == go.Figure, 'Plot should be an instance of plotly.graph_objects.Figure'

    assert {'xaxis', 'xaxis2'} < fig.to_dict()['layout'].keys(), \
        'Plot should have multiple x-axes'
        
    assert {'clay (g/kg)', 'sand (g/kg)'} <= {x['name'] for x in fig.to_dict()['data']}, \
        "Panels should have titles 'clay (g/kg)' and 'sand (g/kg)'"
        
    axis_titles = set()
    fig.for_each_xaxis(lambda x: axis_titles.add(x.title.text))
    assert axis_titles == {'Mean Clay (g/kg)', 'Mean Sand (g/kg)'}, \
        "Axis title should be {'Mean Clay (g/kg)', 'Mean Sand (g/kg)'}"
    
        

def test_plot_property_map():
    sg = SoilGrids()
    sg._data = pd.DataFrame({
        'lat': {0: 8.0, 1: 8.1, 3: 8.0, 10: 8.3, 11: 8.4, 13: 9.0}, 
        'lon': {0: 56.0, 1: 56.2, 3: 56.0, 10: 56.3, 11: 56.4, 13: 57.0}, 
        'soil_property': {0: 'clay', 1: 'sand', 3: 'ocs', 10: 'clay', 11: 'clay', 13: 'ocs'}, 
        'd_factor': {0: 10, 1: 10, 3: 10, 10: 10, 11: 10, 13: 10}, 
        'mapped_units': {0: 'g/kg', 1: 'g/kg', 3: 't/ha', 10: 'g/kg', 11: 'g/kg', 13: 't/ha'}, 
        'target_units': {0: '%', 1: '%', 3: 'kg/m²', 10: '%', 11: '%', 13: 'kg/m²'}, 
        'uncertainty_unit': {0: '', 1: '', 3: '', 10: '', 11: '', 13: ''}, 
        'depth': {0: '0-5cm', 1: '5-15cm', 3: '0-30cm', 10: '0-5cm', 11: '5-15cm', 13: '0-30cm'}, 
        'top_depth': {0: 0, 1: 5, 3: 0, 10: 0, 11: 5, 13: 0}, 
        'bottom_depth': {0: 5, 1: 15, 3: 30, 10: 5, 11: 15, 13: 30}, 
        'unit_depth': {0: 'cm', 1: 'cm', 3: 'cm', 10: 'cm', 11: 'cm', 13: 'cm'}, 
        'mean': {0: 63.0, 1: 64.0, 3: 60.0, 10: 128.0, 11: 124.0, 13: 55.0}
    })

    fig = sg.plot_property_map('ocs')

    assert type(fig) == go.Figure, 'Plot should be an instance of plotly.graph_objects.Figure'

    bounds = {name: round(val, 1) for name, val in fig.to_dict()['layout']['mapbox']['bounds'].items()}
    assert bounds == {'east': 59.0, 'north': 11.0, 'south': 6.0, 'west': 54.0}, \
        "Map bounds should be {'east': 59.0, 'north': 11.0, 'south': 6.0, 'west': 54.0}"
        
    hovertext = fig.to_dict()['data'][0]['hovertext'][0]
    assert hovertext == '<b>ocs: 60.0t/ha</b><br><i>clay: 63.0g/kg</i>', \
        "Plot hovertext should be '<b>ocs: 60.0t/ha</b><br><i>clay: 63.0g/kg</i>'" 