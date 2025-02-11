# formulario/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('avaliar/<int:categoria_id>/', views.avaliar, name='avaliar'),
    path('results/', views.results, name='results'),
]