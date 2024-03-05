from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from .models import Employee


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        max_length=128,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'password']


class CreateEmployeeForm(forms.ModelForm):
    login_form = LoginForm()

    class Meta:
        model = Employee
        fields = ['last_name', 'first_name', 'middle_name', 'gender', 'position']

    def __init__(self, *args, **kwargs):
        super(CreateEmployeeForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select mb-2'
            else:
                field.widget.attrs['class'] = 'form-control mb-2'
