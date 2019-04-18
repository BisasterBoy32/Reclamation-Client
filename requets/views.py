from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView , DeleteView , ListView
from .models import Requet
from django.contrib import messages
from .forms import RequetForm
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin

# Create your views here.
def home(request):
    return render(request,"requets/home.html")


class RequetCreateView(CreateView):
    model = Requet
    form_class = RequetForm

    def form_valid(self , form):
        form.instance.client = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        username = self.request.user.username
        messages.success(self.request,f"{username} Votre Réclamation Créée Avec Succès")
        return reverse("create_requete")


class RequetListView(ListView):
    model = Requet
    context_object_name = "requets"

    def get_queryset(self):
        requets = Requet.objects.filter(client = self.request.user).order_by("-pub_date")
        return requets


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
    template_name = "requets/tech_list.html"

    def get_queryset(self):
        return Requet.objects.filter(tech = self.request.user).order_by("client__profile__type","-pub_date")

    def test_func(self):
        return self.request.user.profile.group == "tech"
