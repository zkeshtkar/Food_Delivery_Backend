from django.core import validators
from django.utils.deconstruct import deconstructible


@deconstructible
class PhoneValidator(validators.RegexValidator):
    regex = r'^09\d{9}$'
    message = (
        'Enter a valid mobile number. This value may contain numbers only, '
        'and must be exactly 11 digits starting with "09"'
    )
    flags = 0


phone_validator = PhoneValidator()


@deconstructible
class EmailValidator(validators.RegexValidator):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    message = (
        'Enter a valid email.'
    )
    flags = 0


email_validator = EmailValidator()
