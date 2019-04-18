from django.shortcuts import render ,redirect ,get_object_or_404
from django.contrib import auth
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView ,ListView ,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from requets.models import Requet
from .forms import EditRequetForm


# Create your views here.
def home(request):
    return render(request , "manager/list_requets.html")


def login_manager(request):

    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(request ,username = username , password = password)
        if user and user.profile.type == "admin":
            auth.login(request,user)
            messages.success(request,f"welcome {username}")
            return redirect("manager_home")
        elif user.profile.type != "admin ":
            error = f"{username} n'est pas un administrateur, seul l'administrateur peut accéder à cette page"
            return render(request,"manager/login_manager.html",{"error":error})
        else :
            error = " nom d'utilisateur ou mot de passe n'est pas correcte"
            return render(request,"manager/login_manager.html",{"error":error})

    return render(request,"manager/login_manager.html")


class RequetsListView( LoginRequiredMixin , UserPassesTestMixin ,ListView):
    model = Requet
    template_name = "manager/requet_list.html"
    ordering = ["-pub_date"]
    context_object_name = "requets"

    def test_func(self):
        return self.request.user.profile.type == "admin"


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

    if request.user.profile.type == "admin" :
        form = EditRequetForm(instance = requet)

        if request.method == "POST":
            form =  EditRequetForm(request.POST ,instance = requet)
            if form.is_valid():
                form.save()
                messages.success(request,f"{client} Reclamation est modifie avec success")
                return redirect("manager_requets")

        return render(request,"manager/edit_requet.html",{"form":form ,"requet":requet})
    else :
        return HttpResponse("<h1>403 Forbidden </h1>")


@login_required
def aprove(request ,id):
    requet = get_object_or_404(Requet , pk = id)

    if request.method == 'POST' and request.user.profile.group == "admin" :
        requet.aprove()
        return redirect("manager_requets")

    else :
        return HttpResponse("<h1>403 Forbidden </h1>")
