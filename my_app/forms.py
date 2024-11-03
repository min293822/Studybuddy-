from django.forms import ModelForm
from .models import Room, User
from django import forms
from django.contrib.auth.forms import UserCreationForm


class RoomForm(ModelForm):
  topic = forms.CharField(max_length=200, required=True, error_messages={'required':''})
  class Meta:
    model = Room
    fields = ['topic', 'name', 'description']
  

class UserEditForm(ModelForm):
  class Meta:
    model = User
    fields = ['name', 'email', 'bio', 'avatar']

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']