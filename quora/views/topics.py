import datetime
import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from quora.models import Profile, Question, Answer, Topic, QuestionVotes
from quora.forms import TopicForm


class AddTopicView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        form = TopicForm()
        return render(request, 'quora/feed/add_topic.haml', {'form': form})

    def post(self, request, *args, **kwargs):
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = Topic()
            topic.topic_text = form.cleaned_data['topic']
            topic.save()
            return HttpResponseRedirect(reverse('quora:feed'))
        else:
            return render(request, 'quora/feed/add_topic.haml', {'form': form})
