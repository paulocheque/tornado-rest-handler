import sys
if sys.version_info[0] == 2:
    from trh import *
else:
    from .trh import *

VERSION = '0.0.7'