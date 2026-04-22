from .models import Competencia

def competencias(request):
    return {
        'competencias': Competencia.objects.all()
    }