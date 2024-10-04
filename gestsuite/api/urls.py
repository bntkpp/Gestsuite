from django.urls import path
from dal import autocomplete
from . import views
from .models import Paciente, Doctor, HistorialPaciente
from .views import PacienteAutocomplete, DoctorAutocomplete, HistorialPacienteAutocomplete

urlpatterns = [
    path('register/', views.UserRegister.as_view(), name='register'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('logout/', views.UserLogout.as_view(), name='logout'),
    path('profile/', views.UserView.as_view(), name='profile'),
    path('paciente-autocomplete/', PacienteAutocomplete.as_view(), name='paciente-autocomplete'),
    path('doctor-autocomplete/', DoctorAutocomplete.as_view(), name='doctor-autocomplete'),
    path('historialpaciente-autocomplete/', HistorialPacienteAutocomplete.as_view(), name='historialpaciente-autocomplete'),

]