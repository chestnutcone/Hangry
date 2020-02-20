from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        print('posting request here')
        print(request.POST)
        if form.is_valid():
            print('login info', form.cleaned_data)
            user = form.get_user()
            login(request, user)
            return redirect('/main/')
        else:
            print('form is not valid')
            form = AuthenticationForm()
        return render(request, 'user/login.html', {'form': form})