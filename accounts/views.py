from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from accounts.models import UserProfile
from django.contrib.auth.models import User
from django.contrib import messages
from accounts.forms import CreateUserForm, UserProfileForm
from django.urls import reverse, reverse_lazy
from . import forms

def index(request):
    return render(request, 'index.html')

def user_signup(request):
    registered = False

    if request.method == 'POST':
        user_form = CreateUserForm(data = request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user=user     # one to one relationship

            if 'profile_pic' in request.FILES:
                print('profile pic is uploaded')
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            registered = True
        
        else:
            print(user_form.errors,profile_form.errors)
    
    else:
        user_form = CreateUserForm()
        profile_form = UserProfileForm()

    return render(request,'accounts/registration.html',
                            {'user_form': user_form,
                             'profile_form': profile_form,
                             'registered': registered})


def user_login(request):
    active = True
    valid = True
    username = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # is_user = User.objects.get(username = username)

        user = authenticate(username = username,password = password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                active = False
        else:
            valid = False
            print('Someone tried to login with username = {} and password = {}'.format(username, password))

    return render(request, 'accounts/login.html', 
                                               {'username': username,
                                                'active': active,
                                                'valid': valid,})


@login_required
def user_logout(request):
    logout(request)
    return render(request, 'index.html')


@login_required
def user_profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    user_profile = UserProfile.objects.get(username=user.username)
    return render(request,'accounts/user_profile.html', {'user_profile': user_profile,})


@login_required
def update_profile(request, pk):
    user = request.user
    user_profile = UserProfile.objects.get(username=user.username)    

    if request.method == "POST ":
        user_form = CreateUserForm(data = request.POST, instance = user)
        profile_form = UserProfileForm(data = request.POST, instance =  user_profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']    
            profile.save()
            return HttpResponseRedirect(reverse_lazy('accounts:profile', kwargs={'pk': user.pk}))

        else: 
            print(user_form.errors, profile_form.errors)
    
    else:
        user_form = CreateUserForm(instance = user)
        profile_form = UserProfileForm(instance = user_profile)

    return render(request, 'accounts/update_profile.html',
                            {'user_form': user_form,
                             'profile_form': profile_form,})


@login_required
def delete_profile(request, pk):
    user = User.objects.get(pk=pk)
    user_profile = UserProfile.objects.get(username=user.username)
    user.delete()
    user_profile.delete()
    return HttpResponseRedirect(reverse_lazy('index'))

def user_subjects(request, pk):
    user = get_object_or_404(User, pk=pk)
    subjects = user.subjects.all()

    return render(request, 'accounts/user_subjects.html',
                            {'student': user,
                            'subjects': subjects,})