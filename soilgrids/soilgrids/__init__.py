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
        `rank_properties()` (method): Determine the relative prevalence of 
            different properties for each location.
        `ocs_correlation()` (method): Analyse the relationship between sand, 
            silt, clay, and OCS (organic carbon stock).
        `aggregate_means()` (method): Aggregate the means of soil properties 
            across depths.
        `plot_ocs_property_relationships()` (method): Plot OCS against each
            other property as a scatterplot, and fit a line between the points.
        `plot_property_map()` (method): Plot soil properties on a map.
"""
    
    def __init__(self):
        self._data = None
    
    # Import methods
    from ._set_data   import get_points, get_points_sample
    from ._data_ops   import rank_properties, aggregate_means
    from ._statistics import ocs_correlation
    from ._visualise  import plot_ocs_property_relationships, plot_property_map
    
    @property
    def data(self) -> pd.DataFrame:
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
    
    
        
            
    
    