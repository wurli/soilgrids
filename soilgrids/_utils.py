import logging
import platform
import subprocess
import time

logger = logging.getLogger("soilgrids")

def check_arg(arg, name, allowed_vals):
    """Check that a function argument is either None or a subset of allowed_vals."""
    
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
    """Convert a scalar to a list, or leave a list unchanged."""
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
            self.last_request_time = time.time()
            return
        
        time_since_last_request = time.time() - self.last_request_time
        time_to_wait = self.interval - time_since_last_request
        
        if time_to_wait > 0:
            logger.info(f"Waiting {time_to_wait:.1f}s before next request...")
            time.sleep(time_to_wait)
            
        self.last_request_time = time.time()


def check_r_available():
    """Check that R is installed and available on the PATH."""
    cmd = 'where' if platform.system() == 'Windows' else 'which'
    try:
        subprocess.check_output([cmd, 'r'])
    except subprocess.CalledProcessError:
        raise RuntimeError(
            "No R installation detected\n" \
            "  i: Make sure your R installation can be found on the PATH"
        )

def rscript(script, *args):
    """Run `Rscript script.R arg1 arg2 arg3...` and return the printed output.""" 
    check_r_available()
    
    try:
        return subprocess.run(['rscript', script, *args], text=True, check=True)
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            f"R script failed with exit code {exc.returncode}.\n" \
            f"  i: Check the R script at {script}.\n" \
            f"  i: Check the arguments: {args}"
        )


