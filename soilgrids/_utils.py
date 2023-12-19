import importlib.resources
import logging
import subprocess
import time
import numpy as np
import pandas as pd
import os
import shutil
import glob

_logger = logging.getLogger('soilgrids')

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


def _to_vector(x):
    """Convert a scalar to a vector, or leave a vector unchanged."""
    scalars = [str, int, float, bool, type(None)]
    vectors = [list, np.ndarray, pd.Series]
    if any([isinstance(x, t) for t in scalars]):
        return [x]
    if any([isinstance(x, t) for t in vectors]):
        return x
    raise TypeError(f'Cannot convert {type(x)} to vector')
    


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
            _logger.info(f'Waiting {time_to_wait:.1f}s before next request...')
            time.sleep(time_to_wait)
            
        self.last_request_time = time.time()


def _rscript(script, *args):
    """Run `rscript script.R arg1 arg2 arg3...` and return the printed output.""" 
    
    res = subprocess.run(
        [_find_rscript_binary(), _pkg_file(script), *args], 
        capture_output=True
    )
    
    if res.returncode != 0:
        args_escaped = [arg.encode('unicode_escape').decode('utf-8') for arg in args]
        args_bullets = [f'* Arg {i+1}: `{arg}`' for i, arg in enumerate(args_escaped)]
        args_trunc   = [arg if len(arg) <= 80 else arg[:77] + '...' for arg in args_bullets]
        args_pretty  = '\n     '.join(args_trunc)
        
        raise RuntimeError(
            f'R script failed with exit code {res.returncode}.\n' \
            f'  i: Check the R script at {script}.\n' \
            f'  i: Check the arguments:\n' \
            f'     {args_pretty}\n' \
            f'  i: Check the error returned by R: \n' \
            f'     {res.stderr.decode("utf-8")}.'
        )
    
    return res.stdout.decode('utf-8')


def _find_rscript_binary():
    """Attempt to find the binary for Rscript.

    It's reasonable to assume the Rscript binary will be on the PATH, but in
    practice this seems to rarely be the case. If the binary isn't present, it's 
    worth checking a few common locations before asking the user to start 
    fiddling with their system variables. NB, the design of this function was 
    influenced by some research into how RStudio finds the R executable, since 
    it does so quite reliably, even when R is not on the PATH.
    """
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # 01: Check for Rscript on the PATH
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    r_path = shutil.which('Rscript')
    if r_path is not None:
        return os.path.abspath(r_path)
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # 02: Check using the R_HOME environment variable
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    r_home = os.environ.get('R_HOME')
    if r_home is not None:
        r_binary = os.path.join(r_home, 'bin', 'Rscript')
        if os.path.exists(r_binary):
            return os.path.abspath(r_binary)
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # 03: Check common installation directories for an executable
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    common_directories = [
        'opt/local/bin/Rscript',                  # macOS standard location
        '/Library/Frameworks/' \
            'R.framework/Versions/current/' \
            'Resources/bin/Rscript',              # Common alternative on macOS
        '/usr/bin/Rscript',                       # Linux standard location
        '/usr/local/bin/Rscript',                 # Common alternative on Linux
        'opt/bin/Rscript',                        # Common alternative on Linux
        'C:/Program Files/R/R-*/bin/Rscript.exe', # Windows
    ]

    for directory in common_directories:
        files = glob.glob(directory)
        if len(files) > 0:
            # Max returns the executable for the most up-to-date R version, e.g.
            # in on Windows when we might get: 
            #     'C:/Program Files/R/R-4.2.0/bin/Rscript.exe' 
            # and 'C:/Program Files/R/R-3.6.0/bin/Rscript.exe'
            return os.path.abspath(max(files))
        
    raise FileNotFoundError(
        "Could not find Rscript binary.\n" +
        "  i: Make sure R is installed.\n" +
        "  i: If R is installed, make sure Rscript is on the PATH."
    )


def _pkg_file(path):
    """Ensure paths to resources work regardless of how the package is installed."""
    path = importlib.resources \
        .files('soilgrids') \
        .joinpath(path)
    
    if not path.exists():
        raise FileNotFoundError(f'File not found: {path}')    
    
    return str(path)


def _rescale(x, a=0, b=1):
    """Rescale an array to fall within [a, b]"""
    xmax, xmin = x.max(), x.min()
    return a + (x - xmin) * (b - a) / (xmax - xmin)
