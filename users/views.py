from django.shortcuts import render ,redirect
from django.contrib.auth.models import User
from .models import Profile
from .forms import UserForm , ProfileForm
from django.contrib import messages
from django.contrib import auth


# Create your views here.

def register(request):
    if request.method == 'POST':
        u_form = UserForm(request.POST)
        p_form = ProfileForm(request.POST)

        if u_form.is_valid() and p_form.is_valid():
            user = u_form.save()
            user.set_password(user.password)
            u_profile = p_form.save(commit = False)
            u_profile.owner = user
            u_profile.save()
            messages.success(request,f"l'utilisateur {user} a été créé avec succès")
            return redirect("register")


    else :
        u_form = UserForm()
        p_form = ProfileForm()

    return render(request,"users/register.html" ,{"u_form":u_form ,"p_form":p_form})


def login_view(request):
    u_form = UserForm()
    p_form = ProfileForm()
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(request ,username = username , password = password)
        if user :
            auth.login(request,user)
            messages.success(request,f"welcome {username}")
            return redirect("home")
        else:
            error = " nom d'utilisateur ou mot de passe n'est pas correcte"

    return render(request,"users/register.html",{"error":error,"u_form":u_form,"p_form":p_form})
