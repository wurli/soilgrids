import soilgrids as sg

soilgrids = sg.SoilGrids()

soilgrids.get_points_sample(
    3,
    lat_min=56.225297, lat_max=55.958103,
    lon_min=8.662215, lon_max=9.354390,
    property=['clay', 'sand', 'silt', 'ocs'],
    depth=['0-5cm', '5-15cm', '15-30cm', '0-30cm'],
    value='mean'
)

soilgrids.aggregate_means()

sg.get_soilgrids(8.664051, 56.283198)

import numpy as np
x, y = np.broadcast_arrays(1, 2)


