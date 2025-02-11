# formulario/urls.py

from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('', lambda request: redirect('avaliar', categoria_id=1)),  # Redirecionar para avaliação da primeira categoria
    path('avaliar/<int:categoria_id>/', views.avaliar, name='avaliar'),
    path('results/', views.results, name='results'),  # Certifique-se da wine 'results' view existir.
]