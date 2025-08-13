from nelson_siegel_svensson.calibrate import calibrate_nss_ols
import numpy as np
import plotly.express as px
from typing import Optional, List, Dict, Union, Any


def addition(a: object, b: object, *args) -> int:
    s = sum([a, b, *args])
    return s

def nss_constructor(t:List[float], y:List[float]):
    if t is not None and y is not None:
        t = np.array(t)
        y = np.array(y)/100
        calibration, status = calibrate_nss_ols(t, y)
        curve_t = np.linspace(0.5, 12, 100)
        curve_nss = calibration(curve_t)
        points = np.array([calibration(t_).round(6) for t_ in t])
        return curve_nss, curve_t, points
    return None

def forward_rate(t: List[float], y: List[float], period=2, *args: List[Any], **kwargs: Dict[str, Any]) -> Optional[str]:
    curve_nss, curve_t, points = nss_constructor(t, y)
    zero_rate = curve_nss[1]
    return print(zero_rate)

def nss_curve(t: List[float], y: List[float], *args: List[Any], **kwargs: Dict[str, Any]) -> Optional[str]:
    curve_nss, curve_t, points = nss_constructor(t, y)
    # if t is not None and y is not None:
    #     t = np.array(t)
        # y = np.array(y)/100
        # calibration, status = calibrate_nss_ols(t, y)
        # curve_t = np.linspace(0.5, 12, 100)
        # curve_nss = calibration(curve_t)
        # points = np.array([calibration(t_).round(6) for t_ in t])
    fig = px.scatter(template='presentation',
                     height=600)
    fig.add_scatter(x=curve_t,
                    y=curve_nss * 100,
                    mode='lines',
                    name='NSS Curve')
    fig.add_scatter(x=t,
                    y=y * 100,
                    mode='markers',
                    marker=dict(size=12, symbol='cross', opacity=0.8),
                    name='Input Points')
    fig.add_scatter(x=t,
                    y=points * 100,
                    mode='markers',
                    marker=dict(size=12, symbol='triangle-up', opacity=0.8),
                    name='Model Points')
    fig.add_bar(x=t,
                y = (np.array(y) * 100 - points * 10000),
                name='Cheap/Dear Points',
                yaxis='y2',
                opacity=0.2)
    fig.update_layout(title_text='Nelson-Siegel-Svensson Curve',
              title_font_size=29,
              title_y=0.975,
              title_x=0.5,
              xaxis_title='Years',
              yaxis_title='Yield [%]',
              yaxis2=dict(title='Spread [pb]', overlaying='y', side='right', showgrid=False),
              margin=dict(l=150, r=150),
              legend=dict(orientation='h',
                          yanchor="top",
                          xanchor="center",
                          y=1.02,
                          x=0.5,
                          bordercolor="Grey",
                          borderwidth=0.5,
                          font=dict(size=14))
                      )
    fig = fig.to_html()
    forward_rate(t, y)
    return fig



