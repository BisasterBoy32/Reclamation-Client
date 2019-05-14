from datetime import datetime

from django.shortcuts import render ,redirect ,get_object_or_404
from django.contrib import auth
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView ,ListView ,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone

# rest rest_framework imports
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .permissions import IsManager

#my filles
from .forms import AddAdminForm ,UserChangeInfoForm ,ProfileAdminForm ,AddressTechForm
from .forms import EditRequetForm
from requets.models import Requet
from users.models import Profile
from .serializers import ReclamationSerializer


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
    ordering = ["pub_date"]
    context_object_name = "requets"

    def get_queryset(self):
        return Requet.objects.filter(state = "ont étape de traitement").order_by("client__profile__type","pub_date")

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
        return Requet.objects.filter(state = "apprové par l'administrateur").order_by("client__profile__type","-pub_date")

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

# reclamation after the failre of the technicien to fix it
class RequetsNoteeListView( LoginRequiredMixin , UserPassesTestMixin ,ListView):
    model = Requet
    template_name = "manager/reclamation_notifée.html"
    ordering = ["-fix_date"]
    context_object_name = "requets"

    def get_queryset(self):
        return Requet.objects.filter(state = "notée").order_by("-fix_date")

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
                if requet.state == "ont étape de traitement" or "notée" :
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

# Recherer un requet
@login_required
def search_requet(request):
    if request.user.profile.group == "admin" :
        search_element = request.POST["search"]
        requets = Requet.objects.filter(problem__icontains = search_element)
        return render(request,"manager/search_requet.html",{"requets" : requets})

# <--------------------------- tech part ----------------------------------------------->
# register tech
@login_required
def register_employee(request):
    if request.user.profile.group == "admin" :
        if request.method == 'POST':
            u_form = AddAdminForm(request.POST)
            p_form = ProfileAdminForm(request.POST)
            a_form = AddressTechForm(request.POST)

            if u_form.is_valid() and p_form.is_valid() and a_form.is_valid():
                user = u_form.save()
                user.set_password(user.password)
                username = user.username
                u_profile = p_form.save(commit = False)
                u_profile.owner = user
                u_profile.group = "tech"
                u_profile.save()
                address = a_form.save(commit = False)
                address.profile = u_profile
                address.save()

                messages.success(request,f"le technicien {username} est creé avec success")
                return redirect("list_tech")

        else :
            u_form = AddAdminForm()
            p_form = ProfileAdminForm()
            a_form = AddressTechForm()

        return render(request,"manager/register_employee.html" ,{"u_form":u_form ,"p_form":p_form ,"a_form":a_form})
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
        a_form = AddressTechForm(instance = tech.profile.address)

        if request.method == 'POST'  :
            u_form = UserChangeInfoForm( request.POST ,instance = tech )
            p_form = ProfileAdminForm(request.POST ,instance = tech.profile)
            a_form = AddressTechForm(request.POST ,instance = tech.profile.address)

            if u_form.is_valid() and p_form.is_valid() and a_form.is_valid() :
                email1 = u_form.cleaned_data["email"]
                if User.objects.filter(email = email1).exclude(username = tech.username).exists():
                    error1 = "l'adresse e-mail que vous avez entrée est déjà enregistrée,"
                    return render(request,"manager/tech_info.html",{"u_form":u_form ,"a_form":a_form ,"p_form":p_form,"error1":error1,"tech":tech})
                else :
                    u_form.save()
                    p_form.save()
                    a_form.save()
                    username = tech.username
                    messages.success(request,f"Les informations de {username} ont été modifiées avec succès")
                    return redirect("tech_info" ,id = tech.id)

        return render(request,"manager/tech_info.html",{"u_form":u_form ,"p_form":p_form,"a_form":a_form ,"tech":tech})

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

#recherch un client
@login_required
def search_client(request):
    if request.user.profile.group == "admin" :
        search_element = request.POST["search"]
        clients = User.objects.filter(
         Q(profile__type = "personne") & (Q(username__icontains = search_element) | Q(profile__personne__first_name__icontains = search_element) |
          Q(profile__personne__last_name__icontains = search_element) | Q(profile__phone_number__icontains = search_element) |
          Q(profile__address__region__icontains = search_element) |  Q(profile__address__commune__icontains = search_element) )
        )
        return render(request , "manager/search_client.html",{"clients" : clients})

#recherch un entrprise
def search_entrprise(request):
    if request.user.profile.group == "admin" :
        search_element = request.POST["search"]
        clients = User.objects.filter(
         Q(profile__type = "entreprise") & (Q(username__icontains = search_element) | Q(profile__company__name__icontains = search_element) |
         Q(profile__phone_number__icontains = search_element) | Q(profile__address__region__icontains = search_element) |
         Q(profile__address__commune__icontains = search_element))
        )
        return render(request , "manager/search_entrprise.html",{"clients" : clients})

# <------------------------------ Les Statistiques ------------------------------------------------------------------>

def techs(request):
    if request.user.profile.group == "admin" :
        return render(request,"manager/static_tech.html")
    else :
        return HttpResponse("<h1>Seul l'administrateur peut accéder à cette page</h1>")

def diaras(request):
    if request.user.profile.group == "admin" :
        return render(request,"manager/static_daira.html")
    else :
        return HttpResponse("<h1>Seul l'administrateur peut accéder à cette page</h1>")

def type(request):
    if request.user.profile.group == "admin" :
        return render(request,"manager/static_type.html")
    else :
        return HttpResponse("<h1>Seul l'administrateur peut accéder à cette page</h1>")

def evolution(request):
    if request.user.profile.group == "admin" :
        return render(request,"manager/static_evolution.html")
    else :
        return HttpResponse("<h1>Seul l'administrateur peut accéder à cette page</h1>")

def evolution_day(request):
    if request.user.profile.group == "admin" :
        month = datetime.now().strftime("%B")
        return render(request,"manager/static_evolution_day.html",{"month":month})
    else :
        return HttpResponse("<h1>Seul l'administrateur peut accéder à cette page</h1>")

#<--------------------------- Rest Framework API ----------------------------------->

#send the new reclamations as a json format
class ReclamationSetView(viewsets.ViewSet):
    
    permission_classes = (permissions.IsAuthenticated , IsManager,)

    def list(self, request):
        queryset = Requet.objects.filter(state = "ont étape de traitement")
        serializer = ReclamationSerializer(queryset, many=True)
        return Response(serializer.data)

#send the noted reclamations as a json format
class NotesSetView(viewsets.ViewSet):
    
    permission_classes = (permissions.IsAuthenticated , IsManager,)

    def list(self, request):
        queryset = Requet.objects.filter(state = "notée")
        serializer = ReclamationSerializer(queryset, many=True)
        return Response(serializer.data)

#sending the data as a json format
class DataChart(APIView):

    permission_classes = (permissions.IsAuthenticated , IsManager,)

    def get(self, request, format=None):
        techs = []
        works = []
        daira = ["bouira","sour","hachimia"]
        reclamations = []
        types = ["Coupage telephonique" ,"Autre Problem" , "Problem internet"]
        reclamtions_type = []
        begenning_date = datetime(2019,1,1)
        weeks = []
        weeks_show = []
        reclamation_week = []
        beg_date = datetime(2019,datetime.now().month,1)
        days = []
        days_show = []
        reclamation_day = []

        # all the weeks for this year
        date1 = begenning_date
        while date1 < datetime.now():
            add = date1.day + 7
            if date1.month == 2 :
                if add <= 28 :
                    date1 = date1.replace(day = add)
                    weeks.append(date1)
                else :
                    add1 = 28 - date1.day
                    add = 7 - add1
                    add_month = date1.month + 1
                    date1 = date1.replace(day = add)
                    date1 = date1.replace(month = add_month)
                    weeks.append(date1)
            elif date1.month % 2 == 0 :
                if add <= 30 :
                    date1 = date1.replace(day = add)
                    weeks.append(date1)
                else :
                    add1 = 30 - date1.day
                    add = 7 - add1
                    add_month = date1.month + 1
                    date1 = date1.replace(day = add)
                    date1 = date1.replace(month = add_month)
                    weeks.append(date1)
            else  :
                if add <= 31 :
                    date1 = date1.replace(day = add)
                    weeks.append(date1)
                else :
                    add1 = 31 - date1.day
                    add = 7 - add1
                    add_month = date1.month + 1
                    date1 = date1.replace(day = add)
                    date1 = date1.replace(month = add_month)
                    weeks.append(date1)

        #all this month days :
        while beg_date < datetime.now() :
            days.append(beg_date)
            beg_date = beg_date.replace(day = beg_date.day + 1)

        #les reclamation de chaque jour :
        for index in range(1,len(days)):
            rec = Requet.objects.filter(pub_date__range = (days[index-1] ,days[index])).count()
            reclamation_day.append(rec)

        #les reclamation par chaque semaine
        for index in range(1,len(weeks)):
            rec = Requet.objects.filter(pub_date__range = (weeks[index-1] ,weeks[index])).count()
            reclamation_week.append(rec)

        # reclamation de chaque categorie(type)
        for type in  types :
            rec_type = Requet.objects.filter(problem = type).count()
            reclamtions_type.append(rec_type)

        # reclamation de chaque daira
        for item in  daira :
            rec_par_daira = Requet.objects.filter(client__profile__address__region = item).count()
            reclamations.append(rec_par_daira)

        #reclamation de fixée par chaque tech
        for tech in User.objects.filter(profile__group = "tech") :
            techs.append(tech.username)
            works.append(tech.works.filter(state = "Problème Résolu").count())


        #orgnaze the weeks appearense
        for week in weeks :
            weeks_show.append(str(week.day) + "/"+ str(week.month) + "/" + str(week.year))

        #orgnaze the days appearense
        for day in days :
            days_show.append(str(day.day) + "/"+ str(day.month) + "/" + str(day.year))

        data = {
        "techs":techs,
        "works":works ,
        "daira":daira,
         "reclamations":reclamations,
         "types" : types,
         "reclamations_type":reclamtions_type,
         "weeks":weeks_show,
         "reclamation_week" : reclamation_week,
         "days" : days_show,
         "reclamation_day" : reclamation_day,
        }

        return Response(data)
