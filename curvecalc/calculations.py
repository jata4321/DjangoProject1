from nelson_siegel_svensson import NelsonSiegelSvenssonCurve
from nelson_siegel_svensson.calibrate import calibrate_nss_ols
import numpy as np
import plotly.express as px
from typing import Optional, List, Dict, Union, Any


def addition(a: object, b: object, *args) -> int:
    s = sum([a, b, *args])
    return s


def nss_curve(t: List[float], y: List[float], *args: List[Any], **kwargs: Dict[str, Any]) -> Optional[str]:
    if t is not None and y is not None:
        t = np.array(t)
        y = np.array(y)/100
        calibration, status = calibrate_nss_ols(t, y)
        curve_t = np.linspace(0.5, 12, 100)
        curve_nss = calibration(curve_t)

        fig = px.scatter(template='presentation',
                         height=500)
        fig.add_scatter(x=curve_t,
                        y=curve_nss * 100,
                        mode='lines',
                        name='NSS Curve')
        fig.add_scatter(x=t,
                        y=y * 100,
                        mode='markers',
                        marker=dict(size=12, symbol='cross', opacity=0.8),
                        name='Input Points')
        fig.update_layout(title_text='Nelson-Siegel-Svensson Curve',
                          title_font_size=28,
                          title_y=0.975,
                          title_x=0.5,
                          xaxis_title='Years',
                          yaxis_title='Yield [%]', )
        fig = fig.to_html()
        return fig
    return None
    # else:
    #     y = NelsonSiegelSvenssonCurve(0.028, -0.02, 0.04, 0.05, 1.1, 4.0)
    #     t = np.linspace(0, 20, 10)
    #     curve = y(t)
    # yield_curve = zip(curve, y, t)

