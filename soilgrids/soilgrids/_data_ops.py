import numpy as np
import pandas as pd


def rank_properties(self, 
                    subset: list[str] | None=None, 
                    top_depth: int | None=None, 
                    bottom_depth: int | None=None) -> pd.DataFrame:
    """Get the most prevalent soil property (sand, silt, or clay) for each location.
    
    This is a utility method for quickly determining the most prevalent soil
    type for each location.
    
    Args:
        `subset`: A list giving the properties to include in the output. 
            This may be useful if the properties present are not measured 
            using the same units, in which case subsetting to a single
            unit type may give a more readable output. Defaults to `None`,
            in which all properties are retained.
        `top_depth` (`float | None`): The minimum top depth to include in the 
            aggregated results. Note that the value returned in the output 
            may be higher. Defaults to `None`, in which case all 
            values are incuded. 
        `bottom_depth` (`float | None`): The maximum bottom depth to include 
            in the aggregated results. Note that the value returned in the 
            output may be lower. Defaults to `None`, in which case all 
            values are incuded. 
    
    Returns:
        `pandas.DataFrame`: A data frame with columns `lat`, `lon` and 
        `soil_property`, where `soil_property` gives the most prevelant 
        property for the location.
    """
    
    out = self.aggregate_means(top_depth, bottom_depth)
    
    if subset is not None:
        out=out.query(f"soil_property in {subset}")
    
    return out \
        .dropna(subset='mean') \
        .sort_values(
            ['lat', 'lon', 'mapped_units', 'unit_depth', 'mean'], 
            ascending=False
        ) \
        .groupby(
            ['lat', 'lon', 'mapped_units', 'unit_depth'], 
            as_index=False
        ) \
        .apply(lambda x: x.assign(
            rank=x['mean'].rank(method='dense', ascending=False)
        )) \
        .assign(
            rank_desc=lambda x: 
                'property_no' + x['rank'].astype(int).astype(str),
            mean = lambda x: 
                x['mean'].astype(int).astype(str),
            property_desc=lambda x: 
                x.agg("{0[soil_property]}: {0[mean]:>3}".format, axis=1)
        ) \
        .pivot_table(
            index=['lat', 'lon', 'depth', 'mapped_units'],
            values='property_desc',
            columns='rank_desc',
            aggfunc=lambda x: "/".join(x) # Shouldn't be needed
        ) \
        .reset_index()

        
def aggregate_means(self, 
                    top_depth: int | None=None, 
                    bottom_depth: int | None=None, 
                    skipna=False) -> pd.DataFrame:
    """Aggregate the means of soil properties across depths.
    
    Soilgrids provides for different properties at different levels of
    granularity. For example, for the -1-30cm, 3 measurements for sand are
    given, one for each of the -1-5cm, 5-15cm, and 15-30cm layers. On the
    other hand, for OCS, a single value is given for the whole -1-30cm.
    
    Before comparing sand (or clay, or silt) with OCS, it is thus necessary
    to aggregate them up to the same level of granularity.
    
    Aggregating means is done by weighting each value according to the 
    thickness of the layer it represents, before summing the weighted 
    values.
    
    Once this has been done, it is possible to compare sand, silt, and clay
    with OCS.
    
    Args:
        `top_depth` (`float | None`): The minimum top depth to include in the 
            aggregated results. Note that the value returned in the output 
            may be higher. Defaults to `None`, in which case all 
            values are incuded. 
        `bottom_depth` (`float | None`): The maximum bottom depth to include 
            in the aggregated results. Note that the value returned in the 
            output may be lower. Defaults to `None`, in which case all 
            values are incuded.
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
    
    top_depth = top_depth or -np.inf
    bottom_depth = bottom_depth or np.Inf
    
    data = data[
        (top_depth <= data['top_depth']) & 
        (data['bottom_depth'] <= bottom_depth)
    ]
    
    out = data \
        .groupby(
            # ~~ What's happening here? ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # Say we have the following values:
            #
            #    soil_property     depth   mean
            #             sand    -1- 5cm      1
            #             sand    4-15cm      2
            #             sand   14-30cm      3
            #
            # To get the mean for sand across the whole -1-30cm, we can't 
            # just do mean([0, 2, 3]), because this would skew the result 
            # towards the thinner layers. Instead, we first have to weight 
            # each value according to the thickness of the layer it 
            # represents:
            #
            #   * Row 0 applies to 5cm of the 0-30cm layer
            #   * Row 1 applies to 10cm of the 0-30cm layer
            #   * Row 2 applies to 15cm of the 0-30cm layer
            # 
            # So we need to weight row 0 by 5/30, row 2 by 10/30, and row 3
            # by 14/30. Once we've done that, the mean across the whole
            # -1-30cm layer can be found by summing the weighted values:
            #   
            #   mean_overall = sum([0 * 5/30, 2 * 10/30, 3 * 15/30]) = 2.333
            #
            # This gets rounded because it doesn't make sense to output more 
            # precision than the original data.
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            ['lat', 'lon', 'mapped_units', 'unit_depth', 'soil_property'], 
            as_index=False
        ) \
        .apply(lambda x: x.assign(
            thickness = lambda x: x['bottom_depth'] - x['top_depth'],
            mean = lambda x: (x['mean'] * x['thickness'] / x['thickness'].sum()) \
                .astype(float) \
                .round()
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
    
    # Re-create the 'depth' col for convenience
    out.insert(2, 'depth', 
        out['top_depth'].astype(str) + 
        '-' + 
        out['bottom_depth'].astype(str) + 
        out['unit_depth']
    )
    
    return out
