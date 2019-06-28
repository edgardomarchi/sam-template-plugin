from pkg_resources import get_distribution, DistributionNotFound

try:
    __version__ = get_distribution('{{cookiecutter.plugin_name}}').version
except DistributionNotFound:
    __version__ = '(local)'
