from django import forms
from django.contrib.auth.models import User
from veterinaria.models import SolicitudCita, FichaMedica


class EditarSolicitudForm(forms.ModelForm):

    veterinario = forms.ModelChoiceField(queryset=User.objects.filter(perfil__rol='Veterinario'),required=False)
    class Meta:
        model = SolicitudCita
        fields = ['veterinario', 'estado']

class FichaMedicaForm(forms.ModelForm):
    class Meta:
        model = FichaMedica
        fields = ['especie', 'raza', 'sexo', 'edad_mascota', 'peso', 'motivo_consulta', 'diagnostico', 'tratamiento', 'observaciones']
        widgets = {
            'motivo_consulta': forms.Textarea(attrs={'rows': 3}),
            'diagnostico': forms.Textarea(attrs={'rows': 3}),
            'tratamiento': forms.Textarea(attrs={'rows': 3}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }