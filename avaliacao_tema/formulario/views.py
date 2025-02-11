# formulario/views.py

from django.template.defaulttags import register
from django.shortcuts import render, redirect, get_object_or_404
from .models import Categoria
from .forms import AvaliacaoForm

# Certifique-se de que estas definições estejam efetivamente listadas antes
# de qualquer uso em uma função ou método.

TEXTO_EXPLICATIVO_CATEGORIAS = {
    "Tecnologia e Inovação": "Esta categoria aborda avanços tecnológicos e inovações disruptivas que transformam como vivemos e trabalhamos.",
    "Saúde e Bem-Estar": "Foque em conceitos, práticas e produtos que melhoram a saúde e promovem o bem-estar físico e mental.",
    "Educação e Aprendizado": "Examine iniciativas, métodos e ferramentas que buscam enriquecer a educação e o aprendizado.",
    "Sustentabilidade e Meio Ambiente": "Avalie práticas e negócios que visam proteger o meio ambiente e promover a sustentabilidade.",
    "Moda e Beleza": "Explore tendências de moda, estilos e produtos de beleza que destacam inovação e autoexpressão.",
    "Alimentação e Gastronomia": "Investigue o mundo culinário, desde inovações na cozinha até às tendências de consumo.",
    "Entretenimento e Mídia": "Compreenda as evoluções no entretenimento e nas mídias e seu impacto cultural.",
    "Viagens e Turismo": "Analise como novas tendências transformam a experiência de viagem e as indústrias turísticas.",
    "E-commerce e Vendas Online": "Considere o impacto do e-commerce nos comportamentos de consumo e nas operações de vendas.",
    "Finanças Pessoais e Investimentos": "Avalie recursos e estratégias que capacitam as pessoas a melhor gerirem suas finanças pessoais e a investirem sabiamente."
}

METRICS_DESCRIPTIONS = {
    'relevancia_pessoal': "Quão relevante ou significativa esta categoria é para você pessoalmente?",
    'curiosidade_intelectual': "Quanto esta categoria desperta sua curiosidade e vontade de aprender mais?",
    'disponibilidade_recursos': "Quão fácil é para você acessar recursos e informações nesta categoria?",
    'prazer_participacao': "Quanto satisfação satisfação você sente ao se envolver com esta categoria?",
    'impacto_vida_diaria': "Qual o nível de impacto desta categoria em suas atividades diárias?",
    'objetivos_crescimento': "Quão alinhada está esta categoria com seus objetivos pessoais ou profissionais?",
    'novidade_variedade': "Quanto esta categoria traz de novidade ou variedade à sua rotina?"
}

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def avaliar(request, categoria_id):
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    texto_explicativo = TEXTO_EXPLICATIVO_CATEGORIAS.get(categoria.nome, "")

    if request.method == 'POST':
        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.categoria = categoria
            avaliacao.save()

            proximas_categorias = Categoria.objects.filter(pk__gt=categoria.id).order_by('pk')
            if proximas_categorias.exists():
                return redirect('avaliar', categoria_id=proximas_categorias.first().id)
            else:
                return redirect('results')

    else:
        form = AvaliacaoForm()

    context = {
        'form': form,
        'categoria': categoria,
        'texto_explicativo': texto_explicativo,
        'METRICS_DESCRIPTIONS': METRICS_DESCRIPTIONS
    }

    return render(request, 'formulario/avaliar.html', context)

def home(request):
    return render(request, 'formulario/home.html')

def results(request):
    # Lógica para calcular resultados & apresentar categorias
    return render(request, 'formulario/results.html')  # Implementamos esta parte nos próximos passos