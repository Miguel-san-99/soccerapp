from django.urls import path
from . import views

urlpatterns = [
    path('competencia/<int:competencia_id>/registrar-equipo/', views.registrar_equipo, name='registrar_equipo'),
    path('login/', views.login, name='login'),
    path('', views.competencia, name='competencia'),
    path('competencia/<int:competencia_id>/', views.torneo, name='torneo'),
]