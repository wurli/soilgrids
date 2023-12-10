import logging
from .SoilGrids     import SoilGrids
from .get_soilgrids import get_soilgrids

logging.basicConfig(level=logging.INFO, format='%(message)s')

__all__ = [
    'SoilGrids',
    'get_soilgrids',
]
