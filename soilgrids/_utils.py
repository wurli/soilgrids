import time

def check_arg(arg, name, allowed_vals):
    # Check that a function argument is either None or a subset of allowed_vals
    
    if arg is None:
        return allowed_vals
    
    if isinstance(arg, str):
        arg = [arg]
    
    # Worth checking this before sending a request, both to avoid unnecessary
    # load on Soilgrids and to provide a quicker error with a more helpful
    # message in the event that an argument is invalid
    assert set(arg) <= set(allowed_vals), \
        'Invalid `{}`. \n  i: Check "{}". \n  i: Allowed values are: "{}".'.format(
            name, 
            '", "'.join(set(arg) - set(allowed_vals)),
            '", "'.join(allowed_vals)
        )
    
    return arg

def to_list(x):
    try:
        iter(x)
    except TypeError:
        x = [x]
    return x

class Throttle():
    # An object that sleeps for a specified minimum interval between calls
    
    def __init__(self, interval=5):
        self.interval = interval
        self.last_request_time = None
        
    def __call__(self):
        if self.last_request_time is None:
            self.last_request = time.time()
        else:
            time_since_last_request = time.time() - self.last_request_time
            time_to_wait = self.interval - time_since_last_request
            if time_to_wait > 0:
                print(f"Waiting {time_to_wait:.1f}s before next request")
                time.sleep(time_to_wait)
            self.last_request = time.time()

