import pytest

import soilgrids
import pandas as pd
    
    
def test_parse_depth():
    ocs_depth = {
        "range": {"top_depth": 0, "bottom_depth": 30, "unit_depth": "cm"}, 
        "label": "0-30cm", 
        "values": {"mean": 87, "uncertainty": 10}
    }

    ocs = soilgrids.api_requests._parse_depth(ocs_depth)
    
    assert type(ocs) == pd.DataFrame,     'Parsed depth should be an instance of pandas.DataFrame'
    assert len(ocs) == 1,                 'Parsed depth should have one row'
    assert 'depth'        in ocs.columns, "Parsed depth should have a 'depth' column"
    assert 'top_depth'    in ocs.columns, "Parsed depth should have a 'top_depth' column"
    assert 'bottom_depth' in ocs.columns, "Parsed depth should have a 'bottom_depth' column"
    assert 'unit_depth'   in ocs.columns, "Parsed depth should have a 'unit_depth' column"
    assert 'mean'         in ocs.columns, "Parsed depth should have a 'mean' column"
    assert 'uncertainty'  in ocs.columns, "Parsed depth should have a 'uncertainty' column"

    
def test_parse_property():
    clay_property = {
        'name': 'clay',
        'unit_measure': {'d_factor': 10, 'mapped_units': 'g/kg', 'target_units': '%', 'uncertainty_unit': ''},
        'depths': [
            {
                'range': {'top_depth': 0, 'bottom_depth': 5,  'unit_depth': 'cm'}, 
                'label': '0-5cm',  
                'values': {'mean': 290, 'uncertainty': 30}},
            {
                'range': {'top_depth': 5, 'bottom_depth': 15, 'unit_depth': 'cm'}, 
                'label': '5-15cm', 
                'values': {'mean': 300, 'uncertainty': 20}
            }
        ] 
    }

    clay = soilgrids.api_requests._parse_property(clay_property)
    
    assert type(clay) == pd.DataFrame,         'Parsed property should be an instance of pandas.DataFrame'
    assert len(clay) == 2,                     'Parsed property should have two rows'
    assert 'soil_property'    in clay.columns, "Parsed property should have a 'soil_property' column"
    assert 'd_factor'         in clay.columns, "Parsed property should have a 'd_factor' column"
    assert 'mapped_units'     in clay.columns, "Parsed property should have a 'mapped_units' column"
    assert 'target_units'     in clay.columns, "Parsed property should have a 'target_units' column"
    assert 'uncertainty_unit' in clay.columns, "Parsed property should have a 'uncertainty_unit' column"
    assert 'depth'            in clay.columns, "Parsed property should have a 'depth' column"
    assert 'top_depth'        in clay.columns, "Parsed property should have a 'top_depth' column"
    assert 'bottom_depth'     in clay.columns, "Parsed property should have a 'bottom_depth' column"
    assert 'unit_depth'       in clay.columns, "Parsed property should have a 'unit_depth' column"
    assert 'mean'             in clay.columns, "Parsed property should have a 'mean' column"
    assert 'uncertainty'      in clay.columns, "Parsed property should have a 'uncertainty' column"


def test_parse_response():
    response = {
        'type': 'Feature',
        'geometry': {'type': 'Point', 'coordinates': [55.123123, 56.456456]},
        'properties': {
            'layers': [
                {
                    'name': 'clay',
                    'unit_measure': {'d_factor': 10, 'mapped_units': 'g/kg', 'target_units': '%', 'uncertainty_unit': ''},
                    'depths': [
                        {
                            'range': {'top_depth': 0, 'bottom_depth': 5,  'unit_depth': 'cm'}, 
                            'label': '0-5cm',  
                            'values': {'mean': 290}},
                        {
                            'range': {'top_depth': 5, 'bottom_depth': 15, 'unit_depth': 'cm'}, 
                            'label': '5-15cm', 
                            'values': {'mean': 300}
                        }
                    ] 
                },
                {
                    'name': 'ocs',
                    'unit_measure': {'d_factor': 10, 'mapped_units': 't/ha', 'target_units': 'kg/m²', 'uncertainty_unit': ''},
                    'depths': [
                        {
                            'range': {'top_depth': 0, 'bottom_depth': 30, 'unit_depth': 'cm'}, 
                            'label': '0-30cm', 
                            'values': {'mean': 87}
                        }
                    ]
                }
            ]
        },
        'query_time_s': 0.8,
    }

    parsed = soilgrids.api_requests._parse_response(response)
    
    assert type(parsed) == pd.DataFrame, 'Parsed response should be an instance of pandas.DataFrame'
    
    # This one's more complex, so it's easiest to just check against the expected output
    expected = pd.DataFrame({
        'lat': {0: 56.456456, 1: 56.456456, 2: 56.456456}, 
        'lon': {0: 55.123123, 1: 55.123123, 2: 55.123123}, 
        'soil_property': {0: 'clay', 1: 'clay', 2: 'ocs'}, 
        'd_factor': {0: 10, 1: 10, 2: 10}, 
        'mapped_units': {0: 'g/kg', 1: 'g/kg', 2: 't/ha'}, 
        'target_units': {0: '%', 1: '%', 2: 'kg/m²'}, 
        'uncertainty_unit': {0: '', 1: '', 2: ''}, 
        'depth': {0: '0-5cm', 1: '5-15cm', 2: '0-30cm'}, 
        'top_depth': {0: 0, 1: 5, 2: 0}, 
        'bottom_depth': {0: 5, 1: 15, 2: 30}, 
        'unit_depth': {0: 'cm', 1: 'cm', 2: 'cm'}, 
        'mean': {0: 290, 1: 300, 2: 87}
    })

    assert parsed.equals(expected), 'Parsed response does not match the expected output'
