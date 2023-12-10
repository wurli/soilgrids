import requests
import time
import pandas as pd
import numpy as np

from ._utils import Throttle, check_arg, to_list


def get_soilgrids(lat, lon, *, property=None, depth=None, value=None):
    """_summary_

    Args:
        lat (_type_): _description_
        lon (_type_): _description_
        property (_type_, optional): _description_. Defaults to None.
        depth (_type_, optional): _description_. Defaults to None.
        value (_type_, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """
    
    # Allow mixing and and matching of scalars and arrays for lat and lon
    lat, lon = np.broadcast_arrays(to_list(lat), to_list(lon))
    
    # NB, the following checks might seem over-zealous, but they're worth it to 
    # avoid burdensome requests to Soilgrids, if not to provide better error 
    # messages to the user.
    assert np.array(np.abs(lat) <= 90).all(), \
        "Invalid `lat`. \n  i: Check `lat` is in the range [-90, 90]."
    
    assert np.array(np.abs(lon) <= 180).all(), \
        "Invalid `lon`. \n  i: Check `lon` is in the range [-180, 180]."
    
    property = check_arg(property, name="property", allowed_vals=[
        'bdod', 'cec', 'cfvo', 'clay', 'nitrogen', 'ocd', 'ocs', 'phh2o', 
        'sand', 'silt', 'soc', 'wv0010', 'wv0033', 'wv1500'
    ])
    depth = check_arg(depth, name="depth", allowed_vals=[
        '0-5cm', '0-30cm', '5-15cm', '15-30cm', '30-60cm', '60-100cm', 
        '100-200cm'
    ])
    value = check_arg(value, name="value", allowed_vals=[
        'Q0.5', 'Q0.05', 'Q0.95', 'mean', 'uncertainty'
    ])
    
    results = [
        _query_soilgrids(
            lat, lon, 
            property=property, 
            depth=depth, 
            value=value
        )
        for lat, lon in zip(lat, lon)
    ]
        
    return pd.concat([_parse_response(r) for r in results])
    
    

_throttle_requests = Throttle(5)
_base_url = 'https://rest.isric.org/soilgrids/v2.0/'    
    
def _query_soilgrids(lat, lon, property=None, depth=None, value=None):
    # Perform the actual API request, with some basic handling for 429 errors
    
    _throttle_requests()
    
    def perform_request():
        return requests.get(
            _base_url + 'properties/query',
            params={
                'lat': lat, 
                'lon': lon, 
                'property': property,
                'depth': depth,
                'value': value
            },
            headers={'accept': 'application/geojson'}
        )
    
    resp = perform_request()
    
    if resp.status_code == 429:
        print("429: Too Many Requests")
        print("  Waiting 60s before retrying...")
        time.sleep(60)
        resp = perform_request()
    
    # Raise anything but a 200 response as an exception
    resp.raise_for_status()
    
    return resp.json()



def _parse_response(x):
    # Parse the full geojson response from _query_soilgrids() into a DataFrame
    
    # Should both be scalars
    lat, lon = x["geometry"]["coordinates"]    
    
    layers = pd.concat([_parse_property(l) for l in x["properties"]["layers"]])
    
    layers.insert(0, "lon", lon)
    layers.insert(0, "lat", lat)   
    
    layers.reset_index(drop=True, inplace=True)
    
    return layers



def _parse_property(x):
    # Parse a single property/layer from the geojson response of 
    # _query_soilgrids() into a DataFrame
    
    # Should be <=1 row
    unit_measures = pd.DataFrame({
        "property": [x["name"]],
        **x["unit_measure"]
    })
    
    # Should be <=1 row per depth, <=1 col per value
    depths = pd.concat([_parse_depth(d) for d in x["depths"]])
    
    return pd.DataFrame.merge(unit_measures, depths, how='cross')



def _parse_depth(x):
    # Parse a single depth from a single property from the geojson response of
    # _query_soilgrids() into a DataFrame
    
    return pd.DataFrame({
        "depth": [x["label"]], 
        **x["range"], 
        **x["values"]
    })

