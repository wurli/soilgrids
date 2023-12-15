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
        `ocs_correlation()` (method): Determine the correlation between sand, 
            silt, clay, and OCS (organic carbon stock).
        `aggregate_means()` (method): Aggregate the means of soil properties 
            across depths.
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
    
    
        
            
    
    