from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from datetime import datetime
from .validators import validate_rut


class AppUserManager(BaseUserManager):
	def create_user(self, username, email, password=None):
		if not email:
			raise ValueError('El email es obligatorio.')
		if not username:
			raise ValueError('El nombre de usuario es obligatorio.')
		if not password:
			raise ValueError('La contraseña es obligatoria.')
		email = self.normalize_email(email)
		user = self.model(username=username, email = email)
		user.set_password(password)
		user.save()
		return user
	
	def create_superuser(self, username, email, password=None):
		if not email:
			raise ValueError('El email es obligatorio.')
		if not username:
			raise ValueError('El nombre de usuario es obligatorio.')
		if not password:
			raise ValueError('La contraseña es obligatoria.')

		user = self.create_user(username, email, password)
		user.is_superuser = True
		user.is_staff = True
		user.save()
		return user


class AppUser(AbstractBaseUser, PermissionsMixin):
	user_id = models.AutoField(primary_key=True)
	username = models.CharField(max_length=50, unique=True)
	email = models.EmailField(max_length=50, unique=True)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']
	objects = AppUserManager()
	def __str__(self):
		return self.username



# Modelo Especialidad
class Especialidad(models.Model):
    id_especialidad = models.AutoField(primary_key=True)
    nombre_especialidad = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre_especialidad

    class Meta:
        verbose_name = "Especialidad"
        verbose_name_plural = "Especialidades"

# Modelo Paciente
class Paciente(models.Model):
    rut_paciente = models.CharField(max_length=12, primary_key=True, validators=[validate_rut])
    nombre_paciente = models.CharField(max_length=50)
    direccion_paciente = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    sexo_choices_paciente = [('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')]
    sexo_paciente = models.CharField(max_length=1, choices=sexo_choices_paciente)
    correo_paciente = models.EmailField(unique=True)
    telefono_paciente = models.CharField(max_length=15)

    @property
    def edad(self):
        today = date.today()
        return today.year - self.fecha_nacimiento.year - ((today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))

    def __str__(self):
        return self.nombre_paciente

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"

# Modelo Doctor
class Doctor(models.Model):
    rut_doctor = models.CharField(max_length=12, primary_key=True, validators=[validate_rut])
    nombre_doctor = models.CharField(max_length=50)
    correo_doctor = models.EmailField(unique=True)
    telefono_doctor = models.CharField(max_length=15)  # Aceptamos números con código internacional
    sexo_choices_doctor = [('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')]
    sexo_doctor = models.CharField(max_length=1, choices=sexo_choices_doctor)
    especialidad = models.ManyToManyField(Especialidad, related_name='doctores')

    def __str__(self):
        return self.nombre_doctor

    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctores"

# Modelo HorarioDisponible
class HorarioDisponible(models.Model):
    id_disponibilidad = models.AutoField(primary_key=True)
    fecha_disponible = models.DateField()
    hora_inicio_dispo = models.TimeField()
    hora_termino_dispo = models.TimeField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    def clean(self):
        if self.hora_inicio_dispo >= self.hora_termino_dispo:
            raise ValidationError('La hora de inicio debe ser menor a la hora de término')
        if self.fecha_disponible < date.today():
            raise ValidationError('La fecha de disponibilidad no puede ser menor a la fecha actual')

    def __str__(self):
        return f'{self.doctor} - {self.fecha_disponible} {self.hora_inicio_dispo}-{self.hora_termino_dispo}'

    class Meta:
        verbose_name = "Horario Disponible"
        verbose_name_plural = "Horarios Disponibles"

# Modelo Cita
class Cita(models.Model):
    id_cita = models.AutoField(primary_key=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    disponibilidad_cita = models.ForeignKey(HorarioDisponible, on_delete=models.CASCADE)
    estado_cita_choices = [('P', 'Pendiente'), ('C', 'Cancelada'), ('R', 'Realizada')]
    estado_cita = models.CharField(max_length=1, choices=estado_cita_choices)
    disponible = models.BooleanField(default=True)
    descripcion_cita = models.CharField(max_length=100)
    motivo_cancelacion = models.TextField(blank=True, null=True)

    def clean(self):
        if self.estado_cita == 'C' and not self.motivo_cancelacion:
            raise ValidationError('El motivo de cancelación es obligatorio si la cita está cancelada.')

    def __str__(self):
        return f'Cita {self.id_cita} - {self.paciente} con {self.doctor}'

    class Meta:
        verbose_name = "Cita"
        verbose_name_plural = "Citas"

# Modelo HistorialPaciente
class HistorialPaciente(models.Model):
    
    id_historial = models.AutoField(primary_key=True)
    fecha_tratamiento = models.DateField()
    diagnostico = models.TextField()
    observaciones_consulta = models.TextField()
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    def __str__(self):
        return f'Historial {self.id_historial} - {self.paciente}'

    class Meta:
        verbose_name = "Historial del Paciente"
        verbose_name_plural = "Historiales de Pacientes"

# Modelo Receta
class Receta(models.Model):
    id_receta = models.AutoField(primary_key=True)
    nombre_medicamento = models.CharField(max_length=50)
    frecuencia_medicamento = models.CharField(max_length=50)
    dosis = models.CharField(max_length=50)
    duracion_medicamento = models.IntegerField(help_text="Duración del tratamiento en días")
    historial = models.ForeignKey(HistorialPaciente, on_delete=models.CASCADE)

    def __str__(self):
        return f'Receta {self.id_receta} - {self.nombre_medicamento}'

    class Meta:
        verbose_name = "Receta"
        verbose_name_plural = "Recetas"

# Modelo FichaMedica
class FichaMedica(models.Model):
    id_fichaPaciente = models.AutoField(primary_key=True)
    tipo_sangre = models.CharField(max_length=3)
    alergias = models.TextField()
    estatura = models.FloatField()
    peso = models.FloatField()
    cond_especiales = models.TextField()
    enf_cronicas = models.TextField()
    cirugias = models.TextField()
    vacunas = models.TextField()
    antecedentes_fam = models.TextField()
    consultas_antiguas = models.ForeignKey(HistorialPaciente, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE)

    def __str__(self):
        return f'Ficha {self.id_fichaPaciente} de Paciente {self.paciente}'

    class Meta:
        verbose_name = "Ficha Médica"
        verbose_name_plural = "Fichas Médicas"