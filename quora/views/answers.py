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
        return render(request, 'quora/feed/answer.haml', {})


class AnswerVotesView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        answer_id = int(request.POST.get('id'))
        vote_type = request.POST.get('type')

        answer = Answer.objects.get(pk=answer_id)

        if (vote_type == 'up'):
            answer.votes += 1
            answer.save()
        elif (vote_type == 'down'):
            answer.votes -= 1
            answer.save()
        else:
            return HttpResponse('Error - bad action')

        return HttpResponse(answer.votes)

