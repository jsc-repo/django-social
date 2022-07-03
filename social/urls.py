from unicodedata import name
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include(("dwitter.urls", "dwitter"), namespace="dwitter")),
    path("admin/", admin.site.urls),
]
