# formulario/models.py

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Categoria(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome

class Avaliacao(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    relevancia_pessoal = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    curiosidade_intelectual = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    disponibilidade_recursos = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    prazer_participacao = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    impacto_vida_diaria = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    objetivos_crescimento = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    novidade_variedade = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def calcular_pontuacao_total(self):
        # Pesos sugeridos das métricas
        pesos = {
            'relevancia_pessoal': 0.25,
            'curiosidade_intelectual': 0.10,
            'disponibilidade_recursos': 0.10,
            'prazer_participacao': 0.15,
            'impacto_vida_diaria': 0.15,
            'objetivos_crescimento': 0.15,
            'novidade_variedade': 0.10,
        }
        total = (
            self.relevancia_pessoal * pesos['relevancia_pessoal'] +
            self.curiosidade_intelectual * pesos['curiosidade_intelectual'] +
            self.disponibilidade_recursos * pesos['disponibilidade_recursos'] + 
            self.prazer_participacao * pesos['prazer_participacao'] +
            self.impacto_vida_diaria * pesos['impacto_vida_diaria'] +
            self.objetivos_crescimento * pesos['objetivos_crescimento'] +
            self.novidade_variedade * pesos['novidade_variedade']
        )
        return total