from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from backend.models import Investimento, InvestimentoRendimento, TipoInvestimento, CalculoFuturo, VariavelMes, \
    VariavelImposto, TipoRendimento


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

    for investimento in Investimento.objects.all():
        print(investimento)
        try:
            CalculoFuturo.objects.get(investimento=investimento)

            a = investimento.start_date
            print(a)
            print("teste")
            print(a.month)
            from datetime import date

            b = date.today()

            dias = pegar_feriados(a, b)
            id_objeto = CalculoFuturo.objects.get(investimento=investimento).id
            resposta, variavel, bonus, total, calculo,soma = calcular_futuro_objeto(id_objeto,a.month)
            total_inicial = total
            for dia in dias:
                print(investimento.nome)

                if investimento.id == 7:
                    print("aqui")
                    print(bonus)
                    print(variavel)
                    print(total)

                resposta2, variavel2, bonus, total2, calculo2, soma = calcular_futuro_objeto(id_objeto, dia.month)

                resposta_verdadeira = calcular_futuro_imaginado(total, variavel, bonus,soma)/12/(30.4167)/100

                resposta = round(calcular_futuro_imaginado(total, variavel, bonus,soma)/12/(30.4167)/100,6)
                total = resposta_verdadeira + total

                try:
                    print(str(InvestimentoRendimento.objects.get(investimento=investimento,data_rendimento__date=dia,tipo=TipoRendimento.objects.get(id=1))))

                except:

                    InvestimentoRendimento.objects.create(investimento=investimento,data_rendimento=dia,valor=resposta,tipo=TipoRendimento.objects.get(id=1))

                print(dia)

        except:
            continue



        #InvestimentoRendimento.

    return HttpResponse("")


def calcular_futuro_objeto(id,mes):
    calculo = CalculoFuturo.objects.get(id=id)

    total = float(calculo.investimento.valor_atual)

    aqui = VariavelMes.objects.get(tipo=calculo.variavel, data_criacao__month=int(mes))
    variavel = float(aqui.valor)
    bonus = float(calculo.bonus)
    soma = float(calculo.soma)

    resposta = round(total * variavel * bonus, 2)
    return resposta,variavel,bonus,total,calculo,soma

def calcular_futuro_imaginado(total,variavel,bonus,soma):
    resposta = total * ((variavel+soma) * bonus)/100
    return resposta




def iterdates(date1, date2):
    import datetime
    one_day = datetime.timedelta(days = 1)
    current = date1
    while current < date2:
        yield current
        current += one_day

def pegar_feriados(a,b):
    import datetime
    from workalendar.america import Brazil
    dias_sem_sabado_domingo = []
    feriados_lista = []
    cal = Brazil()
    feriados = cal.holidays(2022)

    for feriado in feriados:
        feriados_lista.append(feriado[0])
    for d in iterdates(a, b):
        if d.weekday() not in (5, 6):

            print(d, d.weekday())
            if d not in feriados_lista:
                dias_sem_sabado_domingo.append(d)

    print(len(dias_sem_sabado_domingo))

    return dias_sem_sabado_domingo