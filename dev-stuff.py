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


soilgrids.aggregate_means(top_depth=1)
soilgrids.main_properties()
sg.get_points_sample(
    3,
    lat_min=56.225297, lat_max=55.958103,
    lon_min=8.662215, lon_max=9.354390,
    property=['clay', 'sand', 'silt', 'ocs'],
    depth=['0-5cm', '5-15cm', '15-30cm', '0-30cm'],
    value='mean'
)

round(1.1234567, 5)