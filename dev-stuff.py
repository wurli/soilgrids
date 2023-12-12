import soilgrids as sg


soilgrids = sg.SoilGrids()

soilgrids.aggregate_means
soilgrids.get_points
soilgrids.get_points_sample
soilgrids.ocs_correlations
soilgrids.main_properties

soilgrids.get_points_sample(
    50,
    lat_min=56.225297, lat_max=55.958103,
    lon_min=8.662215, lon_max=9.354390,
    soil_property=['clay', 'sand', 'silt', 'ocs'],
    depth=['0-5cm', '5-15cm', '15-30cm', '0-30cm'],
    value='mean'
)

soilgrids.ocs_correlations()

import numpy as np
55.958103 + (np.abs(56.225297 - 55.958103) * np.random.random_sample(5)).round(6)
