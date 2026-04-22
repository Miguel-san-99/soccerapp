from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('competencia/<int:competencia_id>/torneo/<int:torneo_id>/', views.competencia, name='competencia'),
    path('tabla-partidos-htmx/<int:jornada_id>/', views.tabla_partidos_htmx, name='tabla_partidos_htmx'),
    path('nosotros/', views.nosotros, name='nosotros'),
]