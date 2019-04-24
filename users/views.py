from django.shortcuts import render ,redirect , get_object_or_404
from django.contrib.auth.models import User
from .models import Profile ,Personne ,Company
from requets.models import Requet
from .forms import UserForm , ProfileForm , UserChangeInfoForm ,ProfileChangeForm ,PersonneChangeForm ,CompanyChangeForm
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import DetailView
from django.contrib.auth.mixins import UserPassesTestMixin , LoginRequiredMixin


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
            u_type = request.POST["type"]
            u_profile.type = u_type
            u_profile.save()
            if u_profile.type == "personne":
                first_name = request.POST["first_name"]
                last_name = request.POST["last_name"]
                personne = Personne.objects.create(first_name = first_name , last_name = last_name , profile = u_profile)
                personne.save()

            elif u_profile.type == "entreprise":
                name = request.POST["name"]
                entreprise = Company.objects.create(name = name , profile = u_profile)
                entreprise.save()


            username = user.username
            new_user = auth.authenticate(request , username = u_form.cleaned_data["username"] , password = u_form.cleaned_data["password1"])
            auth.login(request ,new_user)
            messages.success(request,f"l'utilisateur {username} a été créé avec succès")
            return redirect("home")

    else :
        u_form = UserForm()
        p_form = ProfileForm()

    return render(request,"users/register.html" ,{"u_form":u_form ,"p_form":p_form})


# log in
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


# <----------------------------------- personne client informations ----------------------------------->

@login_required
def user_info(request):
    u_form = UserChangeInfoForm(instance = request.user )
    p_form = ProfileChangeForm(instance = request.user.profile )
    ps_form = PersonneChangeForm(instance = request.user.profile.personne )

    if request.method == 'POST':
        u_form = UserChangeInfoForm( request.POST ,instance = request.user )
        p_form = ProfileChangeForm( request.POST , instance = request.user.profile )
        ps_form = PersonneChangeForm( request.POST , instance = request.user.profile.personne )

        if u_form.is_valid() and p_form.is_valid() and ps_form.is_valid():
            email1 = u_form.cleaned_data["email"]
            if User.objects.filter(email = email1).exclude(username = request.user.username).exists():
                error1 = "l'adresse e-mail que vous avez entrée est déjà enregistrée,"
                return render(request,"users/client_info.html",{"u_form":u_form,"p_form":p_form,"ps_form":ps_form,"error1":error1})
            else :
                u_form.save()
                p_form.save()
                ps_form.save()
                username = request.user.username
                messages.success(request,f"Les informations d'utilisateur {username} ont été modifiées avec succès")
                return redirect("client_info")

    return render(request,"users/client_info.html",{"u_form":u_form,"p_form":p_form,"ps_form":ps_form})

# <------------------------------- company client information ----------------------------------------->


@login_required
def entreprise_info(request):
    u_form = UserChangeInfoForm(instance = request.user )
    p_form = ProfileChangeForm(instance = request.user.profile )
    c_form = CompanyChangeForm(instance = request.user.profile.company )

    if request.method == 'POST':
        u_form = UserChangeInfoForm( request.POST ,instance = request.user )
        p_form = ProfileChangeForm( request.POST , instance = request.user.profile )
        c_form = CompanyChangeForm( request.POST , instance = request.user.profile.company )

        if u_form.is_valid() and p_form.is_valid() and c_form.is_valid():
            email1 = u_form.cleaned_data["email"]
            if User.objects.filter(email = email1).exclude(username = request.user.username).exists():
                error1 = "l'adresse e-mail que vous avez entrée est déjà enregistrée,"
                return render(request,"users/client_info.html",{"u_form":u_form,"p_form":p_form,"c_form":c_form,"error1":error1})
            else :
                u_form.save()
                p_form.save()
                c_form.save()
                username = request.user.username
                messages.success(request,f"Les informations d'utilisateur {username} ont été modifiées avec succès")
                return redirect("entreprise_info")

    return render(request,"users/client_info.html",{"u_form":u_form,"p_form":p_form,"c_form":c_form})


# logout
@login_required
def logout_view(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect("login")

# class ClientDetailView(UserPassesTestMixin , LoginRequiredMixin ,DetailView):
#     model = User
#     template_name = "users/client_detail.html"
#     context_object_name = "client"
#
#     def test_func(self):
#         return self.request.user.profile.group == "tech"

def requet_info(request ,id_client,id_requet ):
    client = get_object_or_404(User , pk = id_client)
    requet = get_object_or_404(Requet , pk=id_requet)

    context = {"client":client,"requet" :requet}
    if request.user.profile.group == "tech":
        return render(request, "users/requet_info.html" ,context)
    else :
        return HttpResponse("<h1>403 Forbidden</h1>")



# <--------------------------------- tech part ---------------------------------------->

def login_tech(request):

    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username = username , password = password)
        if user and user.profile.group == "tech" :
            auth.login(request ,user)
            return redirect("tech_requets")

        elif user ==  None :
            error = "nom d'utilisateur ou mot de passe n'est pas correcte"
            return render(request,"users/login_tech.html",{"error":error})

        else :
            return HttpResponse("<h2> 403 Forbidden </h2>")


    return render(request ,"users/login_tech.html")

def problem_fixed(request, id):
    requet = get_object_or_404(Requet ,pk = id)
    client = requet.client.username

    if request.method == 'POST' and request.user.profile.group == "tech" :
        requet.requet_fixed()
        messages.success(request,f"Problème de client {client} est reésolu avec success")
        return redirect("tech_requets")

    else :
        return HttpResponse("<h2> 403 Forbidden </h2>")
