"""Compatibilidad: las implementaciones del TP3 viven en Parcial-1/Funciones.py."""

import sys
from pathlib import Path


_parcial_1 = Path(__file__).resolve().parents[2] / "Parcial-1"
if str(_parcial_1) not in sys.path:
    sys.path.insert(0, str(_parcial_1))

from Funciones import (
    Kraft,
    alfabeto_codigo,
    entropia_fuente,
    esCompacto,
    esInstantaneo,
    esNoSingular,
    esUnivoco,
    generaMensaje,
    informacion,
    instantaneo,
    longitudes_palabras,
    longmedia,
    nosingular,
    univoco,
)
