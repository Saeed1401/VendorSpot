from django.core.exceptions import ValidationError


def file_size_validation(file):
    max_size = 600

    if file.size > max_size * 1024:
        raise ValidationError(f'Files cannot be larger than {max_size * 1024}MB!!')
    

def validate_phone_number(number):
    length = 11

    if len(number) != length:
        raise ValidationError(f'{number} is Not valid!!, hint: it must be 11 digits')