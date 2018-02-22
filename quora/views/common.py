from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

class RedirectView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('quora:home'))


class HomeView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'quora/common/home.haml')


