import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils import timezone

from quora.models import Profile, Question, Answer, Topic
from quora.forms import SignupForm, LoginForm


class AddAnswerView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        
