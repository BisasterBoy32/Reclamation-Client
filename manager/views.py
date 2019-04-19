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
from .forms import AddAdminForm
from .forms import EditRequetForm
from django.db.models import Q



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
        elif user.profile.type != "admin":
            error = f"{username} n'est pas un administrateur, seul l'administrateur peut accéder à cette page"
            return render(request,"manager/login_manager.html",{"error":error})
        else :
            error = " nom d'utilisateur ou mot de passe n'est pas correcte"
            return render(request,"manager/login_manager.html",{"error":error})

    return render(request,"manager/login_manager.html")


# <------------------------- nouveax reclamation ----------------------------------------->

class RequetsListView( LoginRequiredMixin , UserPassesTestMixin ,ListView):
    model = Requet
    template_name = "manager/requet_list.html"
    ordering = ["-pub_date"]
    context_object_name = "requets"

    def get_queryset(self):
        return Requet.objects.filter(state = "ont étape de traitement").order_by("-pub_date")

    def test_func(self):
        return self.request.user.profile.group == "admin"

# <------------------------------- reclamation approvée   ----------------------------------------->

class RequetsApprovedListView( LoginRequiredMixin , UserPassesTestMixin ,ListView):
    model = Requet
    template_name = "manager/reclamation_approveé.html"
    ordering = ["-pub_date"]
    context_object_name = "requets"

    def get_queryset(self):
        return Requet.objects.filter(state = "apprové par l'administrateur").order_by("-pub_date")

    def test_func(self):
        return self.request.user.profile.group == "admin"

# <--------------------------------------- reclamation des probleme fixeé ---------------------------------->


class RequetsFixedListView( LoginRequiredMixin , UserPassesTestMixin ,ListView):
    model = Requet
    template_name = "manager/reclamation_fixée.html"
    ordering = ["-pub_date"]
    context_object_name = "requets"

    def get_queryset(self):
        return Requet.objects.filter(state = "Problème Résolu").order_by("-pub_date")

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

# <--------------------------- tech part ----------------------------------------------->
# register
@login_required
def register_employee(request):
    if request.user.profile.group == "admin" :
        if request.method == 'POST':
            u_form = AddAdminForm(request.POST)

            if u_form.is_valid() :
                user = u_form.save()
                user.set_password(user.password)
                username = user.username
                u_profile = Profile.objects.create(owner = user ,group = "tech")
                u_profile.save()
                messages.success(request,f"le technicien {username} est creé avec success")
                return redirect("list_tech")

        else :
            u_form = AddAdminForm()

        return render(request,"manager/register_employee.html" ,{"u_form":u_form})
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
    if tech.profile.group == "tech" :

        tech = get_object_or_404(User , pk = id)
        u_form = AddAdminForm(instance = tech)

        if request.method == 'POST'  :
            u_form = AddAdminForm( request.POST ,instance = request.user )

            if u_form.is_valid() :
                email1 = u_form.cleaned_data["email"]
                if User.objects.filter(email = email1).exclude(username = request.user.username).exists():
                    error1 = "l'adresse e-mail que vous avez entrée est déjà enregistrée,"
                    return render(request,"users/tech_info.html",{"u_form":u_form,"error1":error1})
                else :
                    u_form.save()
                    username = tech.username
                    messages.success(request,f"Les informations de {username} ont été modifiées avec succès")
                    return redirect("tech_info")

        return render(request,"manage/tech_info.html",{"u_form":u_form},{"tech":tech})

    else :
        return HttpResponse("<h1> 403 Forbidden </h1>")
