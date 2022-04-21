from django.core.exceptions import ValidationError
import os

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extention = ['.jpg' , '.png' , '.jpeg']

    if ext.lower() not in valid_extention :
        raise ValidationError('Unsupported file extension')