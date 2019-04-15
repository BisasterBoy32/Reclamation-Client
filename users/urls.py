from django.urls import path , include
from . import views

urlpatterns = [
    path('',views.register,name="register" ),
    path('login/',views.login_view,name="login" ),
    path('client_info/',views.user_info,name="client_info"),
    path('logout/',views.logout_view,name="logout" ),
]
