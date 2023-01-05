from .models import User, Task
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm, widgets


class UserRegistrationForm(UserCreationForm):
	email = forms.EmailField(required=True)
	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")


class TaskForm(ModelForm):
	class Meta:
		model = Task
		fields = ["title", "description", "date", "importance"]
		widgets = {
            'date': widgets.DateInput(attrs={'type': 'date'})
        }