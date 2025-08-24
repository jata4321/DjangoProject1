from django.urls import path
from . import views

app_name = 'navigator'

urlpatterns = [
    # Fulls:
    path('', views.index, name='index'),

    # Partials:
    path('partial-index/', views.partial_index, name='_index'),
]
