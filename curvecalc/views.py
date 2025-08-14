from typing import Any
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from .models import Tenor
from .forms import CurveForm
from .calculations import addition, nss_curve, forward_curve
import plotly.express as px
from itertools import islice

# Create your views here.

def index(request):

    x = ['sty', 'lut', 'mar', 'kwi', 'lip']
    y = [2, 3, 5, 3, 4]

    fig = px.bar(x=x,
                 y=y,
                 height=500,
                 template='presentation',
                 )
    fig.update_layout(title_text='Wykres',
                      title_font_size=28,
                      title_y=0.975,
                      title_x=0.5,
                      xaxis_title='Miesiące',
                      yaxis_title='Waga (kg)',
                      )
    chart = fig.to_html()
    context = {'chart': chart, 'data': y, 'labels': x}

    return render(request, 'curvecalc/index.html', context=context)

class HomePageView(TemplateView):
    template_name = 'curvecalc/home.html'

    def get_context_data(self, *args, **kwargs):
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context['addition'] = addition(10, 25, 1,2,3,4,5)
        ytm, y, t = zip(*nss_curve([0.5,1,2,5,10], [0.027,0.03,0.032,0.0365,0.04], y_crv={1:0.03, 5:0.035, 10:0.04}))
        context['labels'] =[round(float(val),2) for val in t]
        context['data'] = [round(float(val),4) for val in ytm]
        context['ytm'] = [round(float(val),4) for val in y]
        return context

class CurveListView(ListView):
    model = Tenor
    template_name = 'curvecalc/curve_list.html'
    paginate_by = 5
    ordering = ['-id']

class CurveDetailView(DetailView):
    model = Tenor
    template_name = 'curvecalc/curve_detail.html'

class CurveCreateView(CreateView):
    model = Tenor
    form_class = CurveForm
    template_name = 'curvecalc/curve_create.html'
    success_url = '/curvecalc/listview/'

class CurveUpdateView(UpdateView):
    model = Tenor
    form_class = CurveForm
    template_name = 'curvecalc/curve_update.html'
    success_url = '/curvecalc/listview/'

class CurveDeleteView(DeleteView):
    model = Tenor
    template_name = 'curvecalc/curve_delete.html'
    success_url = '/curvecalc/listview/'

class AddCurveView(FormView):
    template_name = 'curvecalc/curve_form.html'
    form_class = CurveForm

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.cleaned = None

    def form_valid(self, form):
        self.cleaned = form.cleaned_data
        data = { 0.5: self.cleaned['tenor_6m'],
            1: self.cleaned['tenor_1y'],
            2: self.cleaned['tenor_2y'],
            5: self.cleaned['tenor_5y'],
            7: self.cleaned['tenor_7y'],
            10: self.cleaned['tenor_10y']}
        data = {k: v for k, v in data.items() if v is not None}
        chart_nss = nss_curve(t=list(data.keys()), y=list(data.values()))
        chart_fwd = forward_curve(t=list(data.keys()), y=list(data.values()), forward_length_months=12)
        context = {'form': form, 'chart_nss': chart_nss, 'chart_fwd':chart_fwd, 'data': data}
        return self.render_to_response(context)


class CurveDataView(TemplateView):
    template_name = 'curvecalc/form_data.html'
