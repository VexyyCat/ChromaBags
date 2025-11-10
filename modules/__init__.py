"""
Paquete de módulos para ChromaBags
"""

from .modcatal import (
    CatalogosManager,
    Color,
    Diseno,
    Material,
    ProductoTerminado
)

from .modboldis import (
    DisenoModelosManager,
    ModeloBolsa,
    Combinacion,
    CombinacionDetallada
)

__all__ = [
    'CatalogosManager',
    'Color',
    'Diseno',
    'Material',
    'ProductoTerminado',
    'DisenoModelosManager',
    'ModeloBolsa',
    'Combinacion',
    'CombinacionDetallada'
]

__version__ = '2.0.0'
__author__ = 'ChromaBags Development Team'