from django.db import models
from .choices import posiciones
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.

class Competencia(models.Model):
    nombre = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nombre
    
class Torneo(models.Model):
    nombre = models.CharField(max_length=50)
    competencia = models.ForeignKey(Competencia, on_delete=models.CASCADE, related_name='torneos')
    
    def calcular_tabla(self):
        partidos = Partido.objects.filter(jornada__torneo=self)
        tabla = {}
        for equipo in self.equipos.all():
            tabla[equipo] = {
                'partidos_jugados':0,
                'partidos_ganados':0,
                'partidos_perdidos':0,
                'partidos_empatados':0,
                'goles_favor':0,
                'goles_contra':0,
                'diferencia_goles':0,
                'puntos':0
            }
        for partido in partidos:
            if not partido.equipo_local or not partido.equipo_visita:
                continue
            
            for equipo, gf, gc in [(partido.equipo_local, partido.goles_local, partido.goles_visita), (partido.equipo_visita, partido.goles_visita, partido.goles_local)]:
                tabla[equipo]['partidos_jugados'] += 1
                tabla[equipo]['goles_favor'] += gf
                tabla[equipo]['goles_contra'] += gc
            
            if partido.goles_local > partido.goles_visita:
                tabla[partido.equipo_local]['partidos_ganados'] += 1
                tabla[partido.equipo_local]['puntos'] += 3
                tabla[partido.equipo_visita]['partidos_perdidos'] += 1
                
            elif partido.goles_local < partido.goles_visita:
                tabla[partido.equipo_visita]['partidos_ganados'] += 1
                tabla[partido.equipo_visita]['puntos'] += 3
                tabla[partido.equipo_local]['partidos_perdidos'] += 1
                
            else:
                tabla[partido.equipo_local]['partidos_empatados'] += 1
                tabla[partido.equipo_local]['puntos'] += 1
                tabla[partido.equipo_visita]['partidos_empatados'] += 1
                tabla[partido.equipo_visita]['puntos'] += 1
        
        for stats in tabla.values():
            stats['diferencia_goles'] = stats['goles_favor'] - stats['goles_contra']
        
        tabla_ordenada = sorted(tabla.items(), key=lambda item: (item[1]['puntos'], item[1]['diferencia_goles'], item[1]['goles_favor']), reverse=True)
        
        return [{'equipo': equipo, **stats} for equipo, stats in tabla_ordenada]
    
    def __str__(self):
        return self.nombre
    
class Equipo(models.Model):
    nombre = models.CharField(max_length=20)
    torneos = models.ManyToManyField(Torneo, related_name='equipos')
    
    def __str__(self):
        return self.nombre

class Jugador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=30)
    apellido_paterno = models.CharField(max_length=30)
    apellido_materno = models.CharField(max_length=30)
    posicion = models.CharField(max_length=3, choices=posiciones, default='DC')
    fecha_nac = models.DateField(verbose_name='Fecha de Nacimiento')
    equipo = models.ForeignKey(Equipo, null=True, on_delete=models.SET_NULL, related_name='jugadores')
    
    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno}"

class Jornada(models.Model):
    nombre = models.CharField(max_length=20)
    fecha = models.DateField(default=timezone.now())
    torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE, related_name='jornadas')
    
    def __str__(self):
        return self.nombre
    
class Partido(models.Model):
    jornada = models.ForeignKey(Jornada, on_delete=models.CASCADE, related_name='partidos')
    equipo_local = models.ForeignKey(Equipo, on_delete=models.SET_NULL, null=True, related_name='partidos_local')
    equipo_visita = models.ForeignKey(Equipo, on_delete=models.SET_NULL, null=True, related_name='partidos_visita')
    goles_local = models.SmallIntegerField(default=0)
    goles_visita = models.SmallIntegerField(default=0)
    fecha = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('equipo_local', 'equipo_visita', 'fecha')
        
    def clean(self):
        if self.equipo_local == self.equipo_visita:
            raise ValidationError("Un equipo no puede jugar contra sí mismo")

        if self.jornada and self.equipo_local and self.equipo_visita:
            torneo = self.jornada.torneo

            if torneo not in self.equipo_local.torneos.all():
                raise ValidationError("El equipo local no pertenece al torneo")

            if torneo not in self.equipo_visita.torneos.all():
                raise ValidationError("El equipo visitante no pertenece al torneo")
    
    def save(self, *args, **kwargs):
        self.full_clean()  # ejecuta clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.equipo_local} vs {self.equipo_visita}"