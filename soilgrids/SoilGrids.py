from .get_soilgrids import get_soilgrids
import numpy as np


class SoilGrids:
    
    def __init__(self):
        self.__data = None
    
    @property
    def data(self):
        if self.__data is None:
            raise ValueError(
                'No data. Call `get_points()` or `get_points_sample()` first.'
            )
        return self.__data
    
    def get_points(self, lat, lon, *, property=None, depth=None, value=None):
        self.__data = get_soilgrids(
            lat, lon, 
            property=property, depth=depth, value=value
        )
        
    def get_points_sample(self, n=5, *, 
                          lat_min=-90, lat_max=90, lon_min=-180, lon_max=180,
                          property=None, depth=None, value=None):
        self.__data = get_soilgrids(
            lat_min + np.abs(lat_max - lat_min) * np.random.random_sample(n).round(6),
            lon_min + np.abs(lon_max - lon_min) * np.random.random_sample(n).round(6),
            property=property, depth=depth, value=value
        )
        
    def main_properties(self):
        return self.aggregate_means() \
            .query('mapped_units == "g/kg"') \
            .sort_values(
                ['lat', 'lon', 'mapped_units', 'unit_depth', 'mean'], 
                ascending=False
            ) \
            .groupby(
                ['lat', 'lon', 'mapped_units', 'unit_depth'], 
                as_index=False
            ) \
            .apply(lambda g: g.iloc[0])
            
    def property_correlations(self):
        pivoted_data = self.aggregate_means() \
            .query('mapped_units == "g/kg"') \
            .pivot_table(
                index=['lat', 'lon'],
                columns='unit_depth',
                values='weighted_mean'
            ) \
            .reset_index()
            
    # TODO: Is this doing the right thing? Is the weighting resulting in
    # inflated/deflated values?
    def aggregate_means(self, top_depth=0, bottom_depth=30):
        assert 'mean' in self.data.keys(), \
            'No `mean` column. Call `get_points()` or `get_points_sample()`' \
            " with `value='mean'` first."
        
        d = self.data
        d = d[(top_depth <= d['top_depth']) & (d['bottom_depth'] <= bottom_depth)]
        
        return d \
            .fillna({'mean': 0}) \
            .groupby(
                ['lat', 'lon', 'unit_depth', 'property'], 
                as_index=False
            ) \
            .apply(lambda x: x.assign(
                # ~~ What's happening here? ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # Say we have the following values:
                #
                #    property     depth   mean
                #        sand    0- 5cm      1
                #        sand    5-15cm      2
                #        sand   15-30cm      3
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
                ['lat', 'lon', 'mapped_units', 'unit_depth', 'property'], 
                as_index=False
            ) \
            .agg({
                'top_depth': 'min',
                'bottom_depth': 'max',
                'mean': 'sum'
            })

