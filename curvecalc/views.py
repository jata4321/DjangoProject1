from typing import Any, Dict
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from .models import Tenor
from .forms import CurveForm, DateRangeForm
from .calculations import addition, nss_curve, forward_curve
import plotly.express as px
from datetime import datetime


class CurveFilterMixin:
    def __init__(self):
        self.request = None

    def apply_filters(self, queryset):
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        search_country = self.request.GET.get('search')

        if start_date:
            start_date = datetime.fromisoformat(start_date)
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            end_date = datetime.fromisoformat(end_date)
            queryset = queryset.filter(date__lte=end_date)
        if search_country:
            queryset = queryset.filter(type_name__country__country_name__icontains=search_country)
        return queryset


def index(request):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May']
    weights = [2, 3, 5, 3, 4]

    chart = create_bar_chart(months, weights)
    context = {'chart': chart, 'data': weights, 'labels': months}
    return render(request, 'curvecalc/index.html', context=context)


def create_bar_chart(x_values, y_values):
    fig = px.bar(
        x=x_values,
        y=y_values,
        height=500,
        template='presentation'
    )
    fig.update_layout(
        title_text='Chart',
        title_font_size=28,
        title_y=0.975,
        title_x=0.5,
        xaxis_title='Months',
        yaxis_title='Weight (kg)',
    )
    return fig.to_html()


class HomePageView(TemplateView):
    template_name = 'curvecalc/home.html'

    def get_context_data(self, *args, **kwargs):
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context['addition'] = addition(10, 25, 1, 2, 3, 4, 5)
        tenors = [0.5, 1, 2, 5, 10]
        yields = [0.027, 0.03, 0.032, 0.0365, 0.04]
        ytm_values = [0.03, 0.04, 0.045, 0.043, 0.04]

        context['labels'] = [round(float(val), 2) for val in tenors]
        context['data'] = [round(float(val), 4) for val in ytm_values]
        context['ytm'] = [round(float(val), 4) for val in yields]
        return context


class CurveListView(ListView, CurveFilterMixin):
    model = Tenor
    template_name = 'curvecalc/curve_list.html'
    paginate_by = 5
    ordering = ['-pk']

    def get_queryset(self):
        return self.apply_filters(super().get_queryset())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_form'] = DateRangeForm(self.request.GET)
        context['search'] = self.request.GET.get('search') or ""
        return context


class PartialCurveListView(CurveListView, CurveFilterMixin):
    template_name = 'curvecalc/partials/_curve_list.html'

class PartialPaginatorView(TemplateView, CurveFilterMixin):
    template_name = 'curvecalc/partials/_paginator.html'


class CurveDetailView(DetailView):
    model = Tenor
    template_name = 'curvecalc/curve_detail.html'


class BaseCurveView:
    model = Tenor
    success_url = reverse_lazy('curvecalc:curve_list')


class CurveCreateView(BaseCurveView, CreateView):
    form_class = CurveForm
    template_name = 'curvecalc/curve_create.html'


class CurveUpdateView(BaseCurveView, UpdateView):
    form_class = CurveForm
    template_name = 'curvecalc/curve_update.html'


class CurveDeleteView(BaseCurveView, DeleteView):
    template_name = 'curvecalc/curve_delete.html'


class AddCurveView(FormView):
    template_name = 'curvecalc/curve_form.html'
    form_class = CurveForm
    TENOR_MAPPING = {
        0.5: 'tenor_6m',
        1: 'tenor_1y',
        2: 'tenor_2y',
        5: 'tenor_5y',
        7: 'tenor_7y',
        10: 'tenor_10y'
    }

    def __init__(self, *args, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.cleaned = None

    def get_tenor_data(self, cleaned_data):
        return {k: cleaned_data[v] for k, v in self.TENOR_MAPPING.items()
                if cleaned_data[v] is not None}

    def form_valid(self, form):
        self.cleaned = form.cleaned_data
        data_old = {k: v for k, v in form.cleaned_data.items() if v is not None}
        data = self.get_tenor_data(self.cleaned)

        chart_nss = nss_curve(t=list(data.keys()), y=list(data.values()))
        chart_fwd = forward_curve(t=list(data.keys()), y=list(data.values()),
                                  forward_length_months=6)

        context = {
            'form': form,
            'chart_nss': chart_nss,
            'chart_fwd': chart_fwd,
            'data': data,
            'data_old': data_old
        }

        if self.request.POST.get('action') == 'save':
            form.save()

        return self.render_to_response(context)


class CurveDataView(TemplateView):
    template_name = 'curvecalc/form_data.html'
