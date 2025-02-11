# formulario/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Defina home como a view inicial
    # Adicione mais rotas conforme necessário
]