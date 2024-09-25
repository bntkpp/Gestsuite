import re
from django.core.exceptions import ValidationError

def validate_rut(value):
    # Quitar puntos y guiones
    rut = value.upper().replace(".", "").replace("-", "")
    
    # Validar formato de longitud
    if len(rut) < 9:
        raise ValidationError('El RUT debe tener al menos 9 caracteres incluyendo el dígito verificador.')

    # Separar el cuerpo del RUT y el dígito verificador
    cuerpo, dv = rut[:-1], rut[-1]

    # Asegurarse de que el cuerpo solo contenga números
    if not cuerpo.isdigit():
        raise ValidationError('El RUT debe contener solo números en la parte del cuerpo.')

    # Calcular dígito verificador
    reversed_cuerpo = map(int, reversed(cuerpo))
    factors = [2, 3, 4, 5, 6, 7]
    s = sum(d * f for d, f in zip(reversed_cuerpo, factors * 100))
    mod = (-s) % 11

    # Convertir el dígito verificador
    if mod == 10:
        calculated_dv = 'K'
    else:
        calculated_dv = str(mod)

    # Validar dígito verificador
    if dv != calculated_dv:
        raise ValidationError(f'El RUT {value} es inválido.')

