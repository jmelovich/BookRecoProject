# this is a test file used to demonstrate how to import methods from other py files
import ctypes
import os

# Load the shared library
lib_path = os.path.join(os.path.dirname(__file__), 'functions/add_numbers')
if os.name == 'nt':  # Windows
    lib_path += '.dll'
else:  # Unix-like systems
    lib_path += '.so'

add_lib = ctypes.CDLL(lib_path)

# Define the function signature
add_lib.add_numbers.argtypes = [ctypes.c_double, ctypes.c_double]
add_lib.add_numbers.restype = ctypes.c_double

def add_numbers(a, b):
    try:
        return add_lib.add_numbers(float(a), float(b))
    except ValueError:
        return "Error: Invalid input"