# Generated by Django 5.1.1 on 2024-11-26 19:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Especialidad',
            fields=[
                ('id_especialidad', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_especialidad', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name': 'Especialidad',
                'verbose_name_plural': 'Especialidades',
            },
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id_paciente', models.AutoField(primary_key=True, serialize=False)),
                ('rut_paciente', models.CharField(max_length=12)),
                ('nombre_paciente', models.CharField(max_length=50)),
                ('direccion_paciente', models.CharField(max_length=50)),
                ('fecha_nacimiento', models.DateField()),
                ('sexo_paciente', models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')], max_length=1)),
                ('correo_paciente', models.EmailField(max_length=254, unique=True)),
                ('telefono_paciente', models.CharField(max_length=15)),
            ],
            options={
                'verbose_name': 'Paciente',
                'verbose_name_plural': 'Pacientes',
            },
        ),
        migrations.CreateModel(
            name='Receta',
            fields=[
                ('id_receta', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_medicamento', models.CharField(max_length=50)),
                ('frecuencia_medicamento', models.CharField(max_length=50)),
                ('dosis', models.CharField(max_length=50)),
                ('duracion_medicamento', models.IntegerField(help_text='Duración del tratamiento en días')),
            ],
            options={
                'verbose_name': 'Receta',
                'verbose_name_plural': 'Recetas',
            },
        ),
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id_doctor', models.AutoField(primary_key=True, serialize=False)),
                ('rut_doctor', models.CharField(max_length=12)),
                ('nombre_doctor', models.CharField(max_length=50)),
                ('correo_doctor', models.EmailField(max_length=254, unique=True)),
                ('telefono_doctor', models.CharField(max_length=15)),
                ('sexo_doctor', models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')], max_length=1)),
                ('especialidad', models.ManyToManyField(related_name='doctores', to='api.especialidad')),
            ],
            options={
                'verbose_name': 'Doctor',
                'verbose_name_plural': 'Doctores',
            },
        ),
        migrations.CreateModel(
            name='HorarioDisponible',
            fields=[
                ('id_disponibilidad', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_disponible', models.DateField()),
                ('hora_inicio_dispo', models.TimeField()),
                ('hora_termino_dispo', models.TimeField()),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.doctor')),
            ],
            options={
                'verbose_name': 'Horario Disponible',
                'verbose_name_plural': 'Horarios Disponibles',
            },
        ),
        migrations.CreateModel(
            name='Cita',
            fields=[
                ('id_cita', models.AutoField(primary_key=True, serialize=False)),
                ('estado_cita', models.CharField(choices=[('P', 'Pendiente'), ('C', 'Cancelada'), ('R', 'Realizada')], max_length=1)),
                ('disponible', models.BooleanField(default=True)),
                ('descripcion_cita', models.CharField(max_length=100)),
                ('motivo_cancelacion', models.TextField(blank=True, null=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.doctor')),
                ('disponibilidad_cita', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.horariodisponible')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.paciente')),
            ],
            options={
                'verbose_name': 'Cita',
                'verbose_name_plural': 'Citas',
            },
        ),
        migrations.CreateModel(
            name='FichaMedica',
            fields=[
                ('id_fichaPaciente', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_sangre', models.CharField(max_length=3)),
                ('alergias', models.TextField()),
                ('estatura', models.FloatField()),
                ('peso', models.FloatField()),
                ('cond_especiales', models.TextField()),
                ('enf_cronicas', models.TextField()),
                ('cirugias', models.TextField()),
                ('vacunas', models.TextField()),
                ('antecedentes_fam', models.TextField()),
                ('cita', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.cita')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.paciente')),
            ],
            options={
                'verbose_name': 'Ficha Médica',
                'verbose_name_plural': 'Fichas Médicas',
            },
        ),
        migrations.CreateModel(
            name='HistorialPaciente',
            fields=[
                ('id_historial', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_tratamiento', models.DateField()),
                ('diagnostico', models.TextField()),
                ('observaciones_consulta', models.TextField()),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.doctor')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.paciente')),
                ('receta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.receta')),
            ],
            options={
                'verbose_name': 'Historial del Paciente',
                'verbose_name_plural': 'Historiales de Pacientes',
            },
        ),
    ]
