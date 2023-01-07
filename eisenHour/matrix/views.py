from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotAllowed
from .forms import UserRegistrationForm, TaskForm, UrgencyDurationForm
from django.contrib.auth.decorators import login_required
from .models import Task
from django.core.exceptions import ObjectDoesNotExist
from datetime import *
import itertools

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


@login_required
def showMatrix(request):
    user = request.user
    today = datetime.today()
    urgentTasksDate = today + user.urgencyTimeRange
    urgentAndImportantTasks = user.tasks.filter(
        status=True, importance=True, date__lt=urgentTasksDate)
    importantTasks = user.tasks.filter(
        status=True, importance=True, date__gt=urgentTasksDate)
    urgentTasks = user.tasks.filter(
        status=True, importance=False, date__lt=urgentTasksDate)
    notUrgentNotImportantTasks = user.tasks.filter(
        status=True, importance=False, date__gt=urgentTasksDate)
    firstRow = itertools.zip_longest(urgentAndImportantTasks, importantTasks)
    secondRow = itertools.zip_longest(
        urgentTasks, notUrgentNotImportantTasks, fillvalue=None)
    return render(request, "matrix/matrix.html", {"firstRow": firstRow, "secondRow": secondRow, "urgencyForm":UrgencyDurationForm()})


@login_required
def changeUrgencyTimeRange(request):
    if request.method == "POST":
        durationForm = UrgencyDurationForm(request.POST)
        if durationForm.is_valid():
            user = request.user
            user.urgencyTimeRange = durationForm.cleaned_data["duration"]
            user.save()
    return redirect("matrix")


@login_required
def showArchive(request):
    user = request.user
    archivedTasks = user.tasks.filter(status=False)
    return render(request,"matrix/archive.html",{"archivedTasks":archivedTasks})