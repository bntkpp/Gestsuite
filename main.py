from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
import requests  # Para llamadas a la API


# Clase base para pantallas que necesitan token CSRF
class CSRFScreen(Screen):
    csrf_token = None

    def obtener_csrf_token(self):
        try:
            response = requests.get("http://127.0.0.1:8000/api/get_csrf/")
            if response.status_code == 200:
                self.csrf_token = response.cookies['csrftoken']
            else:
                return "Error al obtener el token CSRF"
        except Exception as e:
            return f"Error de conexión al obtener el token CSRF: {str(e)}"
        return None

# Pantalla de Inicio de Sesión
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.username = TextInput(hint_text='Usuario', multiline=False)
        self.password = TextInput(hint_text='Contraseña', multiline=False, password=True)
        self.message = Label(text="Ingrese sus credenciales")
        login_btn = Button(text="Iniciar Sesión", on_press=self.validate_login)
        
        layout.add_widget(self.username)
        layout.add_widget(self.password)
        layout.add_widget(self.message)
        layout.add_widget(login_btn)
        self.add_widget(layout)

    def validate_login(self, instance):
        username = self.username.text
        password = self.password.text
        # Simulación de validación
        if username == "admin" and password == "admin":
            self.manager.current = "menu"
        else:
            self.message.text = "Credenciales incorrectas"

# Menú Principal
class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        
        pacientes_btn = Button(text="Gestión de Pacientes", on_press=self.goto_pacientes)
        doctores_btn = Button(text="Gestión de Doctores", on_press=self.goto_doctores)
        citas_btn = Button(text="Agendar Citas", on_press=self.goto_cita)
        ficha_btn = Button(text="Fichas Médicas", on_press=self.goto_ficha)
        receta_btn = Button(text="Recetas Médicas", on_press=self.goto_receta)
        
        layout.add_widget(pacientes_btn)
        layout.add_widget(doctores_btn)
        layout.add_widget(citas_btn)
        layout.add_widget(ficha_btn)
        layout.add_widget(receta_btn)
        self.add_widget(layout)

    def goto_pacientes(self, instance):
        self.manager.current = "paciente"

    def goto_doctores(self, instance):
        self.manager.current = "doctor"

    def goto_cita(self, instance):
        self.manager.current = "cita"

    def goto_ficha(self, instance):
        self.manager.current = "crear_ficha"

    def goto_receta(self, instance):
        self.manager.current = "crear_receta"

# Pantalla para Registrar Paciente
class PacienteScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")
        
        btn_back = Button(
            text="Volver", 
            size_hint_y=None, 
            height=50, 
            on_press=self.goto_menu
        )
        
        # Botón para Crear
        btn_create = Button(text="Crear Paciente", on_press=self.goto_create)
        # Botón para Leer
        btn_read = Button(text="Leer Pacientes", on_press=self.goto_read)
        # Botón para Actualizar
        btn_update = Button(text="Actualizar Paciente", on_press=self.goto_update)
        # Botón para Eliminar
        btn_delete = Button(text="Eliminar Paciente", on_press=self.goto_delete)

        # Agregar botones al layout
        layout.add_widget(btn_back)
        layout.add_widget(btn_create)
        layout.add_widget(btn_read)
        layout.add_widget(btn_update)
        layout.add_widget(btn_delete)

        self.add_widget(layout)

    def goto_menu(self, instance):
        self.manager.current = "menu"

    def goto_create(self, instance):
        self.manager.current = "create_paciente"

    def goto_read(self, instance):
        self.manager.current = "read_paciente"

    def goto_update(self, instance):
        # Aquí deberías seleccionar un RUT previamente
        rut_seleccionado = "21745232-5"  # Esto debería venir de tu lógica de selección
        update_screen = self.manager.get_screen("update_paciente")
        update_screen.buscar_paciente(rut_seleccionado)
        self.manager.current = "update_paciente"

    def goto_delete(self, instance):
        self.manager.current = "delete_paciente"

# Pantalla para Crear Paciente
class CreatePacienteScreen(CSRFScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        
        self.nombre = TextInput(hint_text='Nombre del Paciente')
        self.rut = TextInput(hint_text='RUT')
        self.direccion = TextInput(hint_text='Dirección')
        self.fecha_nacimiento = TextInput(hint_text='Fecha de Nacimiento (YYYY-MM-DD)')
        self.sexo = TextInput(hint_text='Sexo (M/F/O)')
        self.correo = TextInput(hint_text='Correo Electrónico')
        self.telefono = TextInput(hint_text='Teléfono')
        self.message = Label(text="")

        btn_guardar = Button(text="Guardar", on_press=self.guardar_paciente)
        btn_cancelar = Button(text="Cancelar", on_press=self.cancelar)

        # Agregar todos los widgets al layout
        layout.add_widget(self.nombre)
        layout.add_widget(self.rut)
        layout.add_widget(self.direccion)
        layout.add_widget(self.fecha_nacimiento)
        layout.add_widget(self.sexo)
        layout.add_widget(self.correo)
        layout.add_widget(self.telefono)
        layout.add_widget(self.message)
        layout.add_widget(btn_guardar)
        layout.add_widget(btn_cancelar)

        self.add_widget(layout)

        error = self.obtener_csrf_token()
        if error:
            self.message.text = error

    def guardar_paciente(self, instance):
        if not self.csrf_token:
            self.message.text = "Error: no se ha obtenido el token CSRF"
            return

        data = {
            "nombre_paciente": self.nombre.text,
            "rut_paciente": self.rut.text,
            "direccion_paciente": self.direccion.text,
            "fecha_nacimiento": self.fecha_nacimiento.text,
            "sexo_paciente": self.sexo.text,
            "correo_paciente": self.correo.text,
            "telefono_paciente": self.telefono.text
        }
        headers = {
            "X-CSRFToken": self.csrf_token
        }

        try:
            response = requests.post(
                "http://127.0.0.1:8000/api/paciente/create/",
                data=data,
                headers=headers,
                cookies={"csrftoken": self.csrf_token}
            )
            if response.status_code == 201:
                self.message.text = "Paciente creado exitosamente"
                self.limpiar_formulario()
                self.manager.current = "paciente"
            else:
                self.message.text = f"Error al crear paciente: {response.status_code}"
        except Exception as e:
            self.message.text = f"Error de conexión: {str(e)}"

    def limpiar_formulario(self):
        self.nombre.text = ""
        self.rut.text = ""
        self.direccion.text = ""
        self.fecha_nacimiento.text = ""
        self.sexo.text = ""
        self.correo.text = ""
        self.telefono.text = ""

    def cancelar(self, instance):
        self.limpiar_formulario()
        self.manager.current = "paciente"

# Pantalla para Leer Pacientes
class ReadPacienteScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")
        
        # Mensaje de estado
        self.message = Label(text="Cargando pacientes...")
        layout.add_widget(self.message)
        
        # Lista de pacientes
        self.lista = BoxLayout(orientation="vertical", size_hint_y=None)
        layout.add_widget(self.lista)
        
        # Botón Volver
        btn_volver = Button(text="Volver", size_hint_y=None, height=50, on_press=self.volver)
        layout.add_widget(btn_volver)

        self.add_widget(layout)

        # Cargar pacientes
        self.cargar_pacientes()

    def cargar_pacientes(self):
        try:
            response = requests.get("http://127.0.0.1:8000/api/paciente/")
            if response.status_code == 200:
                pacientes = response.json()
                self.lista.clear_widgets()
                for paciente in pacientes:
                    label = Label(
                        text=f"{paciente['nombre_paciente']} - {paciente['rut_paciente']} - {paciente['direccion_paciente']} - {paciente['fecha_nacimiento']} - {paciente['sexo_paciente']} - {paciente['correo_paciente']} - {paciente['telefono_paciente']}"
                    )
                    self.lista.add_widget(label)
                self.message.text = "Pacientes cargados exitosamente"
            else:
                self.message.text = f"Error al cargar pacientes: {response.status_code}"
        except Exception as e:
            self.message.text = f"Error de conexión: {str(e)}"

    def volver(self, instance):
        self.manager.current = "paciente"  # Regresa a la pantalla de gestión de pacientes

# Pantalla para Actualizar Paciente
class UpdatePacienteScreen(CSRFScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")
        
        # Entrada para buscar paciente
        self.rut = TextInput(hint_text="RUT del Paciente", multiline=False)
        self.message = Label(text="Ingrese el RUT para buscar los datos del paciente.")
        
        btn_buscar = Button(text="Buscar Paciente", on_press=self.buscar_paciente)
        
        # Campos para editar datos del paciente
        self.nombre = TextInput(hint_text="Nombre del Paciente")
        self.direccion = TextInput(hint_text="Dirección")
        self.fecha_nacimiento = TextInput(hint_text="Fecha de Nacimiento (YYYY-MM-DD)")
        self.sexo = TextInput(hint_text="Sexo (M/F/O)")
        self.correo = TextInput(hint_text="Correo Electrónico")
        self.telefono = TextInput(hint_text="Teléfono")

        # Botones para actualizar o cancelar
        btn_actualizar = Button(text="Actualizar Paciente", on_press=self.actualizar_paciente)
        btn_cancelar = Button(text="Cancelar", on_press=self.cancelar)

        # Agregar widgets al layout
        layout.add_widget(self.rut)
        layout.add_widget(btn_buscar)
        layout.add_widget(self.message)
        layout.add_widget(self.nombre)
        layout.add_widget(self.direccion)
        layout.add_widget(self.fecha_nacimiento)
        layout.add_widget(self.sexo)
        layout.add_widget(self.correo)
        layout.add_widget(self.telefono)
        layout.add_widget(btn_actualizar)
        layout.add_widget(btn_cancelar)

        self.add_widget(layout)

        error = self.obtener_csrf_token()
        if error:
            self.message.text = error

        # Variable para almacenar el ID del paciente
        self.id_paciente = None

    def buscar_paciente(self, instance):
        """
        Buscar datos del paciente por RUT y rellenar el formulario.
        """
        rut = self.rut.text.strip()
        if not rut:
            self.message.text = "Por favor, ingrese un RUT válido."
            return

        try:
            # Obtener el ID del paciente por su RUT
            response = requests.get(f"http://127.0.0.1:8000/api/paciente/buscar/{rut}/")
            if response.status_code == 200:
                data = response.json()
                self.id_paciente = data.get("id")
                if self.id_paciente:
                    # Obtener datos completos del paciente por ID
                    response = requests.get(f"http://127.0.0.1:8000/api/paciente/{self.id_paciente}/")
                    if response.status_code == 200:
                        paciente = response.json()
                        self.nombre.text = paciente["nombre_paciente"]
                        self.direccion.text = paciente["direccion_paciente"]
                        self.fecha_nacimiento.text = paciente["fecha_nacimiento"]
                        self.sexo.text = paciente["sexo_paciente"]
                        self.correo.text = paciente["correo_paciente"]
                        self.telefono.text = paciente["telefono_paciente"]
                        self.message.text = "Datos del paciente cargados."
                    else:
                        self.message.text = f"Error al cargar datos del paciente: {response.status_code}"
                else:
                    self.message.text = "Paciente no encontrado."
            else:
                self.message.text = f"Error al buscar paciente: {response.status_code}"
        except Exception as e:
            self.message.text = f"Error de conexión: {str(e)}"

    def actualizar_paciente(self, instance):
        """
        Enviar los datos actualizados del paciente al backend.
        """
        if not self.id_paciente:
            self.message.text = "Debe buscar un paciente antes de actualizar."
            return

        if not self.csrf_token:
            self.message.text = "Error: no se ha obtenido el token CSRF."
            return

        data = {
            "nombre_paciente": self.nombre.text,
            "direccion_paciente": self.direccion.text,
            "fecha_nacimiento": self.fecha_nacimiento.text,
            "sexo_paciente": self.sexo.text,
            "correo_paciente": self.correo.text,
            "telefono_paciente": self.telefono.text,
        }
        headers = {
            "Content-Type": "application/json",
            "X-CSRFToken": self.csrf_token
        }

        try:
            response = requests.put(
                f"http://127.0.0.1:8000/api/paciente/update/{self.id_paciente}/",
                json=data,
                headers=headers,
                cookies={"csrftoken": self.csrf_token}
            )
            if response.status_code == 200:
                self.message.text = "Paciente actualizado exitosamente."
            else:
                self.message.text = f"Error al actualizar paciente: {response.status_code}"
        except Exception as e:
            self.message.text = f"Error de conexión: {str(e)}"

    def cancelar(self, instance):
        """
        Limpiar campos y regresar a la pantalla anterior.
        """
        self.rut.text = ""
        self.nombre.text = ""
        self.direccion.text = ""
        self.fecha_nacimiento.text = ""
        self.sexo.text = ""
        self.correo.text = ""
        self.telefono.text = ""
        self.id_paciente = None
        self.message.text = ""
        self.manager.current = "paciente"

# Pantalla para Eliminar Paciente
class DeletePacienteScreen(CSRFScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")
        
        self.rut = TextInput(hint_text="RUT del Paciente a Eliminar", multiline=False)
        self.message = Label(text="Ingrese el RUT del paciente para buscar y eliminar.")
        
        btn_buscar = Button(text="Buscar ID por RUT", on_press=self.buscar_id_paciente)
        btn_eliminar = Button(text="Eliminar Paciente", on_press=self.eliminar_paciente)
        btn_cancelar = Button(text="Cancelar", on_press=self.cancelar)

        layout.add_widget(self.rut)
        layout.add_widget(btn_buscar)
        layout.add_widget(self.message)
        layout.add_widget(btn_eliminar)
        layout.add_widget(btn_cancelar)

        self.add_widget(layout)

        error = self.obtener_csrf_token()
        if error:
            self.message.text = error

        self.id_paciente = None

    def buscar_id_paciente(self, instance):
        rut = self.rut.text.strip()
        if not rut:
            self.message.text = "Por favor, ingrese un RUT válido."
            return

        try:
            response = requests.get(f"http://127.0.0.1:8000/api/paciente/buscar/{rut}/")
            if response.status_code == 200:
                self.id_paciente = response.json().get("id")
                if self.id_paciente:
                    self.message.text = f"Paciente encontrado. ID: {self.id_paciente}"
                else:
                    self.message.text = "Paciente no encontrado."
            else:
                self.message.text = f"Error al buscar paciente: {response.status_code}"
        except Exception as e:
            self.message.text = f"Error de conexión: {str(e)}"

    def eliminar_paciente(self, instance):
        if not self.id_paciente:
            self.message.text = "Debe buscar el ID del paciente antes de eliminarlo."
            return

        headers = {"X-CSRFToken": self.csrf_token}

        try:
            response = requests.delete(
                f"http://127.0.0.1:8000/api/paciente/delete/{self.id_paciente}/",
                headers=headers,
                cookies={"csrftoken": self.csrf_token}
            )
            if response.status_code == 204:
                self.message.text = "Paciente eliminado exitosamente."
                self.rut.text = ""
                self.id_paciente = None
            else:
                self.message.text = f"Error al eliminar paciente: {response.status_code}"
        except Exception as e:
            self.message.text = f"Error de conexión: {str(e)}"

    def cancelar(self, instance):
        self.rut.text = ""
        self.id_paciente = None
        self.manager.current = "paciente"


# Pantalla para Gestionar Doctores
class DoctorScreen(CSRFScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")

        # Botón para Volver
        btn_back = Button(
            text="Volver", 
            size_hint_y=None, 
            height=50, 
            on_press=self.goto_menu
        )

        # Botón para Crear
        btn_create = Button(text="Crear Doctor", on_press=self.goto_create)
        # Botón para Leer
        btn_read = Button(text="Leer Doctores", on_press=self.goto_read)
        # Botón para Actualizar
        btn_update = Button(text="Actualizar Doctor", on_press=self.goto_update)
        # Botón para Eliminar
        btn_delete = Button(text="Eliminar Doctor", on_press=self.goto_delete)

        # Agregar botones al layout
        layout.add_widget(btn_back)  # Botón Volver agregado al inicio
        layout.add_widget(btn_create)
        layout.add_widget(btn_read)
        layout.add_widget(btn_update)
        layout.add_widget(btn_delete)

        self.add_widget(layout)

    def goto_menu(self, instance):
        """Cambia a la pantalla principal o menú"""
        self.manager.current = "menu"  # Cambia al nombre de tu pantalla principal

    def goto_create(self, instance):
        self.manager.current = "create_doctor"

    def goto_read(self, instance):
        self.manager.current = "read_doctor"

    def goto_update(self, instance):
        # Aquí deberías seleccionar un RUT previamente
        update_screen = self.manager.get_screen("update_doctor")
        update_screen.buscar_doctor(rut_seleccionado)
        self.manager.current = "update_doctor"

    def goto_delete(self, instance):
        self.manager.current = "delete_doctor"

# Pantalla para Crear Doctor
class CreateDoctorScreen(CSRFScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")
        
        self.input_nombre = TextInput(hint_text="Nombre del Doctor")
        self.input_rut = TextInput(hint_text="RUT del Doctor")
        self.input_correo = TextInput(hint_text="Correo Electrónico")
        self.input_telefono = TextInput(hint_text="Teléfono")
        
        btn_guardar = Button(text="Guardar", on_press=self.guardar_doctor)
        btn_cancelar = Button(text="Cancelar", on_press=self.cancelar)

        layout.add_widget(self.input_nombre)
        layout.add_widget(self.input_rut)
        layout.add_widget(self.input_correo)
        layout.add_widget(self.input_telefono)
        layout.add_widget(btn_guardar)
        layout.add_widget(btn_cancelar)

        self.add_widget(layout)

    def guardar_doctor(self, instance):
        if not self.csrf_token:
            self.message.text = "Error: no se ha obtenido el token CSRF"
            return
        # Aquí llamas a tu API para crear un doctor
        data = {
            "nombre_doctor": self.input_name.text,
            "rut_doctor": self.input_rut.text,
            "correo_doctor": self.input_email.text,
            "telefono_doctor": self.input_phone.text,
        }
        headers = {
            "X-CSRFToken": self.csrf_token
        }
        try:
            response = requests.post("http://127.0.0.1:8000/api/doctor/create/",
            data = data,
            headers = headers,
            cookies={"csrftoken": self.csrf_token},
            json=data)
            if response.status_code == 201:
                self.message.text = "Doctor creado exitosamente."
                self.lista.limpiar_formulario()
                self.manager.current = "doctor"
            else:
                self.message.text = f"Error al crear doctor: {response.status_code}"
        except Exception as e:
            self.message.text = f"Error de conexión: {str(e)}"

    def limpiar_formulario(self):
        self.input_name.text = ""
        self.input_rut.text = ""
        self.input_email.text = ""
        self.input_phone.text = ""

    def cancelar(self, instance):
        self.limpiar_formulario()
        self.manager.current = "doctor"

class ReadDoctorScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")
        self.label = Label(text="Cargando lista de doctores...")
        btn_back = Button(text="Volver", on_press=self.goto_doctor_screen)

        layout.add_widget(self.label)
        layout.add_widget(btn_back)
        self.add_widget(layout)
        self.load_doctors()

    def load_doctors(self):
        # Aquí consumes el API para obtener la lista de doctores
        response = requests.get("http://127.0.0.1:8000/api/doctor/")
        if response.status_code == 200:
            doctors = response.json()
            self.label.text = "\n".join([f"{doc['nombre_doctor']} ({doc['rut_doctor']})" for doc in doctors])
        else:
            self.label.text = "Error al cargar doctores."

    def goto_doctor_screen(self, instance):
        self.manager.current = "doctor"

class UpdateDoctorScreen(CSRFScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")

        self.rut = TextInput(hint_text="RUT del Doctor", multiline=False)
        self.message = Label(text="Ingrese el RUT del doctor para buscar y actualizar.")

        btn_search = Button(text="Buscar Doctor", on_press=self.buscar_doctor)

        self.rut = TextInput(hint_text="RUT (No editable)", readonly=True)
        self.nombre = TextInput(hint_text="Nuevo Nombre")
        self.correo = TextInput(hint_text="Nuevo Correo")
        self.telefono = TextInput(hint_text="Nuevo Teléfono")
        self.sexo = TextInput(hint_text="Nuevo Sexo")
        self.message = Label(text="")

        btn_actualizar = Button(text="Actualizar Doctor", on_press=self.actualizar_doctor)
        btn_cancelar = Button(text="Cancelar", on_press=self.cancelar)

        layout.add_widget(self.rut)
        layout.add_widget(self.nombre)
        layout.add_widget(self.correo)
        layout.add_widget(self.telefono)
        layout.add_widget(self.sexo)
        layout.add_widget(btn_search)
        layout.add_widget(btn_actualizar)
        layout.add_widget(btn_cancelar)

        self.add_widget(layout)

        error = self.obtener_csrf_token()
        if error:
            self.message.text = error

    def buscar_doctor(self, instance):
        rut = self.input_rut.text
        response = requests.get(f"http://127.0.0.1:8000/api/doctor/{rut}/")
        if response.status_code == 200:
            doctor = response.json()
            self.input_name.text = doctor["nombre_doctor"]
        else:
            print("Doctor no encontrado.")

    def actualizar_doctor(self, instance):
        rut = self.input_rut.text
        data = {"nombre_doctor": self.input_name.text}
        response = requests.put(f"http://127.0.0.1:8000/api/doctor/update/{rut}/", json=data)
        if response.status_code == 200:
            print("Doctor actualizado exitosamente.")
        else:
            print("Error al actualizar doctor.")

    def goto_doctor_screen(self, instance):
        self.manager.current = "doctor"

    def cancelar(self, instance):
        self.rut.text = ""
        self.nombre.text = ""
        self.correo.text = ""
        self.telefono.text = ""
        self.sexo.text = ""
        self.id_doctor = None
        self.message.text = ""
        self.manager.current = "doctor"

class DeleteDoctorScreen(CSRFScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")

        self.input_rut = TextInput(hint_text="RUT del Doctor")
        btn_delete = Button(text="Eliminar", on_press=self.eliminar_doctor)
        btn_back = Button(text="Volver", on_press=self.goto_doctor_screen)

        layout.add_widget(self.input_rut)
        layout.add_widget(btn_delete)
        layout.add_widget(btn_back)

        self.add_widget(layout)

    def eliminar_doctor(self, instance):
        rut = self.input_rut.text
        response = requests.delete(f"http://127.0.0.1:8000/api/doctor/delete/{rut}/")
        if response.status_code == 204:
            print("Doctor eliminado exitosamente.")
        else:
            print("Error al eliminar doctor:", response.json())

    def goto_doctor_screen(self, instance):
        self.manager.current = "doctor"

# Pantalla para Agendar Cita

class CitasScreen(CSRFScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        btn_back = Button(
            text="Volver",
            size_hint_y=None,
            height=50,
            on_press=self.goto_menu
        )

        btn_create = Button(text="Agendar Cita", on_press=self.goto_create)
        btn_read = Button(text="Ver Citas", on_press=self.goto_read)
        btn_update = Button(text="Actualizar Cita", on_press=self.goto_update)
        btn_delete = Button(text="Eliminar Cita", on_press=self.goto_delete)

        layout.add_widget(btn_back)
        layout.add_widget(btn_create)
        layout.add_widget(btn_read)
        layout.add_widget(btn_update)
        layout.add_widget(btn_delete)

        self.add_widget(layout)

    def goto_menu(self, instance):
        self.manager.current = "menu"

    def goto_create(self, instance):
        self.manager.current = "create_cita"

    def goto_read(self, instance):
        self.manager.current = "read_cita"

    def goto_update(self, instance):
        self.manager.current = "update_cita"

    def goto_delete(self, instance):
        self.manager.current = "delete_cita"

class CrearCitaScreen(CSRFScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.spinner_paciente = Spinner(text='Seleccionar Paciente')
        self.spinner_doctor = Spinner(text='Seleccionar Doctor', on_text=self.actualizar_horarios)
        self.spinner_disponibilidad = Spinner(text='Seleccionar Disponibilidad')
        self.descripcion = TextInput(hint_text='Descripción de la Cita')
        self.message = Label(text="Complete los datos para agendar la cita")

        btn_guardar = Button(text="Agendar Cita", on_press=self.agendar_cita)
        btn_cancelar = Button(text="Cancelar", on_press=self.cancelar)
        

        layout.add_widget(Label(text="Registrar Cita"))
        layout.add_widget(Label(text="Paciente"))
        layout.add_widget(self.spinner_paciente)
        layout.add_widget(Label(text="Doctor"))
        layout.add_widget(self.spinner_doctor)
        layout.add_widget(Label(text="Horario Disponible"))
        layout.add_widget(self.spinner_disponibilidad)
        layout.add_widget(Label(text="Descripción"))
        layout.add_widget(self.descripcion)
        layout.add_widget(btn_guardar)
        layout.add_widget(btn_cancelar)

        self.add_widget(layout)

        error = self.obtener_csrf_token()
        if error:
            self.message.text = error
            
        self.cargar_datos()

    def cargar_datos(self):
        try:
            # Cargar pacientes
            response_pacientes = requests.get("http://127.0.0.1:8000/api/paciente/")
            if response_pacientes.status_code == 200:
                pacientes = response_pacientes.json()
                self.spinner_paciente.values = [f"{p['id_paciente']} - {p['nombre_paciente']}" for p in pacientes]

            # Cargar doctores
            response_doctores = requests.get("http://127.0.0.1:8000/api/doctor/")
            if response_doctores.status_code == 200:
                doctores = response_doctores.json()
                self.spinner_doctor.values = [f"{d['id_doctor']} - {d['nombre_doctor']}" for d in doctores]
        except Exception as e:
            print(f"Error al cargar datos: {e}")

    def actualizar_horarios(self, instancia):
        try:
            doctor_id = self.spinner_doctor.text.split(" - ")[0]
            response_horarios = requests.get(f"http://127.0.0.1:8000/api/horario/?doctor_id={doctor_id}")
            if response_horarios.status_code == 200:
                horarios = response_horarios.json()
                self.spinner_disponibilidad.values = [f"{h['id_disponibilidad']} - {h['fecha_disponible']} {h['hora_inicio_dispo']}-{h['hora_termino_dispo']}" for h in horarios]
        except Exception as e:
            print(f"Error al cargar datos: {e}")


    def agendar_cita(self, instancia):
        """Registra la cita en la base de datos"""
        try:
            paciente_id = self.spinner_paciente.text.split(" - ")[0]
            doctor_id = self.spinner_doctor.text.split(" - ")[0]
            disponibilidad_id = self.spinner_disponibilidad.text.split(" - ")[0]
            descripcion = self.descripcion.text

            data = {
                "paciente": paciente_id,
                "doctor": doctor_id,
                "disponibilidad_cita": disponibilidad_id,
                "estado_cita": "P",  # Por defecto, 'Pendiente'
                "descripcion_cita": descripcion
            }
            headers = {
                "X-CSRFToken": self.csrf_token
            }

            response = requests.post("http://127.0.0.1:8000/api/cita/create/", 
            data=data,
            headers=headers,
            cookies={"csrftoken": self.csrf_token},
            json=data)
            if response.status_code == 201:
                print("Cita registrada exitosamente.")
            else:
                print(f"Error al registrar la cita: {response.json()}")
        except Exception as e:
            print(f"Error: {e}")

    def cancelar(self, instancia):
        self.manager.current = "menu" 

# Pantalla para Crear Ficha Médica
class CrearFichaMedicaScreen(CSRFScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.paciente_rut = TextInput(hint_text='RUT del Paciente')
        self.tipo_sangre = TextInput(hint_text='Tipo de Sangre')
        self.alergias = TextInput(hint_text='Alergias')
        self.estatura = TextInput(hint_text='Estatura')
        self.peso = TextInput(hint_text='Peso')
        self.message = Label(text="Complete los datos para crear la ficha médica")
        submit_btn = Button(text="Crear Ficha Médica", on_press=self.crear_ficha)
        
        layout.add_widget(self.paciente_rut)
        layout.add_widget(self.tipo_sangre)
        layout.add_widget(self.alergias)
        layout.add_widget(self.estatura)
        layout.add_widget(self.peso)
        layout.add_widget(self.message)
        layout.add_widget(submit_btn)
        self.add_widget(layout)

        error = self.obtener_csrf_token()
        if error:
            self.message.text = error

    def crear_ficha(self, instance):
        if not self.csrf_token:
            self.message.text = "Error al obtener el token CSRF"
            return

        data = {
            "paciente_rut": self.paciente_rut.text,
            "tipo_sangre": self.tipo_sangre.text,
            "alergias": self.alergias.text,
            "estatura": self.estatura.text,
            "peso": self.peso.text
        }
        headers = {
            "X-CSRFToken": self.csrf_token
        }

        try:
            response = requests.post(
                "http://127.0.0.1:8000/api/fichamedica/create/",
                data=data,
                headers=headers,
                cookies={"csrftoken": self.csrf_token}
            )
            if response.status_code == 201:
                self.message.text = "Ficha médica creada exitosamente"
            else:
                self.message.text = "Error al crear la ficha médica"
        except Exception as e:
            self.message.text = f"Error de conexión: {str(e)}"


# Pantalla para Crear Receta Médica
class CrearRecetaScreen(CSRFScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.paciente_rut = TextInput(hint_text='RUT del Paciente')
        self.medicamento = TextInput(hint_text='Nombre del Medicamento')
        self.frecuencia = TextInput(hint_text='Frecuencia del Medicamento')
        self.dosis = TextInput(hint_text='Dosis')
        self.duracion = TextInput(hint_text='Duración en Días')
        self.message = Label(text="Complete los datos para crear la receta médica")
        submit_btn = Button(text="Crear Receta", on_press=self.crear_receta)
        
        layout.add_widget(self.paciente_rut)
        layout.add_widget(self.medicamento)
        layout.add_widget(self.frecuencia)
        layout.add_widget(self.dosis)
        layout.add_widget(self.duracion)
        layout.add_widget(self.message)
        layout.add_widget(submit_btn)
        self.add_widget(layout)

        error = self.obtener_csrf_token()
        if error:
            self.message.text = error

    def crear_receta(self, instance):
        if not self.csrf_token:
            self.message.text = "Error al obtener el token CSRF"
            return

        data = {
            "paciente_rut": self.paciente_rut.text,
            "nombre_medicamento": self.medicamento.text,
            "frecuencia_medicamento": self.frecuencia.text,
            "dosis": self.dosis.text,
            "duracion": self.duracion.text
        }
        headers = {
            "X-CSRFToken": self.csrf_token
        }

        try:
            response = requests.post(
                "http://127.0.0.1:8000/api/receta/create/",
                data=data,
                headers=headers,
                cookies={"csrftoken": self.csrf_token}
            )
            if response.status_code == 201:
                self.message.text = "Receta médica creada exitosamente"
            else:
                self.message.text = "Error al crear la receta médica"
        except Exception as e:
            self.message.text = f"Error de conexión: {str(e)}"


# Clase principal de la aplicación
class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(PacienteScreen(name="paciente"))
        sm.add_widget(CreatePacienteScreen(name="create_paciente"))
        sm.add_widget(ReadPacienteScreen(name="read_paciente"))
        sm.add_widget(UpdatePacienteScreen(name="update_paciente"))
        sm.add_widget(DeletePacienteScreen(name="delete_paciente"))

        sm.add_widget(DoctorScreen(name="doctor"))
        sm.add_widget(CreateDoctorScreen(name="create_doctor"))
        sm.add_widget(ReadDoctorScreen(name="read_doctor"))
        sm.add_widget(UpdateDoctorScreen(name="update_doctor"))
        sm.add_widget(DeleteDoctorScreen(name="delete_doctor"))

        sm.add_widget(CitasScreen(name="cita"))
        sm.add_widget(CrearCitaScreen(name="create_cita"))
        
        
      
        return sm


if __name__ == "__main__":
    MyApp().run()






