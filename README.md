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


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    Cell In[1], line 21
         10     sg = SoilGrids()
         12     sg.get_points_sample(
         13         50,
         14         lat_min=56.225297, lat_max=55.958103,
       (...)
         18         value='mean'
         19     )
    ---> 21 sg.data \
         22     .filter([
         23         'lat', 'lon', 'soil_property', 'mapped_units', 
         24         'target_units', 'depth', 'mean'
         25     ])


    NameError: name 'sg' is not defined


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
      <td>56.235719</td>
      <td>9.227313</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>1</th>
      <td>56.237697</td>
      <td>8.984183</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>2</th>
      <td>56.239461</td>
      <td>9.191985</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>3</th>
      <td>56.255252</td>
      <td>9.049602</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>4</th>
      <td>56.259932</td>
      <td>8.923327</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>5</th>
      <td>56.262672</td>
      <td>9.002590</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>6</th>
      <td>56.264488</td>
      <td>9.004942</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>7</th>
      <td>56.267499</td>
      <td>9.058695</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>8</th>
      <td>56.273890</td>
      <td>9.107779</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>9</th>
      <td>56.297945</td>
      <td>9.109309</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>10</th>
      <td>56.303049</td>
      <td>8.864423</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>11</th>
      <td>56.311145</td>
      <td>8.916930</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>12</th>
      <td>56.312923</td>
      <td>9.068515</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>13</th>
      <td>56.315340</td>
      <td>8.905336</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>14</th>
      <td>56.318400</td>
      <td>8.995711</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>15</th>
      <td>56.318480</td>
      <td>9.187449</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>16</th>
      <td>56.320075</td>
      <td>8.884830</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>17</th>
      <td>56.329586</td>
      <td>8.906809</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>18</th>
      <td>56.329594</td>
      <td>9.119618</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>19</th>
      <td>56.330206</td>
      <td>9.236711</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>20</th>
      <td>56.335098</td>
      <td>8.693827</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>21</th>
      <td>56.336729</td>
      <td>9.042064</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>22</th>
      <td>56.337229</td>
      <td>9.130738</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>23</th>
      <td>56.343606</td>
      <td>8.953429</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>24</th>
      <td>56.356396</td>
      <td>8.958299</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>25</th>
      <td>56.358869</td>
      <td>8.803543</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>26</th>
      <td>56.359760</td>
      <td>8.789007</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>27</th>
      <td>56.365707</td>
      <td>9.074531</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>28</th>
      <td>56.369691</td>
      <td>8.910835</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>29</th>
      <td>56.370562</td>
      <td>8.963777</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>30</th>
      <td>56.391902</td>
      <td>9.198561</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>31</th>
      <td>56.395247</td>
      <td>9.280102</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>32</th>
      <td>56.404672</td>
      <td>9.154775</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>33</th>
      <td>56.405100</td>
      <td>9.009216</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>34</th>
      <td>56.407227</td>
      <td>8.928714</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>35</th>
      <td>56.407619</td>
      <td>8.765451</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>36</th>
      <td>56.411133</td>
      <td>8.932984</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>37</th>
      <td>56.425257</td>
      <td>8.972734</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>38</th>
      <td>56.425502</td>
      <td>9.219506</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>39</th>
      <td>56.431954</td>
      <td>8.729293</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>40</th>
      <td>56.432663</td>
      <td>9.001378</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>41</th>
      <td>56.437198</td>
      <td>8.981586</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>42</th>
      <td>56.444646</td>
      <td>9.261524</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>43</th>
      <td>56.453442</td>
      <td>9.345086</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>44</th>
      <td>56.460806</td>
      <td>9.332726</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>45</th>
      <td>56.463859</td>
      <td>8.770557</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>46</th>
      <td>56.471824</td>
      <td>9.139974</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>47</th>
      <td>56.477596</td>
      <td>9.092933</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>48</th>
      <td>56.480323</td>
      <td>9.201440</td>
      <td>sand</td>
    </tr>
    <tr>
      <th>49</th>
      <td>56.492063</td>
      <td>8.853880</td>
      <td>sand</td>
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
    -1.07700 -1.05049 -0.05614  0.92996  1.94212 
    
    Coefficients:
                  Estimate Std. Error t value Pr(>|t|)    
    (Intercept)  1.000e+03  1.337e+00 748.061   <2e-16 ***
    ocs         -1.738e-03  2.387e-02  -0.073    0.942    
    ---
    Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1
    
    Residual standard error: 0.8758 on 48 degrees of freedom
    Multiple R-squared:  0.0001104,	Adjusted R-squared:  -0.02072 
    F-statistic: 0.005302 on 1 and 48 DF,  p-value: 0.9423
    
    


## Disclaimers

*   Use of this package is subject to [ISRIC data and software policy](https://www.isric.org/about/data-policy).

*   This package is licensed as [GPL-2](LICENSE).
