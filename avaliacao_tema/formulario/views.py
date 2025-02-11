# formulario/views.py
from django.db.models import Avg, Count
from django.template.defaulttags import register
from django.shortcuts import render, redirect, get_object_or_404
from .models import Categoria, Avaliacao, Usuario
from .forms import AvaliacaoForm, UsuarioForm
import json
from django.core.serializers.json import DjangoJSONEncoder

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

CATEGORIAS = [
    "Moda e Beleza",
    "Alimentação e Gastronomia",
    "Viagens e Turismo",
    "Educação e Aprendizado",
    "E-commerce e Vendas Online",
    "Entretenimento e Mídia",
    "Saúde e Bem-Estar",
    "Finanças Pessoais e Investimentos",
    "Sustentabilidade e Meio Ambiente",
    "Tecnologia e Inovação"
]

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def home(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            request.session['usuario_id'] = usuario.id
            return redirect('avaliar', categoria_id=1)
    else:
        form = UsuarioForm()
    return render(request, 'formulario/home.html', {'form': form})

def avaliar(request, categoria_id):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('home')
    
    usuario = get_object_or_404(Usuario, id=usuario_id)
    categoria = CATEGORIAS[categoria_id - 1]  # Assumindo que CATEGORIAS é uma lista de strings
    
    if request.method == 'POST':
        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.usuario = usuario
            avaliacao.categoria = categoria
            avaliacao.save()
            avaliacao.calcular_pontuacao_total()
            
            if categoria_id < len(CATEGORIAS):
                return redirect('avaliar', categoria_id=categoria_id + 1)
            else:
                return redirect('results')
    else:
        form = AvaliacaoForm()

    context = {
        'form': form,
        'categoria': categoria,
        'METRICS_DESCRIPTIONS': METRICS_DESCRIPTIONS
    }
    return render(request, 'formulario/avaliar.html', context)

class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if obj is None:
            return None
        return super().default(obj)
    
def results(request):
    # Calcular o ranking geral das categorias
    ranking_geral = []
    for categoria in CATEGORIAS:
        avaliacoes = Avaliacao.objects.filter(categoria=categoria)
        pontuacao_media = avaliacoes.aggregate(Avg('pontuacao_total'))['pontuacao_total__avg'] or 0
        num_avaliacoes = avaliacoes.count()
        ranking_geral.append({
            'nome': categoria,
            'pontuacao_media': pontuacao_media,
            'num_avaliacoes': num_avaliacoes
        })
    
    ranking_geral.sort(key=lambda x: x['pontuacao_media'], reverse=True)

    # Obter todas as avaliações para o gráfico
    todas_avaliacoes = Avaliacao.objects.select_related('usuario').all()

    # Preparar dados para o gráfico
    usuarios = Usuario.objects.all()
    dados_grafico = {
        'categorias': CATEGORIAS,
        'usuarios': [user.nome for user in usuarios],
        'pontuacoes': []
    }

    for usuario in usuarios:
        pontuacoes_usuario = []
        for categoria in CATEGORIAS:
            avaliacao = Avaliacao.objects.filter(usuario=usuario, categoria=categoria).first()
            pontuacoes_usuario.append(avaliacao.pontuacao_total if avaliacao else None)
        dados_grafico['pontuacoes'].append(pontuacoes_usuario)

    context = {
        'ranking_geral': ranking_geral,
        'todas_avaliacoes': todas_avaliacoes,
        'dados_grafico': json.dumps(dados_grafico, cls=CustomJSONEncoder),
    }
    return render(request, 'formulario/results.html', context)