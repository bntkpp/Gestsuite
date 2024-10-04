from django import forms
from django.contrib import admin
from dal import autocomplete
from .models import Receta, Especialidad, Paciente, Doctor, HorarioDisponible, HistorialPaciente, Cita

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['paciente', 'doctor', 'disponibilidad_cita', 'estado_cita', 'descripcion_cita']
        widgets = {
            'paciente': autocomplete.ModelSelect2(url='paciente-autocomplete'),
            'doctor': autocomplete.ModelSelect2(url='doctor-autocomplete'),
        }

class CitaAdmin(admin.ModelAdmin):
    form = CitaForm

class HistorialPacienteForm(forms.ModelForm):
    class Meta:
        model = HistorialPaciente
        fields = ['paciente', 'doctor', 'fecha_tratamiento', 'diagnostico', 'observaciones_consulta']
        widgets = {
            'paciente': autocomplete.ModelSelect2(url='paciente-autocomplete'),
            'doctor': autocomplete.ModelSelect2(url='doctor-autocomplete'),
        }

class HistorialPacienteAdmin(admin.ModelAdmin):
    form = HistorialPacienteForm

class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ['nombre_medicamento', 'frecuencia_medicamento', 'dosis', 'duracion_medicamento', 'historial']
        widgets = {
            'historial': autocomplete.ModelSelect2(url='historialpaciente-autocomplete'),
        }

class RecetaAdmin(admin.ModelAdmin):
    form = RecetaForm

# Register your models here.

admin.site.register(Receta, RecetaAdmin)
admin.site.register(Especialidad)
admin.site.register(Paciente)
admin.site.register(Doctor)
admin.site.register(HorarioDisponible)
admin.site.register(HistorialPaciente, HistorialPacienteAdmin)
admin.site.register(Cita, CitaAdmin)
