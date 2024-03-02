
from django.utils.crypto import get_random_string

def get_name_from_email(email:str):
    return email.split('@')[0] + "_" + get_random_string(length=5, allowed_chars='1234567890')