__version__ = '0.0.1'
__version_info__ = tuple([int(num) if num.isdigit() else num for num in __version__.replace('-', '.', 1).split('.')])
# Version synonym
VERSION = __version__
__author__ = 'Javier Llamas Ramirez'
__license__ = 'GNU Affero General Public License v3'
