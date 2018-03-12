import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils import timezone

from quora.models import Profile, Question, Answer, Topic


class AddAnswerView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        question = Question.objects.get(pk=kwargs['id'])
        form = AnswerForm()
        return render(request, 'quora/feed/answer.haml', {'form': form})
