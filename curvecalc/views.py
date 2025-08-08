from typing import Any
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Tenor
from .forms import CurveForm
from .calculations import addition, nss_curve
import plotly.express as px

# Create your views here.
def index(request):

    x = ['sty', 'lut', 'mar', 'kwi', 'lip']
    y = [2, 3, 5, 3, 4]

    fig = px.bar(x=x,
                 y=y,
                 height=600,
                 template='ggplot2',
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

    def get_context_data(self, **kwargs):
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context['addition'] = addition(10, 25, 1,2,3,4,5)
        ytm, t = zip(*nss_curve())
        context['labels'] =[round(float(val),2) for val in t]
        context['data'] = [round(float(val),4) for val in ytm]
        return context

class CurveListView(ListView):
    model = Tenor
    template_name = 'curvecalc/curve_list.html'
    paginate_by = 5

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
