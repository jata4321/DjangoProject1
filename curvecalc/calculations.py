from nelson_siegel_svensson.calibrate import calibrate_nss_ols
from nelson_siegel_svensson.ns import NelsonSiegelCurve
import numpy as np
import plotly.express as px
from typing import Optional, List, Dict, Union, Any


def addition(a: object, b: object, *args) -> int:
    s = sum([a, b, *args])
    return s

def nss_calibrator(t:List[float], y:List[float]):
    if t is not None and y is not None:
        t = np.asarray(t)
        y = np.asarray(y)/100
        calibration, status = calibrate_nss_ols(t, y)
        return calibration
    return None


def nss_constructor(calibration, t:List[float]):
    curve_t = np.linspace(0.5, 12, 100)
    curve_nss = calibration(curve_t)
    points = np.asarray([calibration(_).round(5) for _ in t])
    return curve_nss, curve_t, points

def forward_curve(t: List[float], y: List[float], forward_length_months=3, *args: List[Any], **kwargs: Dict[str, Any]) -> Optional[str]:
    calibration = nss_calibrator(t, y)
    start_date = t[0]
    end_date = t[-1]
    forward_length = forward_length_months / 12
    forward_dates = np.asarray(np.arange(start_date, end_date, forward_length))
    zero_rates = np.asarray(calibration(forward_dates))
    discount_factors = (1+zero_rates)**(-forward_dates)
    forward_annual = np.power(discount_factors[:-1] / discount_factors[1:], 1 / forward_length)-1

    fig = px.line(template='presentation',
                  markers=True,
                  height=600)
    fig.add_scatter(x=forward_dates[:-1],
                    y=forward_annual * 100,
                    mode='lines+markers',
                    name='Forward Curve')
    fig.add_bar(x=forward_dates[:-1],
                y=((forward_annual - forward_annual[0])*10000).round(1),
                name='Forward Spread',
                yaxis='y2',
                opacity=0.3)
    fig.update_layout(title_text=f'{ forward_length_months }m Forward Curve',
                      title_font_size=29,
                      xaxis_title='Years',
                      yaxis_title='Yield p.a. [%]',
                      yaxis2=dict(title='Spread p.a. [b.p]', overlaying='y', side='right', showgrid=False, ),
                      margin=dict(l=150, r=150),
                      legend=dict(orientation='h',
                                  yanchor="top",
                                  xanchor="center",
                                  y=1.02,
                                  x=0.5,
                                  bordercolor="Grey",
                                  borderwidth=0.5,
                                  font=dict(size=14)))
    fig_fwd = fig.to_html()
    return fig_fwd

def nss_curve(t: List[float], y: List[float], *args: List[Any], **kwargs: Dict[str, Any]) -> Optional[str]:

    calibration = nss_calibrator(t, y)
    curve_nss, curve_t, points = nss_constructor(calibration=calibration, t=t)
    forward_curve(t,y,6)

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
    fig_nss = fig.to_html()
    return fig_nss



