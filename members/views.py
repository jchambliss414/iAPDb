from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from members.forms import RegisterUserForm


def members_list(request):
    return render(request, 'members_list.html')


def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=[password])
            messages.success(request, "Registration Successful. Welcome!")
            return redirect('login')
    else:
        form = RegisterUserForm()
    return render(request, 'members/authenticate/register.html', {'form': form})


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.success(request, "Login Error")
            return redirect('login')
            pass

    else:
        return render(request, 'members/authenticate/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, "Successfully Logout Out")
    return redirect('/')
