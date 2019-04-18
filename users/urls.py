from django.urls import path , include
from . import views

urlpatterns = [
    path('',views.register,name="register" ),
    path('login/',views.login_view,name="login" ),
    path('client_info/',views.user_info,name="client_info"),
    path('entreprise_info/',views.entreprise_info,name="entreprise_info"),
    path('logout/',views.logout_view,name="logout" ),
    path('login_tech/',views.login_tech,name="login_tech" ),
    path('client/<int:id_client>/<int:id_requet>/',views.requet_info,name="requet_info" ),
    path("register_personne/<int:id>/",views.register_personne,name="register_personne"),
    path("register_entreprise/<int:id>/",views.register_entreprise,name="register_entreprise"),
    path("problem_fixed/<int:id>/",views.problem_fixed,name="problem_fixed"),
]
