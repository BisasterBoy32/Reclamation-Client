from django.shortcuts import render ,redirect , get_object_or_404
from django.contrib.auth.models import User
from .models import Profile ,Personne ,Company , Address
from requets.models import Requet
from .forms import( AddressPersonneChangeForm ,UserForm ,
                    ProfileForm , UserChangeInfoForm ,
                    ProfileChangeForm ,PersonneChangeForm ,
                    CompanyChangeForm ,AddressCompanyChangeForm
                )
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse ,JsonResponse
from django.views.generic import DetailView
from django.contrib.auth.mixins import UserPassesTestMixin , LoginRequiredMixin
from manager.forms import NotificationForm


from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.conf import settings
from .tokens import account_activation_token


# username validation
def username_validation(request ,username):
    not_valid = User.objects.filter(username = username).exists()

    return JsonResponse({"not_valid":not_valid})

# email validation
def email_validation(request ,email):
    not_valid = User.objects.filter(email = email).exists()

    return JsonResponse({"not_valid":not_valid})

# Create your views here.

def register(request):
    if request.method == 'POST':
        u_form = UserForm(request.POST)
        p_form = ProfileForm(request.POST)

        if u_form.is_valid() and p_form.is_valid():
            user = u_form.save(commit = False)
            user.is_active = False
            user.save()
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
                address = Address.objects.create(
                profile = u_profile ,region = request.POST["region"], commune = request.POST["commune"],
                rue=request.POST["rue"] ,logement = request.POST["logement"]
                )
                address.save()

            elif u_profile.type == "entreprise":
                name = request.POST["name"]
                entreprise = Company.objects.create(name = name , profile = u_profile)
                entreprise.save()
                address = Address.objects.create(
                profile = u_profile ,region = request.POST["e_region"], commune = request.POST["e_commune"], rue=request.POST["e_rue"]
                )
                address.save()

            #in case you want to get rid off the email confirmation : put this return redirect("login") and comment the rest bellow
            # get current site
            current_site = get_current_site(request)
            username = user.username
            subject = f"Activation du compte pour le client {username}"
            # create Message
            message = render_to_string("users/confirm_user.html", {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                })
            html_message = render_to_string("users/confirm_user.html", {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                })
            # send activation link to the user
            user.email_user(subject=subject, message=message, html_message=html_message)
            return redirect('success_register')


    else :
        u_form = UserForm()
        p_form = ProfileForm()

    return render(request,"users/register.html" ,{"u_form":u_form ,"p_form":p_form})


#confirm the user identity
def success_register(request):
    return render(request,"users/success_register.html")

def confirm_user(request ,uidb64 ,token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError,User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            username = user.username
            auth.login(request ,user)
            messages.success(request,f"l'utilisateur {username} a été créé avec succès")
            return redirect("home")
        else:
            return HttpResponse("Invalid Token")



# log in
def login_view(request):
    u_form = UserForm()
    p_form = ProfileForm()
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]

        user = User.objects.filter(username = username).first()
        if user and user.is_active == False :
            error = f"{username} votre compte n'est pas encore activé allez sur votre email et cliquez sur le lien que nous vous avons envoyé pour activer votre compte"
            return render(request,"users/register.html",{"error":error,"u_form":u_form,"p_form":p_form})
        else :
            user = auth.authenticate(request ,username = username , password = password)
            if user  :
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
    a_form = AddressPersonneChangeForm(instance = request.user.profile.address)

    if request.method == 'POST':
        u_form = UserChangeInfoForm( request.POST ,instance = request.user )
        p_form = ProfileChangeForm( request.POST , instance = request.user.profile )
        ps_form = PersonneChangeForm( request.POST , instance = request.user.profile.personne )
        a_form = AddressPersonneChangeForm(request.POST ,instance = request.user.profile.address)

        if u_form.is_valid() and p_form.is_valid() and ps_form.is_valid() and a_form.is_valid():
            email1 = u_form.cleaned_data["email"]
            if User.objects.filter(email = email1).exclude(username = request.user.username).exists():
                error1 = "l'adresse e-mail que vous avez entrée est déjà enregistrée,"
                return render(request,"users/client_info.html",{"u_form":u_form,"p_form":p_form,"ps_form":ps_form,"a_form":a_form ,"error1":error1})
            else :
                u_form.save()
                p_form.save()
                ps_form.save()
                a_form.save()
                username = request.user.username
                messages.success(request,f"Les informations d'utilisateur {username} ont été modifiées avec succès")
                return redirect("client_info")

    return render(request,"users/client_info.html",{"u_form":u_form,"p_form":p_form,"ps_form":ps_form,"a_form":a_form })

# <------------------------------- company client information ----------------------------------------->


@login_required
def entreprise_info(request):
    u_form = UserChangeInfoForm(instance = request.user )
    p_form = ProfileChangeForm(instance = request.user.profile )
    c_form = CompanyChangeForm(instance = request.user.profile.company )
    a_form = AddressCompanyChangeForm(instance = request.user.profile.address)

    if request.method == 'POST':
        u_form = UserChangeInfoForm( request.POST ,instance = request.user )
        p_form = ProfileChangeForm( request.POST , instance = request.user.profile )
        c_form = CompanyChangeForm( request.POST , instance = request.user.profile.company )
        a_form = AddressCompanyChangeForm(request.POST ,instance = request.user.profile.address)

        if u_form.is_valid() and p_form.is_valid() and c_form.is_valid() and a_form.is_valid():
            email1 = u_form.cleaned_data["email"]
            if User.objects.filter(email = email1).exclude(username = request.user.username).exists():
                error1 = "l'adresse e-mail que vous avez entrée est déjà enregistrée,"
                return render(request,"users/client_info.html",{"u_form":u_form,"p_form":p_form ,"c_form":c_form,"error1":error1,"a_form":a_form})
            else :
                u_form.save()
                p_form.save()
                c_form.save()
                a_form.save()
                username = request.user.username
                messages.success(request,f"Les informations d'utilisateur {username} ont été modifiées avec succès")
                return redirect("entreprise_info")

    return render(request,"users/client_info.html",{"u_form":u_form ,"p_form":p_form,"c_form":c_form,"a_form":a_form})


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

@login_required
def note_view(request , id_r , id_u):

    requet = get_object_or_404(Requet , pk = id_r)
    owner = get_object_or_404(User , pk = id_u)
    form = NotificationForm()

    if request.user == requet.client or request.user == requet.tech :

        if request.method == "POST" :
            form = NotificationForm(request.POST)

            if form.is_valid():
                requet.requet_note()
                note = form.save(commit = False)
                note.owner = owner
                note.requet = requet
                note.save()
                username = owner.username
                messages.success(request , f"{username} votre notification est crea avec success")
                if request.user == requet.tech :
                    requet.tech = None
                    requet.save()
                    return redirect("tech_requets" )
                else :
                    return redirect("siuvi_requete" )

        return render(request ,"users/note.html",{"form":form ,"client":owner ,"requet":requet})
    else :
        return HttpResponse("<h2> 403 Forbidden </h2>")
