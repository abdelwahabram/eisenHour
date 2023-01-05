from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserRegistrationForm

# Create your views here.

def first(request):
    return HttpResponse("awesome")

def register(request):
    if request.method == "POST":
        newUserForm = UserRegistrationForm(request.POST)
        if newUserForm.is_valid():
            newUserForm.save()
            return redirect("first")
            # TODO: update with home screen url
        return render(request,"registration/register.html",{"form":newUserForm})
    return render(request,"registration/register.html",{"form":UserRegistrationForm()})
