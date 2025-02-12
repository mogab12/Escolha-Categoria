# formulario/forms.py

from django import forms
from .models import Avaliacao, Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome']

class AvaliacaoForm(forms.ModelForm):
    CHOICES = [(str(i), str(i)) for i in range(1, 6)]

    relevancia_pessoal = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    curiosidade_intelectual = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    disponibilidade_recursos = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    prazer_participacao = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    impacto_vida_diaria = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    objetivos_crescimento = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    novidade_variedade = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Avaliacao
        exclude = ['categoria', 'usuario', 'pontuacao_total']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.ChoiceField):
                field.choices = [(str(i), str(i)) for i in range(1, 6)]