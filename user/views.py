from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from user.models import CustomUser
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.
def signup_view(request):
    if request.method == 'GET':
        # render form
        return render(request, 'registration/signup.html')
    elif request.method == 'POST':
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password2']
            password = make_password(password)

            user, created = CustomUser.objects.get_or_create(username=email,
                                                             first_name=first_name,
                                                             last_name=last_name,
                                                             password=password,
                                                             email=email
                                                             )
            return redirect('/users/login')
        else:
            return render(request, 'registration/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(reverse('main'))
        return render(request, 'registration/login.html', {'form': form})
    elif request.method == 'GET':
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})


@login_required
def logout_view(request):
    if request.method == 'GET':
        logout(request)
        return render(request, 'registration/logout.html')

@login_required
def change_password_view(request):
    current_user = request.user
    if request.method == 'GET':
        return render(request, 'registration/change_password.html')
    elif request.method == 'POST':
        form = PasswordChangeForm(current_user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('main')

        return render(request, 'registration/change_password.html', {'form': form})