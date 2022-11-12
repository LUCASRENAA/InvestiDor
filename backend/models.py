import datetime
from datetime import timezone, timedelta

from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class TipoInvestimento(models.Model):
    #renda_fixa
    nome = models.CharField(max_length=50)

    def __str__(self):
        return (f'{self.nome}')


class Investimento(models.Model):
    #cdb,tesouro selic
    nome = models.CharField(max_length=50)
    tipo = models.ForeignKey(TipoInvestimento, models.CASCADE)
    valor =  models.DecimalField(max_digits=10, decimal_places=2,default=0)
    valor_atual =  models.DecimalField(max_digits=10, decimal_places=2,default=0)

    cotas =  models.DecimalField(max_digits=10, decimal_places=2,default=0)

    usuario = models.ForeignKey(User, models.CASCADE)

    data_criacao = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)

    @property
    def valor_total(self):
        servicos = self.Investimento.objects.filter(ativo=True)  # aplicar filtros padroes se precisar
        preco_total = 0.00
        for servico in servicos:
            preco_total += servico.valor
        return preco_total

    def __str__(self):
        return (f'{self.nome}')



class TipoRendimento(models.Model):
    nome = models.CharField(max_length=50)
    def __str__(self):
        return (f'{self.nome}')
class InvestimentoRendimento(models.Model):
    investimento = models.ForeignKey(Investimento, models.CASCADE)
    valor =  models.DecimalField(max_digits=10, decimal_places=2,default=0)
    data_rendimento = models.DateTimeField()
    tipo = models.ForeignKey(TipoRendimento, models.CASCADE)


class Variavel(models.Model):
    nome = models.CharField(max_length=50)
    def __str__(self):
        return (f'{self.nome}')

class VariavelMes(models.Model):
    tipo = models.ForeignKey(Variavel, models.CASCADE)
    valor =  models.DecimalField(max_digits=10, decimal_places=6,default=0)
    data_criacao = models.DateTimeField(auto_now=False)


    def __str__(self):
        return (f'{self.tipo.nome}')

class CalculoFuturo(models.Model):
    investimento = models.ForeignKey(Investimento, models.CASCADE)
    variavel = models.ForeignKey(Variavel, models.CASCADE)
    bonus =  models.DecimalField(max_digits=10, decimal_places=6,default=0)
    def __str__(self):
        return (f'{self.investimento.nome}')
