import pytest

from soilgrids import SoilGrids
import pandas as pd


def test_soilgrids_data():
    sg = SoilGrids()

    with pytest.raises(ValueError) as err:
        sg.data
    assert 'No data' in str(err.value), 'Error message should indicate no data loaded'

    sg.data = pd.DataFrame({
        'lat': {0: 8.663411, 1: 8.663411, 3: 8.663411, 10: 8.680699, 11: 8.680699, 13: 8.680699}, 
        'lon': {0: 56.323929, 1: 56.323929, 3: 56.323929, 10: 56.441106, 11: 56.441106, 13: 56.441106}, 
        'soil_property': {0: 'clay', 1: 'clay', 3: 'ocs', 10: 'clay', 11: 'clay', 13: 'ocs'}, 
        'd_factor': {0: 10, 1: 10, 3: 10, 10: 10, 11: 10, 13: 10}, 
        'mapped_units': {0: 'g/kg', 1: 'g/kg', 3: 't/ha', 10: 'g/kg', 11: 'g/kg', 13: 't/ha'}, 
        'target_units': {0: '%', 1: '%', 3: 'kg/m²', 10: '%', 11: '%', 13: 'kg/m²'}, 
        'uncertainty_unit': {0: '', 1: '', 3: '', 10: '', 11: '', 13: ''}, 
        'depth': {0: '0-5cm', 1: '5-15cm', 3: '0-30cm', 10: '0-5cm', 11: '5-15cm', 13: '0-30cm'}, 
        'top_depth': {0: 0, 1: 5, 3: 0, 10: 0, 11: 5, 13: 0}, 
        'bottom_depth': {0: 5, 1: 15, 3: 30, 10: 5, 11: 15, 13: 30}, 
        'unit_depth': {0: 'cm', 1: 'cm', 3: 'cm', 10: 'cm', 11: 'cm', 13: 'cm'}, 
        'mean': {0: 63.0, 1: 64.0, 3: 60.0, 10: 128.0, 11: 124.0, 13: 55.0}
    })

    assert type(sg.data) == pd.DataFrame, 'sg.data should be a pandas DataFrame'
    
    assert sg._region_bounds is not None, 'region_bounds should be set when data is set'
    
    assert sg.region_bounds == {'lat': (8.663411, 8.680699), 'lon': (56.323929, 56.441106)}, \
        "region_bounds should be {'lat': (8.663411, 8.680699), 'lon': (56.323929, 56.441106)}"
        
    
def test_rank_properties():
    sg = SoilGrids()
    sg.data = pd.DataFrame({
        'lat': {0: 8.663411, 1: 8.663411, 3: 8.663411, 10: 8.680699, 11: 8.680699, 13: 8.680699}, 
        'lon': {0: 56.323929, 1: 56.323929, 3: 56.323929, 10: 56.441106, 11: 56.441106, 13: 56.441106}, 
        'soil_property': {0: 'clay', 1: 'clay', 3: 'ocs', 10: 'sand', 11: 'sand', 13: 'ocs'}, 
        'd_factor': {0: 10, 1: 10, 3: 10, 10: 10, 11: 10, 13: 10}, 
        'mapped_units': {0: 'g/kg', 1: 'g/kg', 3: 't/ha', 10: 'g/kg', 11: 'g/kg', 13: 't/ha'}, 
        'target_units': {0: '%', 1: '%', 3: 'kg/m²', 10: '%', 11: '%', 13: 'kg/m²'}, 
        'uncertainty_unit': {0: '', 1: '', 3: '', 10: '', 11: '', 13: ''}, 
        'depth': {0: '0-5cm', 1: '5-15cm', 3: '0-30cm', 10: '0-5cm', 11: '5-15cm', 13: '0-30cm'}, 
        'top_depth': {0: 0, 1: 5, 3: 0, 10: 0, 11: 5, 13: 0}, 
        'bottom_depth': {0: 5, 1: 15, 3: 30, 10: 5, 11: 15, 13: 30}, 
        'unit_depth': {0: 'cm', 1: 'cm', 3: 'cm', 10: 'cm', 11: 'cm', 13: 'cm'}, 
        'mean': {0: 63.0, 1: 64.0, 3: 60.0, 10: 128.0, 11: 124.0, 13: 55.0}
    })

    props = sg.rank_properties(['clay', 'sand'], top_depth=0, bottom_depth=30)
    
    assert len(props) == 2, 'rank_properties() should return a row for each point'

    assert set(props.columns) == {'lat', 'lon', 'depth', 'mapped_units', 'property_no1'}, \
        "main_properties() should return a DataFrame with columns 'lat', 'lon', 'depth', 'mapped_units', 'property_no1'"
         
    assert list(props['property_no1'][0:2]) == ['clay:  64', 'sand: 126'], \
        "First two main properties should be 'clay:  64' and 'sand: 126'"
        
    assert props['depth'][0] == '0-15cm', "Output depth should be '0-15cm'"

        
def test_ocs_correlation_works():
    sg = SoilGrids()
    data = pd.read_csv('tests/data/soilgrids-results.csv')
    sg.data= data

    lm = sg.ocs_correlation(capture_output=True)
    
    assert 'clay + sand + silt ~ ocs'       in lm, 'ocs_correlation() should return a linear model summary'
    assert 'Residual standard error: 0.948' in lm, 'Model summary should give a standard error of 0.948'
    
def test_ocs_correlation_fails_with_missing_properties():
    sg = SoilGrids()
    data = pd.read_csv('tests/data/soilgrids-results.csv')        
    sg.data= data \
        .query("soil_property != 'clay'") \
        .reset_index(drop=True)
        
    with pytest.raises(RuntimeError) as err:
        sg.ocs_correlation(capture_output=True)
    assert "No non-missing values for 'clay'" in str(err.value), 'ocs_correlation() should fail with all missing data'


def test_ocs_correlation_fails_with_limited_data():
    sg = SoilGrids()
    data = pd.read_csv('tests/data/soilgrids-results.csv')        
        
    ten_points = data \
        .drop_duplicates(subset=['lat', 'lon']) \
        .filter(['lat', 'lon']) \
        [0:2]

    sg.data= data.merge(ten_points, on=['lat', 'lon'], how='inner')

    with pytest.raises(AssertionError) as err:
        sg.ocs_correlation(capture_output=True)
    
    assert '20 distinct values for `lat` and `lon` are needed' in str(err.value), \
        'Error message should indicate not enough data'
    
def test_aggregate_means(): 
    sg = SoilGrids()
    sg.data = pd.DataFrame({
        'lat': {0: 8.663411, 1: 8.663411, 3: 8.663411, 10: 8.680699, 11: 8.680699, 13: 8.680699}, 
        'lon': {0: 56.323929, 1: 56.323929, 3: 56.323929, 10: 56.441106, 11: 56.441106, 13: 56.441106}, 
        'soil_property': {0: 'clay', 1: 'clay', 3: 'ocs', 10: 'clay', 11: 'clay', 13: 'ocs'}, 
        'd_factor': {0: 10, 1: 10, 3: 10, 10: 10, 11: 10, 13: 10}, 
        'mapped_units': {0: 'g/kg', 1: 'g/kg', 3: 't/ha', 10: 'g/kg', 11: 'g/kg', 13: 't/ha'}, 
        'target_units': {0: '%', 1: '%', 3: 'kg/m²', 10: '%', 11: '%', 13: 'kg/m²'}, 
        'uncertainty_unit': {0: '', 1: '', 3: '', 10: '', 11: '', 13: ''}, 
        'depth': {0: '0-5cm', 1: '5-15cm', 3: '0-30cm', 10: '0-5cm', 11: '5-15cm', 13: '0-30cm'}, 
        'top_depth': {0: 0, 1: 5, 3: 0, 10: 0, 11: 5, 13: 0}, 
        'bottom_depth': {0: 5, 1: 15, 3: 30, 10: 5, 11: 15, 13: 30}, 
        'unit_depth': {0: 'cm', 1: 'cm', 3: 'cm', 10: 'cm', 11: 'cm', 13: 'cm'}, 
        'mean': {0: 9.0, 1: 12.0, 3: 60.0, 10: 128.0, 11: 124.0, 13: 55.0}
    })

    agg = sg.aggregate_means()

    assert type(agg) == pd.DataFrame,                    'aggregate_means() should return a pandas DataFrame'
    assert set(agg['mapped_units']) == {'g/kg', 't/ha'}, 'aggregate_means() should split results by `mapped_units`'
    assert agg['mean'][0] == 11,                         '0-5cm ~ 9, 5-15cm ~ 12 should aggregate to 9 * 5/15 + 12 * 10/15 = 11'
    
    sg.data= sg._data.drop('mean', axis=1)
    
    with pytest.raises(AssertionError) as err:
        sg.aggregate_means() 
    assert 'No `mean` column' in str(err.value), 'aggregate_means() should fail if no `mean` column'


def test_region_bounds():
    sg = SoilGrids()
    sg.data= pd.DataFrame({
        'lat': {0: 8.663411, 1: 8.663411, 3: 8.663411, 10: 8.680699, 11: 8.680699, 13: 8.680699}, 
        'lon': {0: 56.323929, 1: 56.323929, 3: 56.323929, 10: 56.441106, 11: 56.441106, 13: 56.441106}, 
        'soil_property': {0: 'clay', 1: 'clay', 3: 'ocs', 10: 'clay', 11: 'clay', 13: 'ocs'}, 
        'd_factor': {0: 10, 1: 10, 3: 10, 10: 10, 11: 10, 13: 10}, 
        'mapped_units': {0: 'g/kg', 1: 'g/kg', 3: 't/ha', 10: 'g/kg', 11: 'g/kg', 13: 't/ha'}, 
        'target_units': {0: '%', 1: '%', 3: 'kg/m²', 10: '%', 11: '%', 13: 'kg/m²'}, 
        'uncertainty_unit': {0: '', 1: '', 3: '', 10: '', 11: '', 13: ''}, 
        'depth': {0: '0-5cm', 1: '5-15cm', 3: '0-30cm', 10: '0-5cm', 11: '5-15cm', 13: '0-30cm'}, 
        'top_depth': {0: 0, 1: 5, 3: 0, 10: 0, 11: 5, 13: 0}, 
        'bottom_depth': {0: 5, 1: 15, 3: 30, 10: 5, 11: 15, 13: 30}, 
        'unit_depth': {0: 'cm', 1: 'cm', 3: 'cm', 10: 'cm', 11: 'cm', 13: 'cm'}, 
        'mean': {0: 9.0, 1: 12.0, 3: 60.0, 10: 128.0, 11: 124.0, 13: 55.0}
    })
    
    assert sg.region_bounds == {'lat': (8.663411, 8.680699), 'lon': (56.323929, 56.441106)}, \
        "Region bounds should be {'lat': (8.663411, 8.680699), 'lon': (56.323929, 56.441106)}"
        