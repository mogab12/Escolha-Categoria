# formulario/views.py

from django.shortcuts import render

def home(request):
    return render(request, 'formulario/home.html')