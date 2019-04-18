from django.urls import path
from . import views

urlpatterns = [
    path("",views.login_manager,name="login_manager"),
    path("home/",views.home,name="manager_home"),
    path("requets/",views.RequetsListView.as_view(),name="manager_requets"),
    path("aprove_requet/<int:id>/",views.aprove,name="aprove_requet"),
    path("delete_requet/<int:pk>/",views.RequetDeleteView.as_view(),name="manager_delete_requet"),
    path("edit_requet/<int:id>/",views.edit_requet,name="edit_requet"),
]
