from ._version import get_versions
from .data import load_fluke_data_file

__version__ = get_versions()['version']
del get_versions

__all__ = ['load_fluke_data_file']
