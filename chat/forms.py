from django import forms
from django.utils.text import slugify
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Room


class UserRegistrationForm(UserCreationForm):
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    class Meta:
        model =  User
        fields = ['username', 'email',]


class AddRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'room_type']

    def save(self, commit=True):
        instance = super(AddRoomForm, self).save(commit=False)
        instance.slug = slugify(instance.name)
        if commit:
            instance.save()
        return instance
