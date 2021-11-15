import re
import os

from setuptools import setup, find_packages

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


version = get_version('dpl')

setup(
    name='dpl-cli',
    version=version,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests==2.26.0',
        'boto3==1.20.5',
        'mysqlclient==2.0.2',
        'click==8.0.3',
    ],
    entry_points={
        'console_scripts': [
            'dpl=dpl.cli:main',
        ],
    },
)
