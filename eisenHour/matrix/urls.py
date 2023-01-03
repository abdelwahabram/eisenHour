from . import views
from django.urls import path, include

urlpatterns = [
    path("", views.first, name="first"),
    path("register", views.register, name="register"),
    path('accounts/', include('django.contrib.auth.urls')),
]
