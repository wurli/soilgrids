# ============================================================================ #
# The scripts in this folder all relate to the `SoilGrids` class:
#   *  __init__.py: Instantiates the class and defines properties
#   *  Other files define methods
# NB, the class is broken up in this way as the resulting code is easier to
# read, maintain and extend.
# ============================================================================ #

import pandas as pd

class SoilGrids:
    """Read and perform basic analysis of Soilgrids data.
    
    Provides a convenient interface to the Soilgrids API, and some basic data
    wrangling and analysis methods.
    
    Attributes:
        `data` (`pandas.DataFrame`): The data returned by the last call to 
            `get_points()` or `get_points_sample()`. Note that this generates
            a `ValueError` if called before either of these methods.
        `region_bounds` (`dict`): The latitude and longitude ranges covered
            by `data`. Note that this generates a `ValueError` if called before
            `get_points()` or `get_points_sample()`.
        `get_points()` (method): Query Soilgrids for soil properties at 
            specified locations.
        `get_points_sample()` (method): Query a sample of points between
            specified latitude and longitude bounds.
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
    
    # Import methods
    from ._api_requests import get_points, get_points_sample
    from ._data_ops     import rank_properties, aggregate_means
    from ._statistics   import ocs_correlation
    from ._visualise    import plot_ocs_property_relationships, plot_property_map
    
    
    def __init__(self):
        self._data = None
        self._region_bounds = None
    
    
    @property
    def data(self) -> pd.DataFrame:
        """Get or set soilgrids data.
        
        Returns the results of the last call to `get_points()` or 
        `get_points_sample()`. This property can also be set manually (e.g.
        using the output of `get_soilgrids()`), in which case the 
        `region_bounds` property is also set.

        Raises:
            `ValueError`: If no data has been returned yet.

        Returns:
            `pandas.DataFrame`: A data frame of the form returned by 
            `get_soilgrids()`.
        """
        
        _check_data_available(self)
        return self._data
    
    
    @data.setter
    def data(self, value):
        self._region_bounds = {
            'lat': (min(value['lat']), max(value['lat'])),
            'lon': (min(value['lon']), max(value['lon']))
        } 
        self._data = value
    
    
    @property
    def region_bounds(self) -> dict:
        """region_bounds for latitude and longitude.
        
        Returns:
            `dict`: A dictionary of the form:
            ```python
            {'lat': (min, max), 'lon': (min, max)}
            ```
        """
        
        _check_data_available(self)
        return self._region_bounds


def _check_data_available(x: SoilGrids) -> None:
    """Raise an error if no data has been queried yet."""
    
    if x._data is None:
        raise ValueError(
            'No data. Call `get_points()` or `get_points_sample()` first.'
        )
        
            
    
    