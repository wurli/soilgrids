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

## Querying data using `SoilGrids`:
The following code reads in the mean values for clay, sand, silt and ocs 
(organic carbon stock) in the top 30cm of soil for a random set of 50 points 
within roughly 25km of 
[Herning, Denmark](https://en.wikipedia.org/wiki/Herning). Note that points can 
be queried at a maximum rate of 5/minute, so the following code takes about 10 
minutes to run:


```python
# ~~~ Console messages disabled for a cleaner output ~~~ #
import logging
logging.getLogger('soilgrids').setLevel(logging.ERROR)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

from soilgrids import SoilGrids
import pandas as pd


sg = SoilGrids()

sg.get_points_sample(
    50,
    lat_min=56.225297, lat_max=55.958103,
    lon_min=8.662215, lon_max=9.354390,
    soil_property=['clay', 'sand', 'silt', 'ocs'],
    depth=['0-5cm', '5-15cm', '15-30cm', '0-30cm'],
    value='mean'
)

sg.data \
    .filter([
        'lat', 'lon', 'soil_property', 'mapped_units', 
        'target_units', 'depth', 'mean'
    ])
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>lat</th>
      <th>lon</th>
      <th>soil_property</th>
      <th>mapped_units</th>
      <th>target_units</th>
      <th>depth</th>
      <th>mean</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>56.276607</td>
      <td>9.069328</td>
      <td>clay</td>
      <td>g/kg</td>
      <td>%</td>
      <td>0-5cm</td>
      <td>58</td>
    </tr>
    <tr>
      <th>1</th>
      <td>56.276607</td>
      <td>9.069328</td>
      <td>clay</td>
      <td>g/kg</td>
      <td>%</td>
      <td>5-15cm</td>
      <td>52</td>
    </tr>
    <tr>
      <th>2</th>
      <td>56.276607</td>
      <td>9.069328</td>
      <td>clay</td>
      <td>g/kg</td>
      <td>%</td>
      <td>15-30cm</td>
      <td>64</td>
    </tr>
    <tr>
      <th>3</th>
      <td>56.276607</td>
      <td>9.069328</td>
      <td>ocs</td>
      <td>t/ha</td>
      <td>kg/m²</td>
      <td>0-30cm</td>
      <td>66</td>
    </tr>
    <tr>
      <th>4</th>
      <td>56.276607</td>
      <td>9.069328</td>
      <td>sand</td>
      <td>g/kg</td>
      <td>%</td>
      <td>0-5cm</td>
      <td>844</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>5</th>
      <td>56.276492</td>
      <td>8.923697</td>
      <td>sand</td>
      <td>g/kg</td>
      <td>%</td>
      <td>5-15cm</td>
      <td>836</td>
    </tr>
    <tr>
      <th>6</th>
      <td>56.276492</td>
      <td>8.923697</td>
      <td>sand</td>
      <td>g/kg</td>
      <td>%</td>
      <td>15-30cm</td>
      <td>810</td>
    </tr>
    <tr>
      <th>7</th>
      <td>56.276492</td>
      <td>8.923697</td>
      <td>silt</td>
      <td>g/kg</td>
      <td>%</td>
      <td>0-5cm</td>
      <td>111</td>
    </tr>
    <tr>
      <th>8</th>
      <td>56.276492</td>
      <td>8.923697</td>
      <td>silt</td>
      <td>g/kg</td>
      <td>%</td>
      <td>5-15cm</td>
      <td>111</td>
    </tr>
    <tr>
      <th>9</th>
      <td>56.276492</td>
      <td>8.923697</td>
      <td>silt</td>
      <td>g/kg</td>
      <td>%</td>
      <td>15-30cm</td>
      <td>121</td>
    </tr>
  </tbody>
</table>
<p>500 rows × 7 columns</p>
</div>



## Get the property (clay, sand, silt) with the highest value for each point
The `SoilGrids` class provides a handy utility `main_properties()` for finding
the most abundant soil type (i.e. property) for each point. In this case, we
see that the Herning region is quite sandy:


```python
sg.main_properties()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>lat</th>
      <th>lon</th>
      <th>soil_property</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>56.226264</td>
      <td>9.310044</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>1</th>
      <td>56.240131</td>
      <td>9.085027</td>
      <td>clay</td>
    </tr>
    <tr>
      <th>2</th>
      <td>56.240232</td>
      <td>8.923844</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>3</th>
      <td>56.257524</td>
      <td>8.701260</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>4</th>
      <td>56.263617</td>
      <td>8.884656</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>5</th>
      <td>56.267173</td>
      <td>9.272709</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>6</th>
      <td>56.269523</td>
      <td>9.024149</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>7</th>
      <td>56.270786</td>
      <td>9.056345</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>8</th>
      <td>56.271717</td>
      <td>8.752865</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>9</th>
      <td>56.271802</td>
      <td>8.721928</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>10</th>
      <td>56.276492</td>
      <td>8.923697</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>11</th>
      <td>56.276607</td>
      <td>9.069328</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>12</th>
      <td>56.285562</td>
      <td>8.831884</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>13</th>
      <td>56.292184</td>
      <td>9.018149</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>14</th>
      <td>56.295637</td>
      <td>8.973799</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>15</th>
      <td>56.301430</td>
      <td>8.947664</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>16</th>
      <td>56.312244</td>
      <td>9.033930</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>17</th>
      <td>56.320408</td>
      <td>9.099744</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>18</th>
      <td>56.337811</td>
      <td>9.102337</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>19</th>
      <td>56.341841</td>
      <td>9.194195</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>20</th>
      <td>56.344729</td>
      <td>9.196675</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>21</th>
      <td>56.345896</td>
      <td>8.667457</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>22</th>
      <td>56.346370</td>
      <td>9.202317</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>23</th>
      <td>56.353099</td>
      <td>9.168756</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>24</th>
      <td>56.356364</td>
      <td>8.911127</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>25</th>
      <td>56.360388</td>
      <td>9.220224</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>26</th>
      <td>56.362676</td>
      <td>8.894764</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>27</th>
      <td>56.363781</td>
      <td>9.145282</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>28</th>
      <td>56.375587</td>
      <td>9.208008</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>29</th>
      <td>56.382394</td>
      <td>9.065123</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>30</th>
      <td>56.383332</td>
      <td>9.026549</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>31</th>
      <td>56.383418</td>
      <td>9.057628</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>32</th>
      <td>56.403295</td>
      <td>9.287058</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>33</th>
      <td>56.405351</td>
      <td>9.140873</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>34</th>
      <td>56.410998</td>
      <td>8.755577</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>35</th>
      <td>56.430169</td>
      <td>8.839292</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>36</th>
      <td>56.433262</td>
      <td>8.690437</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>37</th>
      <td>56.433473</td>
      <td>8.951179</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>38</th>
      <td>56.439106</td>
      <td>8.688263</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>39</th>
      <td>56.445124</td>
      <td>9.040367</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>40</th>
      <td>56.450100</td>
      <td>9.033623</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>41</th>
      <td>56.454865</td>
      <td>8.677666</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>42</th>
      <td>56.456948</td>
      <td>9.147255</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>43</th>
      <td>56.458241</td>
      <td>8.792846</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>44</th>
      <td>56.475961</td>
      <td>8.833438</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>45</th>
      <td>56.480569</td>
      <td>9.211856</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>46</th>
      <td>56.481033</td>
      <td>8.703145</td>
      <td>clay</td>
    </tr>
    <tr>
      <th>47</th>
      <td>56.483997</td>
      <td>9.324725</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>48</th>
      <td>56.485126</td>
      <td>9.219960</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>49</th>
      <td>56.485551</td>
      <td>8.890252</td>
      <td>clay</td>
    </tr>
  </tbody>
</table>
</div>



## Relationship between clay, sand, silt and organic carbon stock
The `ocs_correlation()` method fits and displays summary statistics for a linear 
model using sand, clay and silt as predictors and OCS as the response variable. 
In this case, we find that these properties are not particularly correlated 
with OCS.


```python
print(sg.ocs_correlation(capture_output=True))
```

    
    Call:
    lm(formula = clay + sand + silt ~ ocs, data = input_data)
    
    Residuals:
         Min       1Q   Median       3Q      Max 
    -184.510  -57.234    6.529   54.289  182.565 
    
    Coefficients:
                Estimate Std. Error t value Pr(>|t|)    
    (Intercept) 113.2903    45.7361   2.477   0.0168 *  
    ocs          16.0033     0.8548  18.721   <2e-16 ***
    ---
    Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1
    
    Residual standard error: 84.13 on 48 degrees of freedom
    Multiple R-squared:  0.8795,	Adjusted R-squared:  0.877 
    F-statistic: 350.5 on 1 and 48 DF,  p-value: < 2.2e-16
    
    


## Disclaimers

*   Use of this package is subject to [ISRIC data and software policy](https://www.isric.org/about/data-policy).

*   This package is licensed as [GPL-2](LICENSE).
