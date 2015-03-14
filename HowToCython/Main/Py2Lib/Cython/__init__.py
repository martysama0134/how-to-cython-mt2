import os
import sys

# Make sure we import the right Cython
cythonpath, _ = os.path.split(os.path.realpath(__file__))
sys.path.insert(0, cythonpath + "\\..")

from Cython.Shadow import __version__

# Void cython.* directives (for case insensitive operating systems).
from Cython.Shadow import *
