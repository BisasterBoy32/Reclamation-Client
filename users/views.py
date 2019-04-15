from django.shortcuts import render ,redirect
from django.contrib.auth.models import User
from .models import Profile
from .forms import UserForm , ProfileForm , UserChangeInfoForm ,ProfileChangeForm
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required


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

    return render(request,"users/register.html",{"u_form":u_form,"p_form":p_form})


# <----------------------------------- client informations ----------------------------------->

@login_required
def user_info(request):
    u_form = UserChangeInfoForm(instance = request.user )
    p_form = ProfileChangeForm(instance = request.user.profile )

    if request.method == 'POST':
        u_form = UserChangeInfoForm( request.POST ,instance = request.user )
        p_form = ProfileChangeForm( request.POST , instance = request.user.profile )

        if u_form.is_valid() and p_form.is_valid():
            email1 = u_form.cleaned_data["email"]
            if User.objects.filter(email = email1).exclude(username = request.user.username).exists():
                error1 = "l'adresse e-mail que vous avez entrée est déjà enregistrée,"
                return render(request,"users/client_info.html",{"u_form":u_form,"p_form":p_form,"error1":error1})
            else :
                u_form.save()
                p_form.save()
                username = request.user.username
                messages.success(request,f"Les informations d'utilisateur {username} ont été modifiées avec succès")
                return redirect("client_info")

    return render(request,"users/client_info.html",{"u_form":u_form,"p_form":p_form})

@login_required
def logout_view(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect("login")
