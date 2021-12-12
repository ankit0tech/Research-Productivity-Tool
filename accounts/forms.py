from django import forms
from django.contrib.auth.models import User
from accounts.models import UserProfile
from department.models import Department

class CreateUserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('linkedin_url', 'profile_pic', 'department', 'course', 'year', 'description')