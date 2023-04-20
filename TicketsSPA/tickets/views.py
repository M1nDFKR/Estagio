from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home') # replace "home" with the name of your homepage URL
        else:
            error_message = "Invalid login credentials."
    else:
        error_message = ""
    return render(request, 'login.html', {'error_message': error_message})

def logout_view(request):
    logout(request)
    return redirect('home') # replace "home" with the name of your homepage URL

