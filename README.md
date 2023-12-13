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
| 56.227  | 8.95852 | sand            |
| 56.2282 | 8.78386 | sand            |
| 56.239  | 8.8889  | sand            |
| 56.2432 | 9.01111 | sand            |
| 56.2581 | 8.76906 | sand            |
| 56.2614 | 9.31379 | sand            |
| 56.2721 | 9.08447 | sand            |
| 56.2824 | 9.16308 | sand            |
| 56.2889 | 8.81124 | sand            |
| 56.2929 | 8.72278 | sand            |
| 56.2946 | 8.96107 | sand            |
| 56.3012 | 9.21258 | sand            |
| 56.302  | 8.86036 | sand            |
| 56.3059 | 9.27081 | sand            |
| 56.3111 | 8.72808 | sand            |
| 56.3184 | 9.05734 | sand            |
| 56.3209 | 9.108   | sand            |
| 56.3273 | 8.74746 | sand            |
| 56.3285 | 8.86959 | sand            |
| 56.329  | 9.02623 | sand            |
| 56.3359 | 8.91845 | sand            |
| 56.3488 | 9.13769 | sand            |
| 56.3513 | 9.26886 | sand            |
| 56.3524 | 8.88601 | sand            |
| 56.3581 | 8.96305 | sand            |
| 56.3661 | 9.31728 | sand            |
| 56.3666 | 8.93146 | sand            |
| 56.3691 | 8.93212 | sand            |
| 56.3707 | 9.31411 | sand            |
| 56.3735 | 9.05815 | sand            |
| 56.3759 | 8.79767 | sand            |
| 56.3892 | 8.86646 | sand            |
| 56.3925 | 9.27119 | sand            |
| 56.3937 | 9.02506 | sand            |
| 56.3949 | 8.80218 | sand            |
| 56.4194 | 9.28738 | sand            |
| 56.4219 | 8.82862 | sand            |
| 56.4322 | 9.05632 | sand            |
| 56.4358 | 8.69287 | sand            |
| 56.446  | 8.69823 | sand            |
| 56.4538 | 8.751   | sand            |
| 56.4597 | 9.28579 | sand            |
| 56.4727 | 8.95341 | sand            |
| 56.4727 | 9.0427  | sand            |
| 56.4734 | 8.71213 | sand            |
| 56.4775 | 9.23639 | sand            |
| 56.4795 | 8.8428  | sand            |
| 56.4816 | 9.12634 | sand            |
| 56.4885 | 9.35333 | sand            |
| 56.4891 | 8.81222 | sand            |


## Relationship between clay, sand, silt and organic carbon stock

The `ocs_correlation()` method fits and displays summary statistics for a linear 
model with sand, clay and silt as predictors and OCS as the response variable. 
Based on the R-squared values returned in the summary, it doesn't look like
these soil properties are particularly good predictors for OCS in this case:


```python
print(sg.ocs_correlation(capture_output=True))
```

    
    Call:
    lm(formula = clay + sand + silt ~ ocs, data = input_data)
    
    Residuals:
        Min      1Q  Median      3Q     Max 
    -1.2765 -0.2709 -0.2256  0.7589  1.7634 
    
    Coefficients:
                 Estimate Std. Error t value Pr(>|t|)    
    (Intercept) 1.000e+03  1.123e+00 890.668   <2e-16 ***
    ocs         4.424e-03  1.967e-02   0.225    0.823    
    ---
    Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1
    
    Residual standard error: 0.8302 on 48 degrees of freedom
    Multiple R-squared:  0.001053,	Adjusted R-squared:  -0.01976 
    F-statistic: 0.05058 on 1 and 48 DF,  p-value: 0.823
    
    


## Disclaimers

*   Use of this package is subject to [ISRIC data and software policy](https://www.isric.org/about/data-policy).
*   This package is licensed as [GPL-2](LICENSE).
