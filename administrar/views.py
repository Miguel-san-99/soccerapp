from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .forms import EquipoForm
from core.models import Competencia, Torneo

# Create your views here.
def registrar_equipo(request, torneo_id):
    
    torneo = get_object_or_404(Torneo, id=torneo_id)
    
    if request.method == 'POST':
        form = EquipoForm(request.POST)
        
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            equipo = form.save(commit=False)
            equipo.manager=user
            equipo.torneo=torneo
            equipo.save()
            return redirect('administrar_torneo', competencia_id=torneo.competencia.id, torneo_id=torneo.id)
    
    else:
        form = EquipoForm()
        context = {'form': form}
        
    return render(request, 'administrar/registrar_equipo.html', context)

def login(request):
    return render(request, 'administrar/login.html')

def competencia(request):
    competencias = Competencia.objects.all()
    context = {'competencias': competencias}
    if request.method == 'POST':
        competencia_id = request.POST.get('competencia')
        return redirect('')
    return render(request, 'administrar/competencia.html', context)

def torneo(request, competencia_id):
    competencia = get_object_or_404(Competencia, id=competencia_id)
    torneos = competencia.torneos.all()
    context = {'competencia':competencia, 'torneos':torneos}
    return render(request, 'administrar/torneo.html', context)

def administrar_torneo(request, competencia_id, torneo_id):
    competencia = get_object_or_404(Competencia, id=competencia_id)
    torneo = get_object_or_404(Torneo, id=torneo_id)
    form_equipo = EquipoForm()
    equipos = torneo.equipos.all()
    context = {'competencia':competencia, 'torneo':torneo, 'equipos':equipos, 'form_equipo': form_equipo}
    return render(request, 'administrar/administrar_torneo.html', context)