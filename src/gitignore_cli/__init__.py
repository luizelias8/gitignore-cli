from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version('gitignore-cli')
except PackageNotFoundError:
    __version__ = 'unknown'
