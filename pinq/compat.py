"""
pinq.compat
~~~~~~~~~~~
"""

from collections import defaultdict, Iterable
from functools import reduce
from itertools import chain, dropwhile, groupby, islice, takewhile, tee
from operator import eq

try:
    from functools import lru_cache
except ImportError:
    def lru_cache(maxsize=128, typed=False):
        """A default decorator if lru_cache does not exist."""
        return lambda f: f

try:
    from itertools import zip_longest
except ImportError:
    from itertools import izip_longest as zip_longest
