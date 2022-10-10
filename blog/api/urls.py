from .views import api_create_view, api_delete_view, api_detail_view, api_list_view, api_update_view
from django.urls import path


urlpatterns = [
    path("home", api_list_view, name="home2"),
    path("<slug:slug>/", api_detail_view, name="detail2"),
    path("<slug:slug>/update", api_update_view, name="update"),
    path("<slug:slug>/delete", api_delete_view, name="delete"),
    path("create/", api_create_view, name="create")
]