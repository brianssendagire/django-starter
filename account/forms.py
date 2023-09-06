from django import forms
from django.contrib.auth import authenticate
from material import Layout

from .models import Account
from logic.utils import extract_name


class AccountAuthenticationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'e.g. samuel.jackson', 'id': 'username'}))
    password = forms.CharField(max_length=254, label='Password',
                               widget=forms.PasswordInput(
                                   attrs={'placeholder': 'Enter your password', 'id': 'password'}))

    class Meta:
        model = Account
        fields = ('username', 'password')

    def clean(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            if not authenticate(username=extract_name(username), password=password):
                raise forms.ValidationError("Username or password are incorrect.")

    layout = Layout('username', 'password')

