from .api_requests import get_soilgrids
from ._utils import _rscript, _logger

from typing import Union
import numpy as np
import pandas as pd
import seaborn.objects as so


class SoilGrids:
    """Read and perform basic analysis of Soilgrids data.
    
    Provides a convenient interface to the Soilgrids API, and some basic data
    wrangling and analysis methods.
    
    Attributes:
        `data` (`pandas.DataFrame`): The data returned by the last call to 
            `get_points()` or `get_points_sample()`. Note that this generates
            a `ValueError` if called before either of these methods.
        `get_points()` (method): Query Soilgrids for soil properties at 
            specified locations.
        `get_points_sample()` (method): Query Soilgrids for soil properties at
            randomly sampled locations.
        `main_properties()` (method): Determine the most prevalent property (out 
            of sand, silt, and clay) for each location.
        `ocs_correlation()` (method): Determine the correlation between sand, 
            silt, clay, and OCS (organic carbon stock).
        `aggregate_means()` (method): Aggregate the means of soil properties 
            across depths.
    """
    
    def __init__(self):
        self._data = None
    
    @property
    def data(self):
        """Data returned by the last call to `get_points()` or `get_points_sample()`.

        Raises:
            `ValueError`: If no data has been returned yet.

        Returns:
            `pandas.DataFrame`: A data frame of the form returned by 
            `get_soilgrids()`.
        """
        if self._data is None:
            raise ValueError(
                'No data. Call `get_points()` or `get_points_sample()` first.'
            )
        return self._data
    
    def get_points(self,
                   lat: float | list[float], 
                   lon: float | list[float], 
                   *, 
                   soil_property: Union[str, list[str], None] = None, 
                   depth: Union[str, list[str], None] = None, 
                   value: Union[str, list[str], None] = None) -> pd.DataFrame:
        """Query Soilgrids for soil properties at specified locations.
    
        This method is a wrapper for the Soilgrids API. The returned geojson is
        parsed into a pandas DataFrame, with a row for each combination of 
        `lat`, `lon`, `soil_property`, and `depth`, and a column for each `value`.
        After running this method, the returned data can be obtained using the
        `data` property.
        
        More detailed information about the data returned can be obtained from
        [IRSIC](https://www.isric.org/explore/soilgrids/faq-soilgrids).
        
        Note that ISRIC's [fair use policy](https://rest.isric.org) requests 
        that at most 5 requests are made per minute, and this method throttles 
        requests to this rate in cases when multiple values for `lat` and `lon` 
        are provided.
        
        Args:
            `lat`: The latitude(s) of the point(s) to query. Must be in the range 
                [-90, 90].
            `lon`: The longitude(s) of the point(s) to query. Must be in the 
                range [-180, 180]. Note that NumPy-style broadcasting is 
                applied to lat and lon, so that if one is a scalar and the other 
                is an array, all combinations of the two are queried. Note that 
                coordinates are rounded to 6 decimal places before querying - 
                roughly the precision needed to identify an 
                [individual human](https://en.wikipedia.org/wiki/Decimal_degrees#Precision).
            `soil_property`: The soil property/properties to query. Must be a 
                subset of the following or `None`, in which case all properties 
                are returned:
                ```python
                ['bdod', 'cec', 'cfvo', 'clay', 'nitrogen', 'ocd', 'ocs', 
                 'phh2o', 'sand', 'silt', 'soc', 'wv0010', 'wv0033', 'wv1500'] 
                ```
            `depth`: The soild depth(s) to query. Must be a subset of the 
                following or `None`, in which case all depths are returned:
                ```python
                ['0-5cm', '0-30cm', '5-15cm', '15-30cm', '30-60cm', '60-100cm', 
                 '100-200cm'] 
                ```
                Note that there is some overlap between the allowed values, since 
                some properties are measured at a more granular level than others.
            `value`: The value(s) to query. Must be a subset of the following or 
                `None`, in which case all values are returned:
                ```python
                ['Q0.5', 'Q0.05', 'Q0.95', 'mean', 'uncertainty']
                ```

        Returns:
            `pd.DataFrame`: A data frame with a row for each combination of 
                `lat`, `lon`, `soil_property`, and `depth`, and a column for 
                each `value`. 
        """
        self._data = get_soilgrids(
            lat, lon, 
            soil_property=soil_property, depth=depth, value=value
        )
        
    
    def get_points_sample(self, 
                          n: int =5, 
                          *, 
                          lat_a: float =-90, 
                          lon_a: float =-180, 
                          lat_b: float =90, 
                          lon_b: float =180,
                          soil_property: Union[str, list[str], None] = None, 
                          depth: Union[str, list[str], None] = None, 
                          value: Union[str, list[str], None] = None) -> pd.DataFrame:
        """Query Soilgrids for a random set of coordinates.
        
        This method is a wrapper for the Soilgrids API. The returned geojson 
        is parsed into a pandas DataFrame, with a row for each combination of 
        `lat`, `lon`, `soil_property`, and `depth`, and a column for each 
        `value`. After running this method, the returned data can be obtained 
        using the `data` property. The points returned by this method are
        uniformly distributed throughout the specified range.
        
        More detailed information about the data returned can be obtained from
        [ISRIC](https://www.isric.org/explore/soilgrids/faq-soilgrids).
        
        Note that ISRIC's [fair use policy](https://rest.isric.org) requests 
        that at most 5 requests are made per minute, and this method throttles 
        requests to this rate in cases when multiple values for `lat` and `lon` 
        are provided.
        
        Args:
            `n`: The number of points to query.
            `lat_a`: The first bounding latitude. Must be in the range [-90, 90]
            `lon_a`: The first bounding longitude. Must be in the range [-180, 180]
            `lat_b`: The second bounding longitude. Must be in the range [-90, 90]
            `lon_b`: The second bounding longitude. Must be in the range [-180, 180]
            `soil_property`: The soil property/properties to query. Must be a 
                subset of the following or `None`, in which case all properties 
                are returned:
                ```python
                ['bdod', 'cec', 'cfvo', 'clay', 'nitrogen', 'ocd', 'ocs', 
                 'phh2o', 'sand', 'silt', 'soc', 'wv0010', 'wv0033', 'wv1500'] 
                ```
            `depth`: The soild depth(s) to query. Must be a subset of the 
                following or `None`, in which case all depths are returned:
                ```python
                ['0-5cm', '0-30cm', '5-15cm', '15-30cm', '30-60cm', '60-100cm', 
                 '100-200cm'] 
                ```
                Note that there is some overlap between the allowed values, 
                since some properties are measured at a more granular level than 
                others.
            `value`: The value(s) to query. Must be a subset of the following or 
                `None`, in which case all values are returned:
                ```python
                ['Q0.5', 'Q0.05', 'Q0.95', 'mean', 'uncertainty']
                ```

        Returns:
            `pd.DataFrame`: A data frame with a row for each combination of 
                `lat`, `lon`, `soil_property`, and `depth`, and a column for 
                each `value`. 
        """
        
        # Uncomment during testing to avoid waiting ages for data to load
        # self._data = pd.read_csv("tests/data/soilgrids-results.csv")
        # return 
        
        lat_min, lat_max = min(lat_a, lat_b), max(lat_a, lat_b)
        lon_min, lon_max = min(lon_a, lon_b), max(lon_a, lon_b)
        
        self._data = get_soilgrids(
            lat_min + (lat_max - lat_min) * np.random.random_sample(n),
            lon_min + (lon_max - lon_min) * np.random.random_sample(n),
            soil_property=soil_property, depth=depth, value=value
        )
        
    
    def main_properties(self):
        """Get the most prevalent soil property (sand, silt, or clay) for each location.
        
        This is a utility method for quickly determining the most prevalent soil
        type for each location.
        
        Note that for this method to work, the column `mean` must be present in
        the data. This can be achieved by calling `get_points()` or 
        `get_points_sample()` with `value='mean'`.
        
        Returns:
            `pandas.DataFrame`: A data frame with columns `lat`, `lon` and 
            `soil_property`, where `soil_property` gives the most prevelant 
            property for the location.
        """
        return self.aggregate_means() \
            .query("soil_property in ['sand', 'silt', 'clay']") \
            .sort_values(
                ['lat', 'lon', 'mapped_units', 'unit_depth', 'mean'], 
                ascending=False
            ) \
            .groupby(
                ['lat', 'lon', 'mapped_units', 'unit_depth'], 
                as_index=False
            ) \
            .apply(lambda g: g.iloc[0]) \
            .filter(['lat', 'lon', 'soil_property'])
            
    
    def ocs_correlation(self, capture_output: bool=False) -> None | str:
        """Get the correlation between sand, silt, clay, and OCS (organic carbon stock).
        
        This method requires R to be installed and available on the PATH in 
        order to run.
         
        1. First, the data is aggregated to get overall means for sand, silt,
           clay for the 0-30cm layer. Soilgrids provides OCS data for the 0-30cm 
           layer as a single value, so this step is necessary to make the 
           values comparable.
      
        2. The aggregated data is pivoted into wide format similar to the 
           following:
            ```
                     lat      lon    sand    silt    clay    ocs
              0  55.9581   8.6622     0.1     0.2     0.7     10
              1  55.9581   8.6622     0.2     0.3     0.5     20
            ...      ...      ...     ...     ...     ...    ...
            ```
            
        3. A linear regression model is then fitted, with OCS as the response 
           variable and sand, silt, and clay as predictors.
 
        4. Summary statistics for the model are returned.
        
        Steps 3 and 4 are performed using R. 
        
        Args:
            `capture_output` (`bool`): If `False` (the default), the model 
                summary is printed to the console. If `True`, the model summary
                is returned as a string.
        
        Returns:
            `None`: The model summary is printed to the console.
        """
        pivoted_data = self.aggregate_means(0, 30) \
            .query("soil_property in ['sand', 'silt', 'clay', 'ocs']") \
            .pivot_table(
                index=['lat', 'lon'],
                columns='soil_property',
                values='mean'
            ) \
            .reset_index()
        
        assert len(pivoted_data) >= 20, \
            "At least 20 distinct values for `lat` and `lon` are needed to fit a linear model."
        
        # Fill missing properties with zeros 
        pivoted_data = pivoted_data.reindex(
            pivoted_data.columns.union(['sand', 'silt', 'clay', 'ocs'], sort=False), 
            axis=1
        )
        
        model_summary = _rscript(
            'r-scripts/linear-regression.R', 
            pivoted_data.to_csv(index=False)
        )
        
        if capture_output:
            return model_summary
        
        _logger.info(model_summary)
   
    def plot_ocs_property_relationships(self, 
                                        top_depth: int=0, 
                                        bottom_depth: int=30) -> so.Plot:
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
            `top_depth` (`float`): The minimum top depth to include in the 
                aggregated results. Note that the value returned in the output 
                may be higher. Defaults to 0.
            `bottom_depth` (`float`): The maximum bottom depth to include in the
                aggregated results. Note that the value returned in the output
                may be lower. Defaults to 30.
                
        Returns:
            `seaborn.objects.Plot`: An object representing the plot. Use the
            `show()` method to display this graphically in an interactive
            context.
        """
        
        data = self.aggregate_means(top_depth, bottom_depth) 
         
        soil_types_data = data \
            .query("soil_property != 'ocs'")
        
        ocs_data = data \
            .query("soil_property == 'ocs'") \
            .filter(['lat', 'lon', 'mean']) \
            .rename(columns={'mean': 'mean_ocs'})
         
        plot_data = soil_types_data \
            .merge(ocs_data, on=['lat', 'lon'], how = 'outer') \
            .reset_index()
        
        plot = so.Plot(plot_data, x="mean", y='mean_ocs') \
            .add(so.Dots()) \
            .add(so.Line(), so.PolyFit(1)) \
            .facet('soil_property') \
            .share(x=False) \
            .label(
                title="Mean {}".format,
                x="",
                y="Mean OCS",
                color="",
            )
        
        return plot
        
    def aggregate_means(self, top_depth: int=0, bottom_depth:int=30, skipna=False) -> pd.DataFrame:
        """Aggregate the means of soil properties across depths.
        
        Soilgrids provides for different properties at different levels of
        granularity. For example, for the 0-30cm, 3 measurements for sand are
        given, one for each of the 0-5cm, 5-15cm, and 15-30cm layers. On the
        other hand, for OCS, a single value is given for the whole 0-30cm.
        
        Before comparing sand (or clay, or silt) with OCS, it is thus necessary
        to aggregate them up to the same level of granularity.
        
        Aggregating means is done by weighting each value according to the 
        thickness of the layer it represents, before summing the weighted 
        values.
        
        Once this has been done, it is possible to compare sand, silt, and clay
        with OCS.
        
        Args:
            `top_depth` (`float`): The minimum top depth to include in the 
                aggregated results. Note that the value returned in the output 
                may be higher. Defaults to 0.
            `bottom_depth` (`float`): The maximum bottom depth to include in the
                aggregated results. Note that the value returned in the output
                may be lower. Defaults to 30.
            `skipna` (`bool`): Whether to propagate missing values when 
                aggregating. This is set to `False` by default, since the 
                alternative can quietly give misleading results.

        Returns:
            `pandas.DataFrame`: A DataFrame with columns `lat`, `lon`, 
            `mapped_units`, `unit_depth`, `soil_property`, `top_depth`, 
            `bottom_depth`, and `mean`.
        """
        assert 'mean' in self.data.keys(), \
            'No `mean` column. Call `get_points()` or `get_points_sample()`' \
            " with `value='mean'` first."
        
        data = self.data
        data = data[
            (top_depth <= data['top_depth']) & 
            (data['bottom_depth'] <= bottom_depth)
        ]
        
        return data \
            .groupby(
                # ~~ What's happening here? ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # Say we have the following values:
                #
                #    soil_property     depth   mean
                #             sand    0- 5cm      1
                #             sand    5-15cm      2
                #             sand   15-30cm      3
                #
                # To get the mean for sand across the whole 0-30cm, we can't 
                # just do mean([1, 2, 3]), because this would skew the result 
                # towards the thinner layers. Instead, we first have to weight 
                # each value according to the thickness of the layer it 
                # represents:
                #
                #   * Row 1 applies to 5cm of the 0-30cm layer
                #   * Row 2 applies to 10cm of the 0-30cm layer
                #   * Row 3 applies to 15cm of the 0-30cm layer
                # 
                # So we need to weight row 1 by 5/30, row 2 by 10/30, and row 3
                # by 15/30. Once we've done that, the mean across the whole
                # 0-30cm layer can be found by summing the weighted values:
                #   
                #   mean_overall = sum([1 * 5/30, 2 * 10/30, 3 * 15/30]) = 2.333
                #
                # (NB, rounding is because it doesn't make sense to give more 
                # precision than the original data.)
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                ['lat', 'lon', 'mapped_units', 'unit_depth', 'soil_property'], 
                as_index=False
            ) \
            .apply(lambda x: x.assign(
                thickness = lambda x: x['bottom_depth'] - x['top_depth'],
                mean = lambda x: (x['mean'] * x['thickness'] / x['thickness'].sum()) #\
                   # .round() \
                   # .astype(np.float)
            )) \
            .groupby(
                ['lat', 'lon', 'mapped_units', 'unit_depth', 'soil_property'], 
                as_index=False
            ) \
            .agg({
                'top_depth': 'min',
                'bottom_depth': 'max',
                'mean': lambda m: m.sum(skipna = skipna)
            })

