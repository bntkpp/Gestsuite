from django.contrib import admin
from .models import Receta, Especialidad, Paciente, Doctor, HorarioDisponible, HistorialPaciente, Cita


# Register your models here.

admin.site.register(Receta)
admin.site.register(Especialidad)
admin.site.register(Paciente)
admin.site.register(Doctor)
admin.site.register(HorarioDisponible)
admin.site.register(HistorialPaciente)
admin.site.register(Cita)
