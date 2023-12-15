"""A Python wrapper for the Soilgrids API

This package provides a minimal wrapper for the ISRIC Soilgrids API, allowing 
users to query soil properties at a particular location and to perform basic 
analyses on the returned data.

Useful links:
    *  Documentation for the API: <https://rest.isric.org/soilgrids/v2.0/docs>
    *  ISRIC REST entry page, including fair use policy: <https://rest.isric.org>
    *  ISRIC data and software policy: <https://www.isric.org/about/data-policy>
    *  Soilgrids FAQ: <https://www.isric.org/explore/soilgrids/faq-soilgrids>

Use of this package is subject to 
[ISRIC data and software policy](https://www.isric.org/about/data-policy).

Functions:
    `get_soilgrids()`: Provides a simple wrapper for the /properties/query
        API endpoint, parsing the geojson response into a pandas DataFrame.
        
Classes:
    `SoilGrids()`: Provides methods for reading data from Soilgrids and basic 
        including utilities for aggregating and analysing the returned data.
        
This package is licensed as 
[GPL-2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html).
"""

import logging

from .api_requests import get_soilgrids
from .soilgrids    import SoilGrids

logging.basicConfig(level=logging.INFO, format='%(message)s')

__all__ = [
    'SoilGrids',
    'get_soilgrids',
]
