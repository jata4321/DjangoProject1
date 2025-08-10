from nelson_siegel_svensson import NelsonSiegelSvenssonCurve
from nelson_siegel_svensson.calibrate import calibrate_ns_ols
import numpy as np

def addition(a: object, b: object, *args) -> int:
    s = sum([a, b, *args])
    return s


def nss_curve(*args:list, **kwargs: dict) -> zip:
    if args is not None:
        t = np.array(args[0])
        y= np.array(args[1])
        print(kwargs.get('y_crv'))
        calibration, status = calibrate_ns_ols(t, y)
        curve = calibration(t)
    else:
        y = NelsonSiegelSvenssonCurve(0.028, -0.02, 0.04, 0.05, 1.1, 4.0)
        t = np.linspace(0, 20, 10)
        curve = y(t)
    yield_curve = zip(curve, t)
    return yield_curve

