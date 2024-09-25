from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
UserModel = get_user_model()

def custom_validation(data):
    email = data['email'].strip()
    username = data['username'].strip()
    password = data['password'].strip()
    ##
    if not email or UserModel.objects.filter(email=email).exists():
        raise ValidationError('elije otro email')
    ##
    if not password or len(password) < 8:
        raise ValidationError('elije otra contraseña, minimo 8 caracteres')
    ##
    if not username:
        raise ValidationError('elije otro nombre de usuario')
    return data


def validate_email(data):
    email = data['email'].strip()
    if not email:
        raise ValidationError('un email es necesario')
    return True

def validate_username(data):
    username = data['username'].strip()
    if not username:
        raise ValidationError('elije otro nombre de usuario')
    return True

def validate_password(data):
    password = data['password'].strip()
    if not password:
        raise ValidationError('una contraseña es necesaria')
    return True

def validate_rut(value):
    rut = value.upper().replace(".", "").replace("-", "")

    if len(rut) < 9:
        raise ValidationError('El RUT debe tener al menos 9 caracteres incluyendo el dígito verificador.')

    cuerpo, dv = rut[:-1], rut[-1]

    if not cuerpo.isdigit():
        raise ValidationError('El RUT debe contener solo números en la parte del cuerpo.')

    reversed_cuerpo = map(int, reversed(cuerpo))
    factors = [2, 3, 4, 5, 6, 7]
    s = sum(d * f for d, f in zip(reversed_cuerpo, factors * 100))
    mod = (-s) % 11

    if mod == 10:
        calculated_dv = 'K'
    else:
        calculated_dv = str(mod)

    if dv != calculated_dv:
        raise ValidationError(f'El RUT {value} es inválido.')
