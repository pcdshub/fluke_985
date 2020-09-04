from ._version import get_versions
from .data import load_fluke_data_file
from .ioc import Fluke985Base, create_ioc

__version__ = get_versions()['version']
del get_versions

__all__ = ['load_fluke_data_file', 'create_ioc', 'Fluke985Base']
