from django.shortcuts import render ,redirect ,get_object_or_404
from django.contrib import auth
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView ,ListView ,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from requets.models import Requet
from django.contrib.auth.models import User
from users.models import Profile
from .forms import AddAdminForm ,UserChangeInfoForm ,ProfileAdminForm
from .forms import EditRequetForm
from django.db.models import Q
from django.utils import timezone



# Create your views here.
def home(request):
    return render(request , "manager/list_requets.html")


def login_manager(request):

    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(request ,username = username , password = password)
        if user and user.profile.group == "admin":
            auth.login(request,user)
            messages.success(request,f"welcome {username}")
            return redirect("manager_home")
        elif user == None :
            error = " nom d'utilisateur ou mot de passe n'est pas correcte"
            return render(request,"manager/login_manager.html",{"error":error})
        else :
            error = f"{username} n'est pas un administrateur, seul l'administrateur peut accéder à cette page"
            return render(request,"manager/login_manager.html",{"error":error})


    return render(request,"manager/login_manager.html")


# <------------------------- nouveax reclamation ----------------------------------------->

class RequetsListView( LoginRequiredMixin , UserPassesTestMixin ,ListView):
    model = Requet
    template_name = "manager/requet_list.html"
    ordering = ["-pub_date"]
    context_object_name = "requets"

    def get_queryset(self):
        return Requet.objects.filter(state = "ont étape de traitement").order_by("client__profile__type","-pub_date")

    def test_func(self):
        return self.request.user.profile.group == "admin"

# <------------------------------- reclamation approvée   ----------------------------------------->

class RequetsApprovedListView( LoginRequiredMixin , UserPassesTestMixin ,ListView):
    model = Requet
    template_name = "manager/reclamation_approveé.html"
    ordering = ["-pub_date"]
    context_object_name = "requets"
    paginate_by = 4

    def get_queryset(self):
        return Requet.objects.filter(state = "apprové par l'administrateur").order_by("-pub_date")

    def test_func(self):
        return self.request.user.profile.group == "admin"

# <--------------------------------------- reclamation des probleme fixeé ---------------------------------->


class RequetsFixedListView( LoginRequiredMixin , UserPassesTestMixin ,ListView):
    model = Requet
    template_name = "manager/reclamation_fixée.html"
    ordering = ["-fix_date"]
    context_object_name = "requets"
    paginate_by = 2

    def get_queryset(self):
        return Requet.objects.filter(state = "Problème Résolu").order_by("-fix_date")

    def test_func(self):
        return self.request.user.profile.group == "admin"




class RequetDeleteView(LoginRequiredMixin , UserPassesTestMixin ,DeleteView ):
    model = Requet
    template_name = "manager/requet_confirm_delete.html"

    def get_success_url(self):
        return reverse("manager_requets")

    def test_func(self):
        return self.request.user.profile.group == "admin"

    def get_context_data(self ,**kwargs):
        data = super().get_context_data(**kwargs)
        requet = self.get_object()
        data['c_requet'] = requet
        return data

# <----------------------------------- edit and approve requet   -------------------------------------------------->

@login_required
def edit_requet(request ,id ):
    requet = get_object_or_404(Requet , pk=id)
    client = requet.client.username

    if request.user.profile.group == "admin" :
        form = EditRequetForm(instance = requet)

        if request.method == "POST":
            form =  EditRequetForm(request.POST ,instance = requet)
            if form.is_valid():
                form.save()
                if requet.state == "ont étape de traitement" :
                    requet.state = "apprové par l'administrateur"
                    requet.aprove_date = timezone.now()
                    requet.save()
                messages.success(request,f"{client} Reclamation est modifie avec success")
                return redirect("manager_requets")

        return render(request,"manager/edit_requet.html",{"form":form ,"requet":requet,"requet":requet})
    else :
        return HttpResponse("<h1>403 Forbidden </h1>")


@login_required
def aprove(request ,id):
    requet = get_object_or_404(Requet , pk = id)
    client = requet.client.username

    if request.method == 'POST' and request.user.profile.group == "admin" :
        requet.aprove()
        messages.success(request,f"{client} Reclamation est approvée avec success")
        return redirect("manager_requets")

    else :
        return HttpResponse("<h1>403 Forbidden </h1>")

#requet fixed informations
@login_required
def requet_info(request ,id):
    requet = get_object_or_404(Requet , pk = id)

    if  request.user.profile.group == "admin" :
        return render(request,"manager/requet_information.html",{"requet":requet})

    else :
        return HttpResponse("<h1>403 Forbidden </h1>")

# <--------------------------- tech part ----------------------------------------------->
# register tech
@login_required
def register_employee(request):
    if request.user.profile.group == "admin" :
        if request.method == 'POST':
            u_form = AddAdminForm(request.POST)
            p_form = ProfileAdminForm(request.POST)

            if u_form.is_valid() and p_form.is_valid() :
                user = u_form.save()
                user.set_password(user.password)
                username = user.username
                u_profile = p_form.save(commit = False)
                u_profile.owner = user
                u_profile.group = "tech"
                u_profile.save()
                messages.success(request,f"le technicien {username} est creé avec success")
                return redirect("list_tech")

        else :
            u_form = AddAdminForm()
            p_form = ProfileAdminForm()

        return render(request,"manager/register_employee.html" ,{"u_form":u_form ,"p_form":p_form})
    else :
        return HttpResponse("<h1>403 Forbidden</h1>")

@login_required
def register_admin(request):
    if request.user.profile.group == "admin" :
        if request.method == 'POST':
            u_form = AddAdminForm(request.POST)

            if u_form.is_valid() :
                user = u_form.save()
                user.set_password(user.password)
                username = user.username
                u_profile = Profile.objects.create(owner = user ,group = "admin")
                u_profile.save()
                messages.success(request,f"un compte de {username} admin est creé avec success")
                return redirect("manager_requets")

        else :
            u_form = AddAdminForm()

        return render(request,"manager/register_admin.html" ,{"u_form":u_form})
    else :
        return HttpResponse("<h1>403 Forbidden</h1>")

# list des technicien
class TechListView( LoginRequiredMixin , UserPassesTestMixin ,ListView):
    model = Requet
    template_name = "manager/list_tech.html"
    context_object_name = "techs"

    def get_queryset(self):
        return User.objects.filter(profile__group = "tech")

    def test_func(self):
        return self.request.user.profile.group == "admin"

# delete techs
class TechDeleteView(LoginRequiredMixin , UserPassesTestMixin ,DeleteView ):
    model = User
    template_name = "manager/tech_confirm_delete.html"

    def get_success_url(self):
        return reverse("list_tech")

    def test_func(self):
        user = self.get_object()
        return self.request.user.profile.group == "admin" and user.profile.group == "tech"

    def get_context_data(self ,**kwargs):
        data = super().get_context_data(**kwargs)
        tech = self.get_object()
        data['tech'] = tech
        return data


#edit tech
@login_required
def tech_info(request ,id):
    tech = get_object_or_404(User , pk = id)
    if tech.profile.group == "tech" :

        u_form = UserChangeInfoForm(instance = tech)
        p_form = ProfileAdminForm(instance = tech.profile)

        if request.method == 'POST'  :
            u_form = UserChangeInfoForm( request.POST ,instance = tech )
            p_form = ProfileAdminForm(request.POST ,instance = tech.profile)

            if u_form.is_valid() and p_form.is_valid() :
                email1 = u_form.cleaned_data["email"]
                if User.objects.filter(email = email1).exclude(username = tech.username).exists():
                    error1 = "l'adresse e-mail que vous avez entrée est déjà enregistrée,"
                    return render(request,"manager/tech_info.html",{"u_form":u_form,"p_form":p_form,"error1":error1,"tech":tech})
                else :
                    u_form.save()
                    p_form.save()
                    username = tech.username
                    messages.success(request,f"Les informations de {username} ont été modifiées avec succès")
                    return redirect("tech_info" ,id = tech.id)

        return render(request,"manager/tech_info.html",{"u_form":u_form ,"p_form":p_form,"tech":tech})

    else :
        return HttpResponse("<h1> 403 Forbidden </h1>")


# <-------------------------------------- client part --------------------------------------->
def client_info(request , id):
    if request.user.profile.group == "admin":
        client = get_object_or_404(User , pk = id)
        return render(request,"manager/client_info.html",{"client" : client})
    else :
        return HttpResponse("<h1> 403 Forbidden </h1>")

class PersonneListView(LoginRequiredMixin , UserPassesTestMixin ,ListView):
    model = User
    template_name = "manager/personne_list.html"
    context_object_name = "clients"

    def get_queryset(self):
        return User.objects.filter(profile__type = "personne")

    def test_func(self):
        return self.request.user.profile.group == "admin"

#list des entreprises
def enterprise_list(request):
    if request.user.profile.group == "admin":
        clients = User.objects.filter(profile__type = "entreprise")
        return render(request,"manager/enterprise_list.html",{"clients":clients})
    else :
        return HttpResponse("<h1>403 Forbidden</h1>")



#delete client
class PersonneDeleteView(LoginRequiredMixin , UserPassesTestMixin ,DeleteView):
    model = User
    template_name = "manager/delete_personne.html"

    def get_context_data(self,**kwargs):
        data = super().get_context_data(**kwargs)
        client = self.get_object()
        data['client'] = client
        return data

    def test_func(self):
        return self.request.user.profile.group == "admin"

    def get_success_url(self):
        return reverse("list_personne")
