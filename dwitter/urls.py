from django.urls import path, include
from .views import dashboard, dweet_like, profile_list, profile, register, index, dweet_detail

urlpatterns = [
    path("", index, name="index"),
    path("dashboard", dashboard, name="dashboard"),
    path("register", register, name="register"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("<str:username>/dweet/<int:pk>", dweet_detail, name="dweet_detail"),
    path("profile_list/", profile_list, name="profile_list"),
    path("profile/<int:pk>", profile, name="profile"),
    path("dweet_like/<int:pk>", dweet_like, name="dweet_like" ),
]
