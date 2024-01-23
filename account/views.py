from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from .models import Profile
from django.contrib.auth.decorators import login_required
# Create your views here.
def register(request):
    if request.method == "POST":
        print(request.POST)  # Add this line to print the POST data for debugging purposes
        email = request.POST.get('email', '')
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')

        if password == password2:
            
            # Check if username same or not
            if User.objects.filter(username=username).exists():
                messages.info(request, "username already taken")
                return redirect('register')
            # Check if email is same or not
            elif User.objects.filter(email=email).exists():
                messages.info(request, "email already registered")
                return redirect('register')
            
            else:
                # create user
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save()

                # log in the user and redirect to profile
                user_login=auth.authenticate(username=username,password=password)
                auth.login(request,user_login)

                # create profilefor new user

                user_model=User.objects.get(username=username)
                new_profile=Profile.objects.create(user=user_model,email_addresss=email)
                new_profile.save()
                return redirect('profile',user_model.username) #todo

        else:
            messages.info(request, "password not match")
            return redirect('register')

    context = {}
    return render(request, "register.html", context)

@login_required(login_url='login')
def profile(request,username):
    user_object = User.objects.get(username=username)
    user_profile=Profile.objects.get(user=user_object)
    context={"user_profile":user_profile}

    return render(request,"profile.html",context)

def login(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']

        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)

            return redirect('profile',username)
        else:
            messages.info(request,"Credentials invalid!")
            return redirect('login')
    
    return render(request,"login.html")

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')