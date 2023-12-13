import soilgrids as sg

sg.get_soilgrids

soilgrids = sg.SoilGrids()

soilgrids.get_points_sample(
    8,
    lat_min=56.225297, lat_max=55.958103,
    lon_min=8.662215, lon_max=9.354390,
    soil_property=['clay', 'sand', 'silt', 'ocs'],
    depth=['0-5cm', '5-15cm', '15-30cm', '0-30cm'],
    value=['mean', 'uncertainty']
)

soilgrids.aggregate_means
soilgrids.get_points
soilgrids.get_points_sample
soilgrids.ocs_correlation
soilgrids.main_properties
soilgrids.ocs_correlation()

import requests
req = requests.get(
    'https://rest.isric.org/soilgrids/v2.0/' + 'properties/query',
    params={
        'lat': 56.225297, 
        'lon': 55.958103, 
        # NB, 'property' is a reserved keyword in Python, so it's best
        # to use a different name here
        'property': ['clay', 'sand', 'silt', 'ocs'],
        'depth': ['0-5cm', '5-15cm', '15-30cm', '0-30cm'],
        'value': 'mean'
    },
    headers={'accept': 'application/geojson'}
)

json = req.json()


import numpy as np
import pandas as pd

df = pd.read_csv('soilgrids-results.csv') \
    .fillna({'mean': 0}) \
    .groupby(
        ['lat', 'lon', 'unit_depth', 'soil_property'], 
        as_index=False
    ) \
    .apply(lambda x: x.assign(
        thickness = lambda x: x['bottom_depth'] - x['top_depth'],
        mean = lambda x: (x['mean'] * x['thickness'] / x['thickness'].sum()) \
            .round() \
            .astype(np.int64)
    )) \
    .groupby(
        ['lat', 'lon', 'mapped_units', 'unit_depth', 'soil_property'], 
        as_index=False
    ) \
    .agg({
        'top_depth': 'min',
        'bottom_depth': 'max',
        'mean': 'sum'
    }) \
    .query("soil_property in ['sand', 'silt', 'clay', 'ocs']") \
    .pivot_table(
        index=['lat', 'lon'],
        columns='soil_property',
        values='mean'
    ) \
    .reset_index()
    
x = sg._utils._rscript('r-scripts/linear-regression.R', df.to_csv(index=False))
print(x.stdout)

type(x)
