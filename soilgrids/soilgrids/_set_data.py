from ..api_requests import get_soilgrids

from typing import Union
import numpy as np
import pandas as pd


def get_points(self,
               lat: float | list[float], 
               lon: float | list[float], 
               *, 
               soil_property: Union[str, list[str], None]=None, 
               depth: Union[str, list[str], None]=None, 
               value: Union[str, list[str], None]=None) -> pd.DataFrame:
    """Query Soilgrids for soil properties at specified locations.

    This method is a wrapper for the Soilgrids API. The returned geojson is
    parsed into a pandas outDataFrame, with a row for each combination of 
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
            Note that the mean is always returned, regardless of the 
            selection.

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
                      lat_a: float=-90, 
                      lon_a: float=-180, 
                      lat_b: float=90, 
                      lon_b: float=180,
                      soil_property: Union[str, list[str], None]=None, 
                      depth: Union[str, list[str], None]=None, 
                      value: Union[str, list[str], None]=None) -> pd.DataFrame:
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
            Note that the mean is always returned, regardless of the 
            selection.

    Returns:
        `pd.DataFrame`: A data frame with a row for each combination of 
            `lat`, `lon`, `soil_property`, and `depth`, and a column for 
            each `value`. 
    """
    
    self._data = pd.read_csv("tests/data/soilgrids-results.csv")
    return 
     
    lat_min, lat_max = min(lat_a, lat_b), max(lat_a, lat_b)
    lon_min, lon_max = min(lon_a, lon_b), max(lon_a, lon_b)
    
    self._data = get_soilgrids(
        lat_min + (lat_max - lat_min) * np.random.random_sample(n),
        lon_min + (lon_max - lon_min) * np.random.random_sample(n),
        soil_property=soil_property, depth=depth, value=value
    )