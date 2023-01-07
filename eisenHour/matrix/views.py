from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotAllowed
from .forms import UserRegistrationForm, TaskForm
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
        return render(request, "registration/register.html", {"form": newUserForm})
    return render(request, "registration/register.html", {"form": UserRegistrationForm()})


@login_required
def showTask(request, taskId):
    task = get_object_or_404(Task, id=taskId, user=request.user)
    return render(request, "matrix/task.html", {"task": task})


@login_required
def addTask(request):
    if request.method == "POST":
        newTask = Task(user=request.user, status=True)
        taskForm = TaskForm(request.POST, instance=newTask)
        if taskForm.is_valid():
            taskForm.save()
            return redirect("first")
            # TODO: update with home screen url
        return render(request, "matrix/add.html", {"form": taskForm})
    return render(request, "matrix/add.html", {"form": TaskForm()})


@login_required
def editTask(request, taskId):
    task = get_object_or_404(Task, id=taskId, user=request.user)
    if request.method == "POST":
        taskForm = TaskForm(request.POST, instance=task)
        if taskForm.is_valid():
            taskForm.save()
            return redirect("first")
            # TODO: update with home screen url
        return render(request, "matrix/edit.html", {"form": taskForm, "taskId": taskId})
    return render(request, "matrix/edit.html", {"form": TaskForm(instance=task), "taskId": taskId})


@login_required
def finishTask(request, taskId):
    task = get_object_or_404(Task, id=taskId, user=request.user)
    if request.method == "POST":
        task.status = False if task.status == True else True
        task.save()
        return redirect("task", taskId)
    return HttpResponseNotAllowed("wrong operation")
