from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from backend.models import Investimento, InvestimentoRendimento, TipoInvestimento, CalculoFuturo, VariavelMes, \
    VariavelImposto


def somar_investimento(usuario,tipo):
    soma = 0

    if tipo == "":
        for investimento in Investimento.objects.filter(ativo=True,usuario=usuario):
            soma = float(investimento.valor) + soma
    else:
        for investimento in Investimento.objects.filter(ativo=True,tipo__nome=tipo,usuario=usuario):
            soma = float(investimento.valor) + soma


    soma = round(soma, 2)
    return soma


def somar_rendimentos(usuario):
    somar = 0
    for investimento_render in InvestimentoRendimento.objects.filter(investimento__usuario=usuario):
        somar = float(investimento_render.valor) + somar

    return somar


def index(request):
    usuario = request.user
    soma = somar_investimento(usuario,"")


    vetor_investimentos = []
    for investimento in Investimento.objects.filter(ativo=True,usuario=usuario):
        porcentagem_investimento = round(100 * float(investimento.valor) / soma, 2)

        vetor_investimentos.append(investimento_rendimento(investimento,investimento.valor,porcentagem_investimento))
    dados = {"investimentos": Investimento.objects.filter(ativo=True,usuario=usuario),"soma":soma,"titulo":"Gráfico sem rendimentos/perdas",
             'pagina':1,'vetor_tabela':vetor_investimentos}
    return render(request, "frontend/modelo.html",dados)


def rendimentos(request):
    usuario = request.user
    soma = somar_investimento(usuario,'')





    investimentos = Investimento.objects.filter(usuario=usuario)
    investimentos_rendimentos_enviados = []
    for investimento in investimentos:
        rendimentos = InvestimentoRendimento.objects.filter(investimento=investimento,investimento__usuario=usuario)
        valor = float(investimento.valor)
        for rendimento in rendimentos:
            valor = valor + float(rendimento.valor)
            valor = round(float(valor),2)
        if valor != 0:
            porcentagem_investimento = round(100 * valor / soma, 2)

            investimentos_rendimentos_enviados.append(investimento_rendimento(investimento,valor,porcentagem_investimento))

    print(investimentos_rendimentos_enviados)
    soma_rendimento = somar_rendimentos(usuario)
    somar_valores = soma + soma_rendimento

    somar_valores = round(somar_valores, 2)
    dados = {"investimentos": Investimento.objects.filter(usuario=usuario),
             "vetor_com_investimento_rendimentos": investimentos_rendimentos_enviados,
             "titulo": "Gráfico com rendimentos/perdas","soma":somar_valores,'pagina':1,"vetor_tabela":investimentos_rendimentos_enviados,'vetor_tabela':investimentos_rendimentos_enviados}
    return render(request, "frontend/modelo.html",dados)



def rendimento_por_tipo(request):
    usuario = request.user
    soma = somar_investimento(usuario,"")



    vetor_investimentos = []
    for tipo in TipoInvestimento.objects.filter():
        investimento = Investimento.objects.filter(ativo=True,tipo=tipo,usuario=usuario)
        soma_tipo = 0
        for percorrer_investimentos_tipo in investimento:
            soma_tipo = float(percorrer_investimentos_tipo.valor) + soma_tipo
        soma_tipo = round(soma_tipo,2)
        porcentagem_investimento = round(100*soma_tipo/soma,2)



        vetor_investimentos.append(investimento_rendimento(tipo,soma_tipo,porcentagem_investimento))
    print(vetor_investimentos)


    dados = {"investimentos": vetor_investimentos,"soma":soma,"titulo":"Gráfico sem rendimentos/perdas por tipo",
             'pagina':3,"vetor_tabela":vetor_investimentos}
    return render(request, "frontend/modelo.html",dados)

class investimento_rendimento:
        def __init__(self, investimento, valor, porcentagem):
            self.investimento = investimento
            self.valor = valor
            self.porcentagem = porcentagem


def rendimento_por_tipo_total(request):
    usuario = request.user
    soma = somar_investimento(usuario,"")



    vetor_investimentos = []
    for tipo in TipoInvestimento.objects.filter():
        investimento = Investimento.objects.filter(ativo=True,tipo=tipo,usuario=usuario)
        soma_tipo = 0
        for percorrer_investimentos_tipo in investimento:
            soma_tipo = float(percorrer_investimentos_tipo.valor) + soma_tipo



        for percorrer_investimentos_tipo in InvestimentoRendimento.objects.filter(investimento__tipo=tipo,investimento__usuario=usuario):
            soma_tipo = float(percorrer_investimentos_tipo.valor) + soma_tipo
        soma_tipo = round(soma_tipo,2)
        porcentagem_investimento = round(100*soma_tipo/soma,2)
        vetor_investimentos.append(investimento_rendimento(tipo,soma_tipo,porcentagem_investimento))
    print(vetor_investimentos)


    dados = {"investimentos": vetor_investimentos,"soma":soma,"titulo":"Gráfico com rendimentos/perdas por tipo",
             'pagina':3,"vetor_tabela":vetor_investimentos}
    return render(request, "frontend/modelo.html",dados)





def tipo_de_investimento(request,tipo):
    usuario = request.user
    soma = somar_investimento(usuario,tipo)


    vetor_investimentos = []
    for investimento in Investimento.objects.filter(ativo=True,tipo__nome=tipo,usuario=usuario):
        porcentagem_investimento = round(100 * float(investimento.valor) / soma, 2)

        vetor_investimentos.append(investimento_rendimento(investimento,investimento.valor,porcentagem_investimento))
    dados = {"investimentos": Investimento.objects.filter(ativo=True,tipo__nome=tipo,usuario=usuario),"soma":soma,"titulo":"Gráfico sem rendimentos/perdas",
             'pagina':2,'vetor_tabela':vetor_investimentos}
    return render(request, "frontend/modelo.html",dados)


def CALCULOFUTURO(request):

    meses = 12
    id_objeto = 1
    resposta,variavel,bonus,total,calculo = calcular_futuro_objeto(id_objeto)
    print(resposta)
    total_inicial = total
    total = resposta  + total
    for simulacao in range(meses-1):
        resposta = calcular_futuro_imaginado(total,variavel,bonus )
        total = resposta + total
        print(total)

    lucro = total - total_inicial
    print(lucro)
    #ainda falta calcular imposto
    variaveis = VariavelImposto.objects.filter(tipo=calculo.variavel)
    dias = 12* (30.4167)
    for pegar_imposto in variaveis:

        if dias > pegar_imposto.dias:
            imposto = pegar_imposto.valor
    print(imposto)


    lucro = lucro-float(lucro) * (float(imposto) / 100)

    return HttpResponse(str(total_inicial + lucro) + "<p>Lucro: " + str(lucro) +"</p> ")


def calcular_futuro_objeto(id):
    calculo = CalculoFuturo.objects.get(id=id)

    total = float(calculo.investimento.valor_atual)
    variavel = float(VariavelMes.objects.get(id=calculo.variavel.id).valor) / 12 / 100
    bonus = float(calculo.bonus)

    resposta = round(total * variavel * bonus, 2)
    return resposta,variavel,bonus,total,calculo

def calcular_futuro_imaginado(total,variavel,bonus):
    resposta = round(total * variavel * bonus, 2)
    return resposta