from django.shortcuts import render, get_object_or_404, redirect
from .models import Torneo, Competencia, Jornada

# Create your views here.

def home(request):
    return render(request, 'core/index.html')

def competencia(request, competencia_id, torneo_id):
    competencia = get_object_or_404(Competencia, id=competencia_id)
    torneos = competencia.torneos.all()
    if torneo_id:
        torneo_actual = get_object_or_404(Torneo, id=torneo_id)
    else:
        torneo_actual = torneos.order_by('-id').first()
    tabla = torneo_actual.calcular_tabla()
    lista_victorias = sorted(tabla, key=lambda item: (item['partidos_ganados']), reverse=True)[:5]
    lista_perdidos = sorted(tabla, key=lambda item: (item['partidos_perdidos']), reverse=True)[:5]
    lista_empatados = sorted(tabla, key=lambda item: (item['partidos_empatados']), reverse=True)[:5]
    lista_goles_favor = sorted(tabla, key=lambda item: (item['goles_favor']), reverse=True)[:5]
    lista_goles_contra = sorted(tabla, key=lambda item: (item['goles_contra']), reverse=True)[:5]
    jornadas = torneo_actual.jornadas.all()
    context = {'competencia': competencia,
               'torneos': torneos,
               'torneo_actual': torneo_actual,
               'tabla': tabla,
               'jornadas': jornadas,
               'lista_victorias': lista_victorias,
               'lista_perdidos': lista_perdidos,
               'lista_empatados': lista_empatados,
               'lista_goles_favor': lista_goles_favor,
               'lista_goles_contra': lista_goles_contra
               }
    return render(request, 'core/competencia.html', context)

def tabla_partidos_htmx(request, jornada_id):
    jornada = get_object_or_404(Jornada, id=jornada_id)
    partidos = jornada.partidos.all()
    context = {'partidos':partidos, 'jornada':jornada}
    return render(request, 'core/partials/tabla_partidos.html', context)


def nosotros(request):
    return render(request, 'core/nosotros.html')