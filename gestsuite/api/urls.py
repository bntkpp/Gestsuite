from django.urls import path
from dal import autocomplete
from . import views
from .models import Paciente, Doctor, HistorialPaciente
from .views import PacienteAutocomplete, DoctorAutocomplete, HistorialPacienteAutocomplete, get_csrf

urlpatterns = [
    path('get_csrf/', views.get_csrf, name='get_csrf'),

    path('register/', views.UserRegister.as_view(), name='register'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('logout/', views.UserLogout.as_view(), name='logout'),
    path('profile/', views.UserView.as_view(), name='profile'),

    path('paciente/', views.lista_pacientes_api, name='lista_pacientes_api'),
    path('paciente/<int:pk>/', views.PacienteDetailView.as_view(), name='paciente_detail'),
    path('paciente/create/', views.PacienteCreateView.as_view(), name='paciente_create'),
    path("paciente/update/<int:id>/", views.paciente_update, name='paciente_update'),
    path("paciente/delete/<int:id>/", views.paciente_delete, name='paciente_delete'),
    path("paciente/buscar/<str:rut>/", views.buscar_id, name="buscar_id"),

    path('doctor/', views.lista_doctores_api, name='lista_doctores_api'),
    path('doctor/<int:pk>/', views.DoctorDetailView.as_view(), name='doctor_detail'),
    path('doctor/create/', views.DoctorCreateView.as_view(), name='doctor_create'),
    path('doctor/update/<int:pk>/', views.DoctorUpdateView.as_view(), name='doctor_update'),
    path('doctor/delete/<int:pk>/', views.DoctorDeleteView.as_view(), name='doctor_delete'),

    path('horario/', views.lista_horariodisponible_api, name='lista_horariodisponible_api'),
    

    path('historialpaciente/', views.HistorialPacienteListView.as_view(), name='historialpaciente_list'),
    path('historialpaciente/create/', views.HistorialPacienteCreateView.as_view(), name='historialpaciente_create'),
    path('historialpaciente/update/<int:pk>/', views.HistorialPacienteUpdateView.as_view(), name='historialpaciente_update'),
    path('historialpaciente/delete/<int:pk>/', views.HistorialPacienteDeleteView.as_view(), name='historialpaciente_delete'),
    
    path('cita/', views.CitaListView.as_view(), name='cita_list'),
    path('cita/<int:pk>/', views.CitaDetailView.as_view(), name='cita_detail'),
    path('cita/create/', views.CitaCreateView.as_view(), name='cita_create'),
    path('cita/update/<int:pk>/', views.CitaUpdateView.as_view(), name='cita_update'),
    path('cita/delete/<int:pk>/', views.CitaDeleteView.as_view(), name='cita_delete'),
    
    path('receta/', views.RecetaListView.as_view(), name='receta_list'),
    path('receta/create/', views.RecetaCreateView.as_view(), name='receta_create'),
    path('receta/update/<int:pk>/', views.RecetaUpdateView.as_view(), name='receta_update'),
    path('receta/delete/<int:pk>/', views.RecetaDeleteView.as_view(), name='receta_delete'),

    path('fichamedica/', views.FichaMedicaListView.as_view(), name='fichamedica_list'),
    path('fichamedica/create/', views.FichaMedicaCreateView.as_view(), name='fichamedica_create'),
    path('fichamedica/update/<int:pk>/', views.FichaMedicaUpdateView.as_view(), name='fichamedica_update'),
    path('fichamedica/delete/<int:pk>/', views.FichaMedicaDeleteView.as_view(), name='fichamedica_delete'),
    
    path('paciente-autocomplete/', PacienteAutocomplete.as_view(), name='paciente-autocomplete'),
    path('doctor-autocomplete/', DoctorAutocomplete.as_view(), name='doctor-autocomplete'),
    path('historialpaciente-autocomplete/', HistorialPacienteAutocomplete.as_view(), name='historialpaciente-autocomplete'),

]