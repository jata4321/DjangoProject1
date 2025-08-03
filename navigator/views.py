from django.shortcuts import render
from bokeh.plotting import figure, show
from bokeh.resources import CDN
from bokeh.embed import file_html


# Create your views here.
def index(request):

    x = ['sty', 'lut', 'mar', 'kwi']
    y = [4, 3, 5, 3]

    fig = figure(height=500, width=500,
                 title="My first plot",
                 title_location="above",
                 x_axis_label="x", y_axis_label="y")
    fig.line([1,2,3,4], [1,4,9,16])
    chart = file_html(fig, CDN, title="My first plot")
    context = {'chart': chart, 'data': y, 'labels': x}

    return render(request, 'navigator/index.html', context=context)