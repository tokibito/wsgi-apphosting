import os
import sys
import unittest

from tests.runapp import *
from tests.config import *

if __name__ == '__main__':
    BASE_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))
    if not BASE_DIR in sys.path:
        sys.path.append(BASE_DIR)
    unittest.main()
