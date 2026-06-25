from django import forms
from veterinaria.models import FichaMedica


class EditarFichaDoctorForm(forms.ModelForm):

    class Meta:
        model = FichaMedica

        fields = ['especie','raza','sexo','edad_mascota','peso','motivo_consulta','diagnostico','tratamiento','observaciones']

        widgets = {
            'motivo_consulta': forms.Textarea(attrs={'rows': 3}),
            'diagnostico': forms.Textarea(attrs={'rows': 3}),
            'tratamiento': forms.Textarea(attrs={'rows': 3}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }