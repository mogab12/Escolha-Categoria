from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Usuario(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome

class Categoria(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome

class Avaliacao(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True)
    categoria = models.CharField(max_length=100)
    relevancia_pessoal = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    curiosidade_intelectual = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    disponibilidade_recursos = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    prazer_participacao = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    impacto_vida_diaria = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    objetivos_crescimento = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    novidade_variedade = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    pontuacao_total = models.FloatField(default=0)

    def calcular_pontuacao_total(self):
        pesos = {
            'relevancia_pessoal': 0.25,
            'curiosidade_intelectual': 0.10,
            'disponibilidade_recursos': 0.10,
            'prazer_participacao': 0.15,
            'impacto_vida_diaria': 0.15,
            'objetivos_crescimento': 0.15,
            'novidade_variedade': 0.10,
        }
        total = sum(getattr(self, campo) * peso for campo, peso in pesos.items())
        self.pontuacao_total = total
        self.save()
        return total