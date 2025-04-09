from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('graphic/', views.graphic, name='graphic'),
    path('get_data/', views.get_data, name='get_data'),
]
