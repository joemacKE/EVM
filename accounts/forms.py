from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'salutation', 'is_active', 'phone_number', 'profile_pic', 'password1', 'password2']







