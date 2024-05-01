from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from exhibitions.models import Company, Exhibition


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


class CompanyForm(forms.Form):
    company_name = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        required=False,
        label='Предприятие',
        widget=forms.Select(attrs={'class': 'form-select', 'onchange': 'this.form.submit()'})
    )


class ExhibitionForm(forms.Form):
    exhibition_name = forms.ModelChoiceField(
        queryset=Exhibition.objects.all(),
        required=False,
        label='Выставка',
        widget=forms.Select(attrs={'class': 'form-select', 'onchange': 'this.form.submit()'})
    )
