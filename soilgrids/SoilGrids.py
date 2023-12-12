from .get_soilgrids import get_soilgrids
from ._utils import rscript, logger

from typing import Union
import numpy as np
import pandas as pd


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
        `ocs_correlations()` (method): Determine the correlation between sand, 
            silt, clay, and OCS (organic carbon stock).
        `aggregate_means()` (method): Aggregate the means of soil properties 
            across depths.
    """
    
    def __init__(self):
        self.__data = None
    
    @property
    def data(self):
        """Data returned by the last call to `get_points()` or `get_points_sample()`.

        Raises:
            `ValueError`: If no data has been returned yet.

        Returns:
            `pandas.DataFrame`: A data frame of the form returned by 
            `get_soilgrids()`.
        """
        if self.__data is None:
            raise ValueError(
                'No data. Call `get_points()` or `get_points_sample()` first.'
            )
        return self.__data
    
    def get_points(self,
                   lat: float | list[float], 
                   lon: float | list[float], 
                   *, 
                   soil_property: Union[str, list[str], None] = None, 
                   depth: Union[str, list[str], None] = None, 
                   value: Union[str, list[str], None] = None) -> pd.DataFrame:
        """Query Soilgrids for soil properties at specified locations.
    
        This function is a wrapper for the Soilgrids API. The returned geojson is
        parsed into a pandas DataFrame, with a row for each combination of 
        `lat`, `lon`, `soil_property`, and `depth`, and a column for each `value`.
        
        More detailed information about the data returned can be obtained from
        [IRSIC](https://www.isric.org/explore/soilgrids/faq-soilgrids).
        
        Args:
            `lat`: The latitude(s) of the point(s) to query. Must be in the range 
                [-90, 90].
            `lon`: The longitude(s) of the point(s) to query. Must be in the 
                range [-180, 180]. Note that NumPy-style broadcasting is 
                applied to lat and lon, so that if one is a scalar and the other 
                is an array, all combinations of the two are queried.
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
        self.__data = get_soilgrids(
            lat, lon, 
            soil_property=soil_property, depth=depth, value=value
        )
        
    
    def get_points_sample(self, 
                          n: int =5, 
                          *, 
                          lat_min: float =-90, 
                          lat_max: float =90, 
                          lon_min: float =-180, 
                          lon_max: float =180,
                          soil_property: Union[str, list[str], None] = None, 
                          depth: Union[str, list[str], None] = None, 
                          value: Union[str, list[str], None] = None) -> pd.DataFrame:
        """Query Soilgrids for a random set of coordinates.
        
        This function is a wrapper for the Soilgrids API. The returned geojson 
        is parsed into a pandas DataFrame, with a row for each combination of 
        `lat`, `lon`, `soil_property`, and `depth`, and a column for each 
        `value`.
        
        More detailed information about the data returned can be obtained from
        [ISRIC](https://www.isric.org/explore/soilgrids/faq-soilgrids).
        
        Args:
            `n`: The number of points to query.
            `lat_min`: The minimum latitude of the points to query. Must be in 
                the range [-90, 90].
            `lat_max`: The maximum latitude of the points to query. Must be in 
                the range [-90, 90].
            `lon_min`: The minimum longitude of the points to query. Must be in 
                the range [-180, 180].
            `lon_max`: The maximum longitude of the points to query. Must be in
                the range [-180, 180].
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
        self.__data = get_soilgrids(
            lat_min + (np.abs(lat_max - lat_min) * np.random.random_sample(n)).round(6),
            lon_min + (np.abs(lon_max - lon_min) * np.random.random_sample(n)).round(6),
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
            
    
    def ocs_correlations(self) -> None:
        """Get the correlation between sand, silt, clay, and OCS (organic carbon stock).
        
        1. First, the data is aggregated to get overall means for sand, silt,
           clay for the 0-30cm layer (this is because Soilgrids provides OCS
           data for the 0-30cm layer as a single value).
      
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
        
        model_summary = rscript(
            'r-scripts/linear-regression.R', 
            pivoted_data.to_csv()
        )
        
        logger.info(model_summary)
    
    
    def aggregate_means(self, top_depth=0, bottom_depth=30):
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
            .fillna({'mean': 0}) \
            .groupby(
                ['lat', 'lon', 'unit_depth', 'soil_property'], 
                as_index=False
            ) \
            .apply(lambda x: x.assign(
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
                thickness = lambda x: x['bottom_depth'] - x['top_depth'],
                mean = lambda x: (x['mean'] * x['thickness'] / x['thickness'].sum()) \
                    .round() \
                    .astype(np.int64)
            )) \
            .groupby(
                ['lat', 'lon', 'mapped_units', 'unit_depth', 'soil_property'], 
                as_index=False
            ) \
            .agg({
                'top_depth': 'min',
                'bottom_depth': 'max',
                'mean': 'sum'
            })

