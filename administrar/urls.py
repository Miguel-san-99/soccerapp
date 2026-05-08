from django.urls import path
from . import views

urlpatterns = [
    path('competencia/<int:competencia_id>/registrar-equipo/', views.registrar_equipo, name='registrar_equipo'),
]