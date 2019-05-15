from django.shortcuts import render , redirect ,get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView , DeleteView , ListView ,DetailView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.contrib.auth.decorators import login_required

from users.forms import UserForm ,ProfileForm
from .forms import RequetForm ,InternetRequetForm
from .models import Requet

# Create your views here.
def home(request):
    u_f = UserForm()
    p_f = ProfileForm()
    return render(request,"users/register.html",{"u_form":u_f, "p_form":p_f})

def choose_problem(request):
    return render(request ,"requets/choose.html")

#problem telephone fix
class RequetCreateView(LoginRequiredMixin ,CreateView):
    model = Requet
    form_class = RequetForm

    def form_valid(self , form):
        form.instance.client = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        username = self.request.user.username
        messages.success(self.request,f"{username} Votre Réclamation Créée Avec Succès")
        return reverse("create_requete")

#problem d'internet
class RequetInternetCreateView(LoginRequiredMixin ,CreateView):
    model = Requet
    template_name = "requets/requet_internet.html"
    form_class = InternetRequetForm


    def form_valid(self , form):
        form.instance.client = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        username = self.request.user.username
        messages.success(self.request,f"{username} Votre Réclamation Créée Avec Succès")
        return reverse("create_requete")


class RequetListView(LoginRequiredMixin ,ListView):
    model = Requet
    context_object_name = "requets"

    def get_queryset(self):
        requets = Requet.objects.filter(client = self.request.user).order_by("-pub_date")
        return requets

class FixRequetView(LoginRequiredMixin ,UserPassesTestMixin ,DetailView):
    model = Requet
    context_object_name = "requet"
    template_name = "requets/requet_fixée.html"

    def test_func(self):
        requet = self.get_object()
        return self.request.user == requet.client and requet.state == "Problème Résolu" and requet.fix_confirm == False

class RequetDeleteView(LoginRequiredMixin , UserPassesTestMixin ,DeleteView):
    model = Requet

    def get_success_url(self):
        return reverse("siuvi_requete")

    def test_func(self):
        requet = self.get_object()
        return self.request.user == requet.client


# <------------------------- tech part --------------------------------------------------->

class TechRequetListView(LoginRequiredMixin , UserPassesTestMixin ,ListView):
    model = Requet
    context_object_name = "requets"
    oreder_by = ["pub_date"]
    template_name = "requets/tech_list.html"

    def get_queryset(self):
        return Requet.objects.filter(tech = self.request.user ).exclude(state = "Problème Résolu").order_by("client__profile__type","pub_date")

    def test_func(self):
        return self.request.user.profile.group == "tech"

# Client part problem resolu avec success
@login_required
def success_view(request , id):
    requet = get_object_or_404(Requet , pk=id )
    if request.user == requet.client :
        requet.fix_confirm = True
        requet.save()
        username = request.user.username
        messages.success(request,f"{username} nous sommes heureux de vous aider à résoudre le problème")
        return redirect("siuvi_requete")
    else :
        return HttpResponse("<h1>403 Forbidden</h1>")
