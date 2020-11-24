from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
from cloudinary.forms import CloudinaryFileField

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username','email']

class UserProfileUpdateForm(forms.ModelForm):
    image = CloudinaryFileField(
        options = {
            'crop':'thumb',
            'width':300,
            'height':300,
        }
    )
    class Meta:
        model = UserProfile
        fields = ['image']