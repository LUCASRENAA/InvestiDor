from django.urls import path
from . import views

urlpatterns = [
    path("investimento/", views.index, name="index"),

    path("investimento/<tipo>", views.tipo_de_investimento, name="index"),

    path("rendimentos/", views.rendimentos),
    path("tipo/", views.rendimento_por_tipo),
    path("tipo2/", views.rendimento_por_tipo_total),
    path("", views.CALCULOFUTURO),

]