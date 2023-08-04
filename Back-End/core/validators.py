from django.core.exceptions import ValidationError
import re


def validate_phone_number(number):

    # Remove any whitespace or special characters from the phone number
    phone_number = re.sub(r'\s+|-', '', number)
    length = 11

    if len(phone_number) != length or not re.match(r'^09\d{9}$', phone_number):
        raise ValidationError(
            f'{number} is Not valid!!, hint: it must be 11 digits and start with 09. e,g: 09171234567'
        )
    return number

