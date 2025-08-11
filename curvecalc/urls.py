from django.urls import path
from . import views

app_name = 'curvecalc'

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.HomePageView.as_view(), name='home'),
    path('listview/', views.CurveListView.as_view(), name='curve_list'),
    path('detailview/<int:pk>/', views.CurveDetailView.as_view(), name='curve_detail'),
    path('createview/', views.CurveCreateView.as_view(), name='curve_create'),
    path('updateview/<int:pk>/', views.CurveUpdateView.as_view(), name='curve_update'),
    path('deleteview/<int:pk>/delete/', views.CurveDeleteView.as_view(), name='curve_delete'),
    path('formview/', views.AddCurveView.as_view(), name='curve_form'),
]