from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from .models import Task
from django.core.exceptions import ObjectDoesNotExist


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

@login_required
def showTask(request,taskId):
    task = get_object_or_404(Task, id = taskId, user = request.user)
    return render(request,"matrix/task.html",{"task":task})