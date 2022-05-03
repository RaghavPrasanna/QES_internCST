from telnetlib import LOGOUT
from django.shortcuts import render, redirect

# For login authentication
from django.contrib.auth.models import User, auth
# TO display messages(message passing)
from django.contrib import messages
# Create your views here.


# To Login to your account
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')
       
    else:
        return render(request, 'login.html')


# To register user account
def register(request):

    if request.method == 'POST':
        first_name =request.POST['first_name']
        last_name =request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        # To check if both the password1 and password2 are matching
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                # print("username already exists")
                messages.info(request, 'Username already exists')
                return redirect('register')
            
            else:
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.save();
                # print("User created")
                return redirect('login')

        else:
            # print('password not matching')
            messages.info(request, 'Password not matching...')
            return redirect('register')
            
 
    else:
        return render(request, 'register.html')

# To LOGOUT
def logout(request):
    auth.logout(request)
    return redirect('/')
