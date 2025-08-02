from django.urls import path
from . import views

app_name = 'portcalc'

urlpatterns = [
    path('', views.index, name='index'),
]
