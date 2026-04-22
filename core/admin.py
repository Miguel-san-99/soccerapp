from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Competencia)
admin.site.register(Torneo)
admin.site.register(Jornada)
admin.site.register(Partido)
admin.site.register(Equipo)
admin.site.register(Jugador)