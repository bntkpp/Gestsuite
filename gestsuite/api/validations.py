from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
UserModel = get_user_model()

def custom_validation(data):
    email = data['email'].strip()
    username = data['username'].strip()
    password = data['password'].strip()
    ##
    if not email or UserModel.objects.filter(email=email).exists():
        raise ValidationError('Elige otro email o ingresa uno válido.')
    ##
    if not password or len(password) < 8:
        raise ValidationError('EliGe otra contraseña, minimo 8 caracteres.')
    ##
    if not username:
        raise ValidationError('Elige otro nombre de usuario.')
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


