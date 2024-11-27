import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, login, logout
from django.core.exceptions import ValidationError
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import UserRegisterSerializer, UserLoginSerializer, UserSerializer
from rest_framework import permissions, status
from .validations import custom_validation, validate_username, validate_password
from .models import Receta, Especialidad, Paciente, Doctor, HorarioDisponible, Cita, HistorialPaciente, FichaMedica
from .forms import RecetaForm, EspecialidadForm, PacienteForm, DoctorForm, HorarioDisponibleForm, CitaForm, HistorialPacienteForm, FichaMedicaForm
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib import messages
from dal import autocomplete
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from django.views import View


@ensure_csrf_cookie
def get_csrf(request):
    return JsonResponse({"message": "Token CSRF obtenido correctamente"})

class UserRegister(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        clean_data = custom_validation(request.data)
        serializer = UserRegisterSerializer(data=clean_data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(clean_data)
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

class UserLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)
    def post(self, request):
        data = request.data
        if not validate_username(data):
            raise ValidationError('Nombre de usuario no válido')
        if not validate_password(data):
            raise ValidationError('Contraseña no válida')
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(data)
            login(request, user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        

class UserLogout(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)

class UserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)

class PacienteListView(ListView):
    model = Paciente
    context_object_name = 'pacientes'
    template_name = 'paciente_list.html' #donde se va a mostrar la lista de pacientes

def lista_pacientes_api(request):
    """
    Endpoint para devolver la lista de pacientes en formato JSON.
    """
    pacientes = Paciente.objects.all().values(
        'id_paciente','rut_paciente', 'nombre_paciente', 'direccion_paciente', 
        'fecha_nacimiento', 'sexo_paciente', 'correo_paciente', 'telefono_paciente'
    )
    return JsonResponse(list(pacientes), safe=False)    

class PacienteDetailView(DetailView):
    model = Paciente
    context_object_name = 'paciente'
    template_name = 'paciente_detail.html'

class PacienteCreateView(CreateView):
    model = Paciente
    form_class = PacienteForm #formulario que se va a usar 
    template_name = 'paciente_create.html' #donde se va a mostrar el formulario
    success_url = reverse_lazy('http://127.0.0.1:8000/api/paciente/') #redirigir a la lista de pacientes


def paciente_update(request, id):
    paciente = get_object_or_404(Paciente, id_paciente=id)
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            paciente.rut = data.get('rut_paciente', paciente.rut_paciente)
            paciente.nombre_paciente = data.get('nombre_paciente', paciente.nombre_paciente)
            paciente.direccion_paciente = data.get('direccion_paciente', paciente.direccion_paciente)
            paciente.fecha_nacimiento = data.get('fecha_nacimiento', paciente.fecha_nacimiento)
            paciente.sexo_paciente = data.get('sexo_paciente', paciente.sexo_paciente)
            paciente.correo_paciente = data.get('correo_paciente', paciente.correo_paciente)
            paciente.telefono_paciente = data.get('telefono_paciente', paciente.telefono_paciente)
            paciente.save()
            return JsonResponse({'message': 'Paciente actualizado exitosamente.'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Error al decodificar JSON.'}, status=400)
    return JsonResponse({'error': 'Método no permitido.'}, status=405)

def paciente_delete(request, id):
    if request.method == 'DELETE':
        try:
            paciente = get_object_or_404(Paciente, id_paciente=id)
            paciente.delete()
            return JsonResponse({"message": "Paciente eliminado exitosamente"}, status=204)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "Método no permitido"}, status=405)

def buscar_id(request, rut):
    try:
        paciente = get_object_or_404(Paciente, rut_paciente=rut)
        return JsonResponse({"id": paciente.id_paciente}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=404)

def delete_paciente(request, rut_paciente):
    if request.method == 'DELETE':
        try:
            paciente = Paciente.objects.get(rut_paciente=rut_paciente)
            paciente.delete()
            return JsonResponse({"message": "Paciente eliminado exitosamente."}, status=204)
        except Paciente.DoesNotExist:
            return JsonResponse({"error": "Paciente no encontrado."}, status=404)

class PacienteAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Paciente.objects.none()

        datos = Paciente.objects.all()

        if self.q:
            # Buscar por RUT
            datos = datos.filter(rut_paciente__icontains=self.q)

        return datos

    def get_result_label(self, result):
        # Mostrar el nombre en el autocompletado, pero buscar por RUT
        return f'{result.rut_paciente} - {result.nombre_paciente}'

#CRUD DOCTOR

class DoctorListView(ListView):
    model = Doctor
    context_object_name = 'doctores'
    template_name = 'doctor/doctor_list.html'

def lista_doctores_api(request):
    """
    Endpoint para devolver la lista de pacientes en formato JSON.
    """
    doctores = Doctor.objects.all().values(
        'id_doctor','rut_doctor', 'nombre_doctor', 'correo_doctor', 'telefono_doctor',
        'sexo_doctor'
    )
    return JsonResponse(list(doctores), safe=False)    

class DoctorDetailView(DetailView):
    model = Doctor
    context_object_name = 'doctores'
    template_name = 'doctor/doctor_detail.html'

class DoctorCreateView(CreateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'doctor/doctor_form.html'
    success_url = reverse_lazy('doctor_list')

class DoctorUpdateView(UpdateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'doctor/doctor_form.html'
    success_url = reverse_lazy('doctor_list')

class DoctorDeleteView(DeleteView):
    model = Doctor
    template_name = 'doctor/doctor_delete.html'
    success_url = reverse_lazy('doctor_list')

class DoctorAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Doctor.objects.none()

        datos = Doctor.objects.all()

        if self.q:
           
            datos = datos.filter(rut_doctor__icontains=self.q)

        return datos

    def get_result_label(self, result):

        return f'{result.rut_doctor} - {result.nombre_doctor}'


#CRUD CITA

class CitaListView(ListView):
    model = Cita
    context_object_name = 'citas'
    template_name = 'cita/cita_list.html'

    def citas_disponibles(self):
        return Cita.objects.filter(disponible=True)

class CitaDetailView(DetailView):
    model = Cita
    context_object_name = 'citas'
    template_name = 'cita/cita_detail.html'

class CitaCreateView(CreateView):
    model = Cita
    form_class = CitaForm
    template_name = 'cita/cita_form.html'
    success_url = reverse_lazy('cita_list')

    def validar_cita(self, form):
        paciente = form.cleaned_data.get('paciente')
        fecha = form.cleaned_data.get('fecha')
        cita_existente = Cita.objects.filter(paciente=paciente, fecha=fecha, disponible=True).first() #si no encuentra nada devuelve None
        if cita_existente:
            cita_existente.disponible = False
            cita_existente.save()
            messages.error(self.request, 'Un paciente ya tiene una cita en esa fecha')
            return self.form_invalid(form)
        else:
            return super().form_valid(form)

class CitaUpdateView(UpdateView):
    model = Cita
    form_class = CitaForm
    template_name = 'cita/cita_form.html'
    success_url = reverse_lazy('cita_list')

class CitaDeleteView(DeleteView):
    model = Cita
    template_name = 'cita/cita_delete.html'
    success_url = reverse_lazy('cita_list')

#CRUD HISTORIAL PACIENTE

class HistorialPacienteListView(ListView):
    model = HistorialPaciente
    context_object_name = 'historiales'
    template_name = 'historial_paciente/historial_paciente_list.html'

class HistorialPacienteCreateView(CreateView):
    model = HistorialPaciente
    form_class = HistorialPacienteForm
    template_name = 'historial_paciente/historial_paciente_form.html'
    success_url = reverse_lazy('historial_paciente_list')

class HistorialPacienteUpdateView(UpdateView):
    model = HistorialPaciente
    form_class = HistorialPacienteForm
    template_name = 'historial_paciente/historial_paciente_form.html'
    success_url = reverse_lazy('historial_paciente_list')

class HistorialPacienteDeleteView(DeleteView):
    model = HistorialPaciente
    template_name = 'historial_paciente/historial_paciente_delete.html'
    success_url = reverse_lazy('historial_paciente_list')

class HistorialPacienteAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return HistorialPaciente.objects.none()

        datos = HistorialPaciente.objects.all()

        if self.q:
            
            datos = datos.filter(paciente__rut_paciente__icontains=self.q)

        return datos

    def get_result_label(self, result):
        # Mostrar el nombre del paciente en el historial
        return f'{result.paciente.rut_paciente} - {result.paciente.nombre_paciente}'

#CRUD RECETA

class RecetaListView(ListView):
    model = Receta
    context_object_name = 'recetas'
    template_name = 'receta/receta_list.html'

class RecetaCreateView(CreateView):
    model = Receta
    form_class = RecetaForm
    template_name = 'receta/receta_form.html'
    success_url = reverse_lazy('receta_list')

class RecetaUpdateView(UpdateView):
    model = Receta
    form_class = RecetaForm
    template_name = 'receta/receta_form.html'
    success_url = reverse_lazy('receta_list')

class RecetaDeleteView(DeleteView):
    model = Receta
    template_name = 'receta/receta_delete.html'
    success_url = reverse_lazy('receta_list')

#CRUD ESPECIALIDAD

class EspecialidadListView(ListView):
    model = Especialidad
    context_object_name = 'especialidades'
    template_name = 'especialidad/especialidad_list.html'

class EspecialidadCreateView(CreateView):
    model = Especialidad
    form_class = EspecialidadForm
    template_name = 'especialidad/especialidad_form.html'
    success_url = reverse_lazy('especialidad_list')

class EspecialidadUpdateView(UpdateView):
    model = Especialidad
    form_class = EspecialidadForm
    template_name = 'especialidad/especialidad_form.html'
    success_url = reverse_lazy('especialidad_list')

class EspecialidadDeleteView(DeleteView):
    model = Especialidad
    template_name = 'especialidad/especialidad_delete.html'
    success_url = reverse_lazy('especialidad_list')

#CRUD HORARIO DISPONIBLE

class HorarioDisponibleListView(ListView):
    model = HorarioDisponible
    context_object_name = 'horarios'
    template_name = 'horario_disponible/horario_disponible_list.html'

def lista_horariodisponible_api(request):
    """
    Endpoint para devolver la lista de pacientes en formato JSON.
    """
    horarios = HorarioDisponible.objects.all().values(
        'id_disponibilidad','fecha_disponible', 'hora_inicio_dispo', 
        'hora_termino_dispo', 'doctor'
    )
    return JsonResponse(list(horarios), safe=False)    

def filtrar_horarios(request):
    doctor_id = request.GET.get('doctor_id')  # Obtener el parámetro de la URL
    if not doctor_id:
        return JsonResponse({"error": "Se debe proporcionar doctor_id"}, status=400)
    
    horarios = HorarioDisponible.objects.filter(doctor_id=doctor_id)
    resultados = [
        {
            "id_disponibilidad": horario.id_disponibilidad,
            "fecha_disponible": horario.fecha_disponible.strftime("%Y-%m-%d"),
            "hora_inicio_dispo": horario.hora_inicio_dispo.strftime("%H:%M"),
            "hora_termino_dispo": horario.hora_termino_dispo.strftime("%H:%M"),
        }
        for horario in horarios
    ]
    return JsonResponse(resultados, safe=False)

class HorarioDisponibleCreateView(CreateView):
    model = HorarioDisponible
    form_class = HorarioDisponibleForm
    template_name = 'horario_disponible/horario_disponible_form.html'
    success_url = reverse_lazy('horario_disponible_list')

class HorarioDisponibleUpdateView(UpdateView):
    model = HorarioDisponible
    form_class = HorarioDisponibleForm
    template_name = 'horario_disponible/horario_disponible_form.html'
    success_url = reverse_lazy('horario_disponible_list')

class HorarioDisponibleDeleteView(DeleteView):
    model = HorarioDisponible
    template_name = 'horario_disponible/horario_disponible_delete.html'
    success_url = reverse_lazy('horario_disponible_list')

#CRUD FICHA MEDICA

class FichaMedicaListView(ListView):
    model = FichaMedica
    context_object_name = 'fichas'
    template_name = 'ficha_medica/ficha_medica_list.html'

class FichaMedicaCreateView(CreateView):
    model = FichaMedica
    form_class = FichaMedicaForm
    template_name = 'ficha_medica/ficha_medica_form.html'
    success_url = reverse_lazy('ficha_medica_list')

class FichaMedicaUpdateView(UpdateView):
    model = FichaMedica
    form_class = FichaMedicaForm
    template_name = 'ficha_medica/ficha_medica_form.html'
    success_url = reverse_lazy('ficha_medica_list')

class FichaMedicaDeleteView(DeleteView):
    model = FichaMedica
    template_name = 'ficha_medica/ficha_medica_delete.html'
    success_url = reverse_lazy('ficha_medica_list')