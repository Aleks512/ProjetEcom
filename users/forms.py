from django import forms
from .models import Consultant

class ConsultantCreationForm(forms.ModelForm):
    class Meta:
        model = Consultant
        fields = ['user_name', 'email','first_name', 'last_name', 'password', 'company', 'is_staff']
        widgets = {
            'password': forms.PasswordInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].initial = "Ventalis"
        self.fields['matricule'].disabled = True
        self.fields['is_staff'].initial = True

