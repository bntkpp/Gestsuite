import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
import requests

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Botones para navegar entre opciones
        self.register_button = Button(text='Registrar Usuario')
        self.register_button.bind(on_press=self.go_to_register)
        layout.add_widget(self.register_button)

        self.patient_button = Button(text='Gestionar Pacientes')
        self.patient_button.bind(on_press=self.go_to_patients)
        layout.add_widget(self.patient_button)

        self.doctor_button = Button(text='Gestionar Doctores')
        self.doctor_button.bind(on_press=self.go_to_doctors)
        layout.add_widget(self.doctor_button)

        self.add_widget(layout)

    def go_to_register(self, instance):
        self.manager.current = 'register'

    def go_to_patients(self, instance):
        self.manager.current = 'patients'

    def go_to_doctors(self, instance):
        self.manager.current = 'doctors'


class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.username_input = TextInput(hint_text='Username')
        self.email_input = TextInput(hint_text='Email')
        self.password_input = TextInput(hint_text='Password', password=True)

        layout.add_widget(self.username_input)
        layout.add_widget(self.email_input)
        layout.add_widget(self.password_input)

        self.register_button = Button(text='Registrar Usuario')
        self.register_button.bind(on_press=self.register_user)
        layout.add_widget(self.register_button)

        self.label = Label(text='Respuesta de la API aparecerá aquí.')
        layout.add_widget(self.label)

        back_button = Button(text='Volver al Menú')
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def register_user(self, instance):
        url = 'http://127.0.0.1:8000/api/register/'
        data = {
            'username': self.username_input.text,
            'email': self.email_input.text,
            'password': self.password_input.text
        }
        try:
            response = requests.post(url, json=data)
            self.label.text = f'Status Code: {response.status_code}\nResponse: {response.text}'
        except requests.exceptions.RequestException as e:
            self.label.text = f'Error: {e}'

    def go_back(self, instance):
        self.manager.current = 'menu'


class PatientScreen(Screen):
    def __init__(self, **kwargs):
        super(PatientScreen, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.rut_input = TextInput(hint_text='RUT Paciente')
        self.nombre_input = TextInput(hint_text='Nombre Paciente')
        self.direccion_input = TextInput(hint_text='Dirección Paciente')
        self.fecha_nacimiento_input = TextInput(hint_text='Fecha Nacimiento (YYYY-MM-DD)')
        self.sexo_input = TextInput(hint_text='Sexo Paciente')
        self.correo_input = TextInput(hint_text='Correo Paciente')
        self.telefono_input = TextInput(hint_text='Teléfono Paciente')

        layout.add_widget(self.rut_input)
        layout.add_widget(self.nombre_input)
        layout.add_widget(self.direccion_input)
        layout.add_widget(self.fecha_nacimiento_input)
        layout.add_widget(self.sexo_input)
        layout.add_widget(self.correo_input)
        layout.add_widget(self.telefono_input)

        self.register_button = Button(text='Registrar Paciente')
        self.register_button.bind(on_press=self.register_patient)
        layout.add_widget(self.register_button)

        self.label = Label(text='Respuesta de la API aparecerá aquí.')
        layout.add_widget(self.label)

        back_button = Button(text='Volver al Menú')
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def register_patient(self, instance):
        url = 'http://127.0.0.1:8000/api/paciente/create/'  # Cambia la URL según tu API
        data = {
            'rut_paciente': self.rut_input.text,
            'nombre_paciente': self.nombre_input.text,
            'direccion_paciente': self.direccion_input.text,
            'fecha_nacimiento': self.fecha_nacimiento_input.text,
            'sexo_paciente': self.sexo_input.text,
            'correo_paciente': self.correo_input.text,
            'telefono_paciente': self.telefono_input.text
        }
        try:
            response = requests.post(url, json=data)
            self.label.text = f'Status Code: {response.status_code}\nResponse: {response.text}'
        except requests.exceptions.RequestException as e:
            self.label.text = f'Error: {e}'

    def go_back(self, instance):
        self.manager.current = 'menu'


class DoctorScreen(Screen):
    def __init__(self, **kwargs):
        super(DoctorScreen, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.rut_input = TextInput(hint_text='RUT Doctor')
        self.nombre_input = TextInput(hint_text='Nombre Doctor')
        self.correo_input = TextInput(hint_text='Correo Doctor')
        self.telefono_input = TextInput(hint_text='Teléfono Doctor')
        self.sexo_input = TextInput(hint_text='Sexo Doctor')

        layout.add_widget(self.rut_input)
        layout.add_widget(self.nombre_input)
        layout.add_widget(self.correo_input)
        layout.add_widget(self.telefono_input)
        layout.add_widget(self.sexo_input)

        self.register_button = Button(text='Registrar Doctor')
        self.register_button.bind(on_press=self.register_doctor)
        layout.add_widget(self.register_button)

        self.label = Label(text='Respuesta de la API aparecerá aquí.')
        layout.add_widget(self.label)

        back_button = Button(text='Volver al Menú')
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def register_doctor(self, instance):
        url = 'http://127.0.0.1:8000/api/doctor/create/'  # Cambia la URL según tu API
        data = {
            'rut_doctor': self.rut_input.text,
            'nombre_doctor': self.nombre_input.text,
            'correo_doctor': self.correo_input.text,
            'telefono_doctor': self.telefono_input.text,
            'sexo_doctor': self.sexo_input.text
        }
        try:
            response = requests.post(url, json=data)
            self.label.text = f'Status Code: {response.status_code}\nResponse: {response.text}'
        except requests.exceptions.RequestException as e:
            self.label.text = f'Error: {e}'

    def go_back(self, instance):
        self.manager.current = 'menu'


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(PatientScreen(name='patients'))
        sm.add_widget(DoctorScreen(name='doctors'))
        return sm


if __name__ == '__main__':
    MyApp().run()





