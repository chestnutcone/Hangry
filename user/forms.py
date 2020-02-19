from django import forms
from user.models import CustomUser
from django.contrib.auth.hashers import make_password


class SignUpForm(forms.Form):
    email = forms.CharField(max_length=254)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=50)
    password1 = forms.CharField(max_length=50)
    password2 = forms.CharField(max_length=50)

    def create_user(self):
        error = ''
        cleaned_data = self.cleaned_data
        print('cleaned data', cleaned_data)
        try:
            _ = CustomUser.objects.get(username=cleaned_data['email'])
        except CustomUser.DoesNotExist:
            if cleaned_data['password1'] == cleaned_data['password2']:
                password_hash = make_password(cleaned_data['password1'])
                _ = CustomUser.objects.create_user(username=cleaned_data['email'],
                                                   first_name=cleaned_data['first_name'],
                                                   last_name=cleaned_data['last_name'],
                                                   password=password_hash)
            else:
                error = "Password does not match"
        else:
            error = "User already exists"
        return error
