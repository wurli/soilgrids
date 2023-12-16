import pandas as pd

class SoilGrids:
    """Read and perform basic analysis of Soilgrids data.
    
    Provides a convenient interface to the Soilgrids API, and some basic data
    wrangling and analysis methods.
    
    Attributes:
        `data` (`pandas.DataFrame`): The data returned by the last call to 
            `get_points()` or `get_points_sample()`. Note that this generates
            a `ValueError` if called before either of these methods.
        `region_bounds` (`dict`): The region_bounds of latitude and longitude returned covered
            by `data`. Note that this generates a `ValueError` if called before
            `get_points()` or `get_points_sample()`.
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
    
    # Import methods
    from ._set_data   import get_points, get_points_sample
    from ._data_ops   import rank_properties, aggregate_means
    from ._statistics import ocs_correlation
    from ._visualise  import plot_ocs_property_relationships, plot_property_map
    
    def __init__(self):
        self._data = None
        self._region_bounds = None
    
    @property
    def data(self) -> pd.DataFrame:
        """Data returned by the last call to `get_points()` or `get_points_sample()`.

        Raises:
            `ValueError`: If no data has been returned yet.

        Returns:
            `pandas.DataFrame`: A data frame of the form returned by 
            `get_soilgrids()`.
        """
        _check_data_available(self)
        return self._data
    
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
        return self._region_bounds or {
            'lat': (min(self._data['lat']), max(self._data['lat'])),
            'lon': (min(self._data['lon']), max(self._data['lon']))
        }


def _check_data_available(x: SoilGrids) -> None:
    """Raise an error if no data has been queried yet."""
    if x._data is None:
        raise ValueError(
            'No data. Call `get_points()` or `get_points_sample()` first.'
        )
        
            
    
    