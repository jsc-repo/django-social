from django.urls import path, include
from .views import dashboard, profile_list, profile, register

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("register", register, name="register"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("profile_list/", profile_list, name="profile_list"),
    path("profile/<int:pk>", profile, name="profile"),
]
