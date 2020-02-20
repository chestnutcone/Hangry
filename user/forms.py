from django import forms
from user.models import CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    email = forms.CharField(max_length=254)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=50)

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email', 'first_name', 'last_name')

    # def create_user(self):
    #     error = ''
    #     cleaned_data = self.cleaned_data
    #     try:
    #         _ = CustomUser.objects.get(username=cleaned_data['email'])
    #         error = "Username already exists"
    #     except CustomUser.DoesNotExist:
    #         if cleaned_data['password1'] == cleaned_data['password2']:
    #             print('password', cleaned_data['password1'])
    #             password_hash = make_password(cleaned_data['password1'])
    #             _ = CustomUser.objects.create_user(username=cleaned_data['email'],
    #                                                first_name=cleaned_data['first_name'],
    #                                                last_name=cleaned_data['last_name'],
    #                                                password=password_hash)
    #         else:
    #             error = "Password does not match"
    #     return error

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('email', 'first_name', 'last_name')