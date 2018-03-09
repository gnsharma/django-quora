from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib import messages

from quora.models import Profile
from quora.forms import SignupForm, LoginForm


class SignupView(View):

    def get(self, request, *args, **kwargs):
        form = SignupForm()
        return render(request, 'quora/common/signup.haml', {'form': form})

    def post(self, request, *args, **kwargs):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = User()
            user.password = make_password(form.cleaned_data['password'])
            user.username = form.cleaned_data['username']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            profile = Profile(user=user)
            profile .save()
            return HttpResponseRedirect(reverse('quora:login'))
        else:
            return render(request, 'quora/common/signup.haml', {'form': form})


class HomeView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, 'quora/feed/feed.haml', {})
        else:
            form = LoginForm()
            return render(request, 'quora/common/home.haml', {'form': form})
        
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'quora/feed/feed.haml', {})
                else:
                    return HttpResponse('Your account is disabled.')

            else:
                messages.error(request, "User credentials are not correct.")
                return render(request, 'quora/common/home.haml', {'form': form})

        else:
            return render(request, 'quora/common/home.haml', {'form': form})


class LogoutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('quora:home'))
