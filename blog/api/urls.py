from .views import api_create_view, api_delete_view, api_detail_view, api_list_view, api_update_view, api_register_view, PostListView, get_user_properties, api_update_user_properties
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path("home", api_list_view, name="home2"),
    path("<slug:slug>/", api_detail_view, name="detail2"),
    path("users", get_user_properties, name="users"),
    path("users/update", api_update_user_properties, name="user-update"),
    path("<slug:slug>/update", api_update_view, name="update"),
    path("<slug:slug>/delete", api_delete_view, name="delete"),
    path("create", api_create_view, name="create"),
    path("register", api_register_view, name="register"),
    path("login", obtain_auth_token, name="login"),
    path("list", PostListView.as_view(), name="list"),

    
]