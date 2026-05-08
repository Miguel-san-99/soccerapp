from django import forms
from core.models import Equipo, Torneo

class EquipoForm(forms.ModelForm):
    username = forms.CharField(
        max_length=20,
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
    torneo = forms.ModelChoiceField(
        queryset=Torneo.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select',
                                   'placeholder': 'temporada 2026'})
        )
    
    class Meta:
        model = Equipo
        fields = ['nombre']
        widgets = {'nombre': forms.TextInput(attrs={'class': 'form-control',
                                                    'placeholder': 'Nombre'})}
        
    def __init__(self, *args, **kwargs):

        torneos = kwargs.pop('torneos', None)

        super().__init__(*args, **kwargs)

        if torneos:
            self.fields['torneo'].queryset = torneos