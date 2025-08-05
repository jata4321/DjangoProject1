from typing import Tuple, Any

from nelson_siegel_svensson import NelsonSiegelSvenssonCurve
import numpy as np
from numpy import ndarray

def addition(a: object, b: object, *args) -> int:
    s = sum([a, b, *args])
    return s

def nss_curve(*kwargs):
    y = NelsonSiegelSvenssonCurve(0.028, -0.03, -0.04, -0.015, 1.1, 4.0)
    t = np.linspace(0, 20, 10)
    curve = y(t)
    yield_curve = zip(curve, t)
    return yield_curve