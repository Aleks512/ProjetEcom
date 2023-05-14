from django.core.exceptions import ValidationError
import string

from django.core.exceptions import ValidationError


class ContainsLetterValidator:
    def validate(self, password, user=None):
        if not any(char.isupper() for char in password) or not any(char.islower() for char in password):
            raise ValidationError(
                'Le mot de passe doit contenir au moins une lettre majuscule et une lettre minuscule', code='password_no_letters')

    def get_help_text(self):
        return 'Votre mot de passe doit contenir au moins une lettre majuscule et une lettre minuscule.'


class ContainsNumberValidator:
    def validate(self, password, user=None):
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                'Le mot de passe doit contenir un chiffre', code='password_no_number')

    def get_help_text(self):
        return 'Votre mot de passe doit contenir au moins un chiffre.'


class ContainsSpecialCharacterValidator:
    def validate(self, password, user=None):
        if not any(char in string.punctuation for char in password):
            raise ValidationError(
                'Le mot de passe doit contenir un caractère spécial', code='password_no_special_characters')

    def get_help_text(self):
        return 'Votre mot de passe doit contenir au moins un caractère spécial.'

class ContainsSpecialCharacterValidator:
    def validate(self, password, user=None):
        if not any(char in string.punctuation for char in password):
            raise ValidationError(
                'Le mot de passe doit contenir un caractère spécial', code='password_no_special_characters')

    def get_help_text(self):
        return 'Votre mot de passe doit contenir au moins un caractère spécial.'