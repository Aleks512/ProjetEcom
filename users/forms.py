from django import forms
from django.http import request

from .models import Consultant
from django.contrib.auth.hashers import make_password
from django.contrib.auth import password_validation


class ConsultantCreationForm(forms.ModelForm):
    class Meta:
        model = Consultant
        fields = "__all__"
        exclude = ('matricule',)
        widgets = {
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['company'].initial = 'Ventalis'
        self.fields['is_active'].initial = True
        self.fields['is_staff'].initial = True
        self.fields['is_employee'].initial = True
        self.fields['password'] = forms.CharField(
            widget=forms.PasswordInput(render_value=True),
            required=False
        )


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        #to hash password in db
        if not password:
            password = make_password(None)
            cleaned_data['password'] = password
        else:
            password_validation.validate_password(password)
            cleaned_data['password'] = make_password(password)
        return cleaned_data







