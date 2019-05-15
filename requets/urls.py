from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('create_requete/',views.choose_problem,name="create_requete"),
    path('create_requete_telephonique/',views.RequetCreateView.as_view(),name="create_requete_telephonique"),
    path('create_requete_internet/',views.RequetInternetCreateView.as_view(),name="create_requete_internet"),
    path('siuvi_requet/',views.RequetListView.as_view(),name="siuvi_requete"),
    path('delete_requet/<int:pk>/',views.RequetDeleteView.as_view(),name="delete_requete"),
    path("tech_requets",views.TechRequetListView.as_view(),name="tech_requets"),
    path("requet_fixée/<int:pk>/",views.FixRequetView.as_view(),name="requet_fixée"),
    path("success_view/<int:id>/",views.success_view,name="success_view"),

]
