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
from quora.forms import SignupForm, LoginForm


class FeedView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        latest_questions_list = Question.objects.filter(pub_date__lte=timezone.now()).filter(
            pub_date__gte=timezone.now() - datetime.timedelta(days=1)).order_by('-pub_date')
        return render(request, 'quora/feed/latest_feed.haml', {'questions': latest_questions_list})


class QuestionView(View):

    def get(self, request, *args, **kwargs):
        question = Question.objects.get(pk=kwargs['id'])
        return render(request, 'quora/feed/question.haml', {'question': question})


class QuestionVotesView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        question_id = int(request.POST.get('id'))
        vote_type = request.POST.get('type')

        question = Question.objects.get(pk=question_id)

        if (vote_type == 'up'):
            question.votes += 1
            question.save()
        elif (vote_type == 'down'):
            question.votes -= 1
            question.save()
        else:
            return HttpResponse('Error - bad action')

        return HttpResponse(question.votes)












