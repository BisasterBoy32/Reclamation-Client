from django.urls import path
from . import views

urlpatterns = [
    path("",views.login_manager,name="login_manager"),
    path("home/",views.home,name="manager_home"),
    path("requets/",views.RequetsListView.as_view(),name="manager_requets"),
    path("aprove_requet/<int:id>/",views.aprove,name="aprove_requet"),
    path("delete_requet/<int:pk>/",views.RequetDeleteView.as_view(),name="manager_delete_requet"),
    path("edit_requet/<int:id>/",views.edit_requet,name="edit_requet"),
    path("requets_approved/",views.RequetsApprovedListView.as_view(),name="manager_approved_requets"),
    path("requets_fixed/",views.RequetsFixedListView.as_view(),name="manager_fixed_requets"),
    path("register_employee/",views.register_employee,name="register_employee"),
    path("register_admin/",views.register_admin,name="register_admin"),
    path("list_tech/",views.TechListView.as_view(),name="list_tech"),
    path("delete_tech/<int:pk>/",views.TechDeleteView.as_view(),name="delete_tech"),
    path("tech_info/<int:id>/",views.tech_info,name="tech_info"),
    path("client_info/<int:id>/",views.client_info,name="manager_client_info"),
    path("requet_info/<int:id>/",views.requet_info,name="manager_requet_info"),
    path("list_personne/",views.PersonneListView.as_view(),name="list_personne"),
    path("delete_personne/<int:pk>/",views.PersonneDeleteView.as_view(),name="delete_personne"),
    path("list_enterprise/",views.enterprise_list,name="list_enterprise"),
    path("search_requet/",views.search_requet,name="search_requet"),
    path("search_client/",views.search_client,name="search_client"),
    path("search_entrprise/",views.search_entrprise,name="search_entrprise"),
]
