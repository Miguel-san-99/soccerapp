from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .forms import EquipoForm
from core.models import Competencia

# Create your views here.
def registrar_equipo(request, competencia_id):
    
    competencia = get_object_or_404(Competencia, id=competencia_id)
    torneos = competencia.torneos.all()
    context = {'competencia': competencia}
    
    if request.method == 'POST':
        form = EquipoForm(request.POST, torneos=torneos)
        
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            equipo = form.save(commit=False)
            equipo.manager=user
            equipo.torneo=form.cleaned_data['torneo']
            equipo.save()
            return redirect('home')
    
    else:
        form = EquipoForm(torneos=torneos)
        context = {'form': form}
        
    return render(request, 'administrar/registrar_equipo.html', context)

def home(request):
    return render(request, 'administrar/index.html')