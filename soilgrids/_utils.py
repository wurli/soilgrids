import logging
import subprocess
import time
import importlib.resources

_logger = logging.getLogger("soilgrids")

def _check_arg(arg, name, allowed_vals):
    """Check that a function argument is either None or a subset of allowed_vals."""
    
    if arg in [None, []]:
        return allowed_vals
    
    if isinstance(arg, str):
        arg = [arg]
    
    # Worth checking this before sending a request, both to avoid unnecessary
    # load on Soilgrids and to provide a quicker error with a more helpful
    # message in the event that an argument is invalid
    assert set(arg) <= set(allowed_vals), \
        "Invalid `{}`. \n  i: Check '{}'. \n  i: Allowed values are: '{}'.".format(
            name, 
            "', '".join(set(arg) - set(allowed_vals)),
            "', '".join(allowed_vals)
        )
    
    return arg

def _to_list(x):
    """Convert a scalar to a list, or leave a list unchanged."""
    try:
        iter(x)
    except TypeError:
        x = [x]
    return x

class _Throttle():
    """Sleep for a specified minimum interval between calls"""
    
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
            _logger.info(f"Waiting {time_to_wait:.1f}s before next request...")
            time.sleep(time_to_wait)
            
        self.last_request_time = time.time()


def _rscript(script, *args):
    """Run `Rscript script.R arg1 arg2 arg3...` and return the printed output.""" 
    _check_r_available()
    
    res = subprocess.run(
        ['rscript', _pkg_file(script), *args], 
        capture_output=True
    )
    
    if res.returncode != 0:
        raise RuntimeError(
            f'R script failed with exit code {res.returncode}.\n' \
            f'  i: Check the R script at {script}.\n' \
            f'  i: Check the arguments: {args}\n' \
            f'  i: Check the error returned by R: {res.stderr.decode('utf-8')}.\n'
        )
    
    return res.stdout.decode('utf-8')


def _check_r_available():
    """Check that R can be called from Python."""
    if not _r_available():
        raise RuntimeError(
            "No R installation detected\n" \
            "  i: Make sure your R installation can be found on the PATH"
        )


def _r_available():
    """Check that R can be called from Python.""" 
    cmd = ['rscript', '-e', 'R.version']
    return subprocess.run(cmd, capture_output=True).returncode == 0


def _pkg_file(path):
    """Ensure paths to resources work regardless of how the package is installed."""
    path = importlib.resources \
        .files('soilgrids') \
        .joinpath(path)
    return str(path)
