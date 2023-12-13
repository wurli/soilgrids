# soilgrids

This package provides a minimal wrapper for the ISRIC Soilgrids API, allowing 
users to query soil properties by latitude/longitude and to perform basic 
analyses on the returned data.

Functions:

*   `get_soilgrids()`: Provides a simple wrapper for the /properties/query
    API endpoint, parsing the geojson response into a pandas DataFrame.
        
Classes:

*   `SoilGrids()`: Provides methods for reading data from Soilgrids and basic 
    including utilities for aggregating and analysing the returned data.

Useful links:

*   Documentation for the API: <https://rest.isric.org/soilgrids/v2.0/docs>
*   ISRIC REST entry page, including fair use policy: <https://rest.isric.org>
*   ISRIC data and software policy: <https://www.isric.org/about/data-policy>
*   Soilgrids FAQ: <https://www.isric.org/explore/soilgrids/faq-soilgrids>

## Querying data using `SoilGrids`

The following code reads in the mean values for clay, sand, silt and organic 
carbon stock (ocs) in the top 30cm of soil for a random set of 50 points 
within roughly 25km of 
[Herning, Denmark](https://en.wikipedia.org/wiki/Herning). Note that points can 
be queried at a maximum rate of 5/minute, so the following code takes about 10 
minutes to run:


```python
import logging
from soilgrids import SoilGrids
import pandas as pd
from IPython.display import Markdown as md

# Turn off console logs for cleaner notebook output
logging.getLogger('soilgrids').setLevel(logging.ERROR)

# Helper for displaying tables as markdown
show = lambda df: display(md(df.to_markdown(index=False)))

sg = SoilGrids()

sg.get_points_sample(
    50,
    lat_min=56.225297, lat_max=55.958103,
    lon_min=8.662215, lon_max=9.354390,
    soil_property=['clay', 'sand', 'silt', 'ocs'],
    depth=['0-5cm', '5-15cm', '15-30cm', '0-30cm'],
    value='mean'
)

# For brevity, only a subset of the data is shown
show(data[0:15].filter([
    'lat', 'lon', 'soil_property', 'mapped_units', 
    'target_units', 'depth', 'mean'
]))
```


|     lat |     lon | soil_property   | mapped_units   | target_units   | depth   |   mean |
|--------:|--------:|:----------------|:---------------|:---------------|:--------|-------:|
| 56.3866 | 8.88611 | clay            | g/kg           | %              | 0-5cm   |    120 |
| 56.3866 | 8.88611 | clay            | g/kg           | %              | 5-15cm  |    117 |
| 56.3866 | 8.88611 | clay            | g/kg           | %              | 15-30cm |    111 |
| 56.3866 | 8.88611 | ocs             | t/ha           | kg/m²          | 0-30cm  |     69 |
| 56.3866 | 8.88611 | sand            | g/kg           | %              | 0-5cm   |    719 |
| 56.3866 | 8.88611 | sand            | g/kg           | %              | 5-15cm  |    727 |
| 56.3866 | 8.88611 | sand            | g/kg           | %              | 15-30cm |    726 |
| 56.3866 | 8.88611 | silt            | g/kg           | %              | 0-5cm   |    161 |
| 56.3866 | 8.88611 | silt            | g/kg           | %              | 5-15cm  |    156 |
| 56.3866 | 8.88611 | silt            | g/kg           | %              | 15-30cm |    163 |


## Get the property (clay, sand, silt) with the highest value for each point

The `SoilGrids` class provides a handy utility `main_properties()` for finding
the most abundant soil type (i.e. property) for each point. In this case, we
see that the Herning region is quite sandy:


```python
show(sg.main_properties())
```


|     lat |     lon | soil_property   |
|--------:|--------:|:----------------|
| 56.4323 | 8.80164 | sand            |


## Relationship between clay, sand, silt and organic carbon stock

The `ocs_correlation()` method fits and displays summary statistics for a linear 
model with sand, clay and silt as predictors and OCS as the response variable. 
In this case, we find these soil properties are quite effective at predicting 
OCS, explaining around 90% of the variance:


```python
print(sg.ocs_correlation(capture_output=True))
```

## Disclaimers

*   Use of this package is subject to [ISRIC data and software policy](https://www.isric.org/about/data-policy).
*   This package is licensed as [GPL-2](LICENSE).
