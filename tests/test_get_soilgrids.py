import pytest

import soilgrids
from urllib import request

# NB, get_soilgrids() itself isn't tested as its logic is pretty simple. 
# The sub-functions it calls are tested below and in other files.


def test_query_soilgrids():
    try:
        request.urlopen('http://google.com', timeout=1)
    except request.URLError: 
        pytest.skip('No internet connection')
        
    resp = soilgrids.api_requests._query_soilgrids(
        50, 60,
        soil_property=['clay', 'ocs'],
        depth=['0-5cm', '0-30cm'],
        value=['mean', 'uncertainty']
    )
    
    # Note that [lat, lon] are returned in order [lon, lat]
    assert resp['geometry']['coordinates'] == [60, 50], 'Response should be for lat=50, lon=60'
    
    returned_properties = [p['name'] for p in resp['properties']['layers']]
    assert set(returned_properties) == {'clay', 'ocs'}, 'Response should include properties clay and ocs'
    
    returned_depths = [d['label'] for p in resp['properties']['layers'] for d in p['depths']]
    assert set(returned_depths) == {'0-5cm', '0-30cm'}, 'Response should include depths 0-5cm and 0-30cm'
    
    returned_values = [v for p in resp['properties']['layers'] for d in p['depths'] for v in d['values']]
    assert set(returned_values) == {'mean', 'uncertainty'}, 'Response should include values mean and uncertainty'
    
    