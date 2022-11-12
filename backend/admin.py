from django.contrib import admin

# Register your models here.
from backend.models import TipoInvestimento, Investimento, InvestimentoRendimento, TipoRendimento, Variavel, \
    VariavelMes, CalculoFuturo

admin.site.register(TipoInvestimento)
admin.site.register(Investimento)
admin.site.register(InvestimentoRendimento)
admin.site.register(TipoRendimento)
admin.site.register(Variavel)
admin.site.register(VariavelMes)
admin.site.register(CalculoFuturo)

