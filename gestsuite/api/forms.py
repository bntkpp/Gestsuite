from django import forms
from .models import Receta, Especialidad, Paciente, Doctor, HorarioDisponible, Cita, HistorialPaciente, FichaMedica

class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = [
            'nombre_medicamento', 
            'frecuencia_medicamento',
            'dosis',
            'duracion_medicamento',
            'historial'
            ]

class EspecialidadForm(forms.ModelForm):
    class Meta:
        model =Especialidad
        fields = [
            'nombre_especialidad'
        ]

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            'rut_paciente',
            'nombre_paciente',
            'direccion_paciente',
            'fecha_nacimiento',
            'sexo_paciente',
            'correo_paciente',
            'telefono_paciente'
        ]

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = [
            'rut_doctor',
            'nombre_doctor',
            'correo_doctor',
            'telefono_doctor',
            'sexo_doctor',
            'especialidad'
        ]

class HorarioDisponibleForm(forms.ModelForm):
    class Meta:
        model = HorarioDisponible
        fields = [
            'fecha_disponible',
            'hora_inicio_dispo',
            'hora_termino_dispo',
            'doctor'
        ]

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = [
            'paciente',
            'doctor',
            'disponibilidad_cita',
            'estado_cita',
            'descripcion_cita',
            'motivo_cancelacion'
        ]

class HistorialPacienteForm(forms.ModelForm):
    class Meta:
        model = HistorialPaciente
        fields = [
            'fecha_tratamiento',
            'diagnostico',
            'observaciones_consulta',
            'paciente',
            'doctor'
        ]

class FichaMedicaForm(forms.ModelForm):
    class Meta:
        model = FichaMedica
        fields = [
            'tipo_sangre',
            'alergias',
            'estatura',
            'peso',
            'cond_especiales',
            'enf_cronicas',
            'cirugias',
            'vacunas',
            'antecedentes_fam',
            'consultas_antiguas',
            'paciente',
            'cita'
        ]