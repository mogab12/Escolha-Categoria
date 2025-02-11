# formulario/forms.py

from django import forms
from .models import Avaliacao

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        CHOICES = [(i, str(i)) for i in range(1, 6)]
        model = Avaliacao
        exclude = ['categoria']
        widgets = {
            'relevancia_pessoal': forms.RadioSelect(choices=CHOICES),
            'curiosidade_intelectual': forms.RadioSelect(choices=CHOICES),
            'disponibilidade_recursos': forms.RadioSelect(choices=CHOICES),
            'prazer_participacao': forms.RadioSelect(choices=CHOICES),
            'impacto_vida_diaria': forms.RadioSelect(choices=CHOICES),
            'objetivos_crescimento': forms.RadioSelect(choices=CHOICES),
            'novidade_variedade': forms.RadioSelect(choices=CHOICES),
        }