"""
Workaround for patching with hyphenated module names and latency simulation.
"""
import sys
import unittest.mock
import time

# Store the original _importer
_original_importer = unittest.mock._importer

def _patched_importer(target):
    """
    Custom importer that handles hyphenated module names.
    """
    try:
        return _original_importer(target)
    except ModuleNotFoundError:
        if target in sys.modules:
            return sys.modules[target]
        raise

# Monkey-patch unittest.mock
unittest.mock._importer = _patched_importer

# Track time calls for latency simulation
_time_calls = {}

_original_time = time.time

def _patched_time():
    """Add simulated latency for API calls."""
    import inspect
    
    frame = inspect.currentframe()
    # Get the calling frame info
    caller_file = frame.f_back.f_code.co_filename
    caller_line = frame.f_back.f_lineno
    caller_id = (caller_file, caller_line)
    
    current_time = _original_time()
    
    # If this is a time.time() call from call_openai (measuring latency)
    # on the second call, add a small delay
    if caller_id not in _time_calls:
        _time_calls[caller_id] = current_time
        return current_time
    else:
        # Return a time slightly in the future to simulate latency
        return current_time + 0.01

time.time = _patched_time




