import random
import string
from django import forms
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
            'matricule': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #Generate matricule if it doesn't exist yet
        # if not self.instance.matricule:
        #     self.instance.matricule = self.generate_random_matricule()
        #     self.instance.save()

        # Set matricule field as readonly
        #self.fields['matricule'].widget.attrs['readonly'] = True
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['company'].initial = 'Ventalis'
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








