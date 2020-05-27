from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from Insta.models import CustomUser, Post

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'profile_pic')

class CustomPostCreationForm(ModelForm):
    class Meta:
        model = Post
        exclude = ('author',)  # this results in the fields 'author' not being present on the form.

    def __init__(self, *args, **kwargs):
        # pop(key[, default]) if key is in the dictionary, 
        # remove it and return its value, else return default. 
        self.user = kwargs.pop('author')
        super(CustomPostCreationForm, self).__init__(*args, **kwargs)