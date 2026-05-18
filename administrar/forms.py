from django import forms
from core.models import Equipo, Torneo

class EquipoForm(forms.ModelForm):
    username = forms.CharField(
        max_length=20,
        label='Nombre del manager',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Username'})
        )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control',
                                       'placeholder': 'Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': 'Password'})
        )
    
    class Meta:
        model = Equipo
        fields = ['nombre']
        widgets = {'nombre': forms.TextInput(attrs={'class': 'form-control',
                                                    'placeholder': 'Nombre'})}
        labels = {'nombre': 'Nombre del equipo'}