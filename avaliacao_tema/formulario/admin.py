from django.contrib import admin, messages
from django.db.models import Avg
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Usuario, Avaliacao, Categoria

# Função de ação personalizada
def recalcular_pontuacoes(modeladmin, request, queryset):
    for avaliacao in queryset:
        avaliacao.calcular_pontuacao_total()
    messages.success(request, f"{queryset.count()} avaliações foram recalculadas.")
recalcular_pontuacoes.short_description = "Recalcular pontuações selecionadas"

# Recurso para ImportExport
class AvaliacaoResource(resources.ModelResource):
    class Meta:
        model = Avaliacao
        fields = ('id', 'usuario__nome', 'categoria', 'pontuacao_total', 'data_criacao')

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'data_criacao')
    search_fields = ('nome',)

@admin.register(Avaliacao)
class AvaliacaoAdmin(ImportExportModelAdmin):
    resource_class = AvaliacaoResource
    list_display = ('usuario', 'categoria', 'pontuacao_total', 'data_criacao')
    list_filter = ('categoria', 'data_criacao')
    search_fields = ('usuario__nome', 'categoria')
    readonly_fields = ('pontuacao_total',)
    actions = [recalcular_pontuacoes]

    fieldsets = (
        (None, {
            'fields': ('usuario', 'categoria')
        }),
        ('Pontuações', {
            'fields': ('relevancia_pessoal', 'curiosidade_intelectual', 'disponibilidade_recursos',
                       'prazer_participacao', 'impacto_vida_diaria', 'objetivos_crescimento',
                       'novidade_variedade', 'pontuacao_total')
        }),
    )

    def get_list_chart_data(self, queryset):
        data = queryset.values('categoria').annotate(
            avg_pontuacao=Avg('pontuacao_total')
        ).order_by('-avg_pontuacao')
        return {
            'labels': [item['categoria'] for item in data],
            'datasets': [{
                'label': 'Pontuação Média',
                'data': [item['avg_pontuacao'] for item in data],
                'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                'borderColor': 'rgba(75, 192, 192, 1)',
                'borderWidth': 1
            }]
        }

    list_chart_type = "bar"
    list_chart_options = {
        "responsive": True,
        "scales": {
            "yAxes": [{
                "ticks": {
                    "beginAtZero": True
                }
            }]
        }
    }

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)