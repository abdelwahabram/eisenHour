from . import views
from django.urls import path, include

urlpatterns = [
    path("", views.main, name="main"),
    path("matrix", views.showMatrix, name="matrix"),
    path("register", views.register, name="register"),
    path('accounts/', include('django.contrib.auth.urls')),
    path("task/<int:taskId>", views.showTask, name="task"),
    path("task/add", views.addTask, name="add"),
    path("edit/<int:taskId>", views.editTask, name="edit"),
    path("done/<int:taskId>", views.finishTask, name="done"),
    path("change-duration", views.changeUrgencyTimeRange, name="duration"),
    path("archive", views.showArchive, name="archive"),
]
