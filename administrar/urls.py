from django.urls import path
from . import views

urlpatterns = [
    path('registrar-equipo/<int:torneo_id>/', views.registrar_equipo, name='registrar_equipo'),
    path('login/', views.login, name='login'),
    path('', views.competencia, name='competencia'),
    path('competencia/<int:competencia_id>/', views.torneo, name='torneo'),
    path('competencia/<int:competencia_id>/torneo/<int:torneo_id>/', views.administrar_torneo, name='administrar_torneo'),
]