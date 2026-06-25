from django import forms
from django.utils import timezone
from .models import SolicitudCita


class SolicitudCitaForm(forms.ModelForm):

    class Meta:
        model = SolicitudCita

        fields = ['nombre','apellido','email','telefono','nombre_mascota','tipo_consulta','fecha_hora','observaciones']

        widgets = {
            'telefono': forms.TextInput(attrs={
                'placeholder': 'Ej: 912345678',
                'maxlength': '9',
                'inputmode': 'numeric',
                'oninput': "this.value = this.value.replace(/[^0-9]/g, '')"
            }),

            'fecha_hora': forms.TextInput(attrs={
                'class': 'datetimepicker',
                'placeholder': 'Selecciona fecha y hora'

            }),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']
        if not telefono.isdigit():
            raise forms.ValidationError('El telefono solo debe contener numeros.')
        if len(telefono) != 9:
            raise forms.ValidationError('El telefono debe tener 9 digitos.')
        return telefono
    
    def clean_fecha_hora(self):
        fecha_hora = self.cleaned_data['fecha_hora']
        if fecha_hora < timezone.now():
            raise forms.ValidationError('No puede seleccionar una fecha u hora pasada.')
        
        if fecha_hora.year != 2026:
            raise forms.ValidationError('Solo se permiten citas durante el año 2026.')
        
        if fecha_hora.minute not in [0, 30]:
            raise forms.ValidationError('Solo se permiten horarios cada 30 minutos.')
        
        if fecha_hora.hour < 9:
            raise forms.ValidationError('El horario comienza a las 09:00.')
        
        if fecha_hora.hour >= 20:
            raise forms.ValidationError('El horario termina a las 20:00.')
        
        if 13 <= fecha_hora.hour < 15:
            raise forms.ValidationError('No hay atención entre 13:00 y 15:00.')

        # Esto nos ayuda Verifica si ya existe una cita en la misma fecha y hora cada cita es con 30 minutos de diferencia y no se puede reservar la misma hora para otra cita tambien.
        if SolicitudCita.objects.filter(fecha_hora=fecha_hora).exists():
            raise forms.ValidationError('Este horario ya fue reservado. Por favor seleccione otro horario.')

        return fecha_hora



