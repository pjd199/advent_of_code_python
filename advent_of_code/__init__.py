"""Nothing to initialise for this package."""
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("advent_of_code_solver")
except PackageNotFoundError: # pragma: no cover
    __version__ = "uninstalled"
