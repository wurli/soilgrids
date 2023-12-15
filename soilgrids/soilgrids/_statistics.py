from .._utils import _rscript, _logger

def ocs_correlation(self,
                    top_depth: int | None=None, 
                    bottom_depth: int | None=None, 
                    capture_output: bool=False) -> None | str:
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
            `top_depth` (`float | None`): The minimum top depth to include in the 
            aggregated results. Note that the value returned in the output 
            may be higher. Defaults to `None`, in which case all 
            values are incuded. 
        `bottom_depth` (`float | None`): The maximum bottom depth to include 
            in the aggregated results. Note that the value returned in the 
            output may be lower. Defaults to `None`, in which case all 
            values are incuded.
        `capture_output` (`bool`): If `False` (the default), the model 
            summary is printed to the console. If `True`, the model summary
            is returned as a string.
    
    Returns:
        `None`: The model summary is printed to the console.
    """
    pivoted_data = self.aggregate_means(top_depth, bottom_depth) \
        .query("soil_property in ['sand', 'silt', 'clay', 'ocs']") \
        .pivot_table(
            index=['lat', 'lon'],
            columns='soil_property',
            values='mean'
        ) \
        .reset_index()
    
    assert len(pivoted_data) >= 20, \
        'At least 20 distinct values for `lat` and `lon` are needed to fit a linear model.'
    
    # Missing columns will be all NaN, which will throw a better error on 
    # the R side
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


