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
from quora.forms import SignupForm, LoginForm, QuestionForm
from quora.views.answers import voting_logic


class FeedView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        topic = request.GET.get('topic')

        if topic is None:
            latest_questions_list = Question.objects.filter(pub_date__lte=timezone.now()).filter(
                pub_date__gte=timezone.now() - datetime.timedelta(days=1)).order_by('-pub_date')
            return render(request, 'quora/feed/latest_feed.haml',
                          {'questions': latest_questions_list})
        else:
            questions = Question.objects.filter(topics__topic_text=topic)
            return render(request, 'quora/feed/latest_feed.haml', {'questions': questions})


class QuestionView(View):

    def get(self, request, *args, **kwargs):
        question = Question.objects.get(pk=request.GET.get('id'))
        return render(request, 'quora/feed/question.haml', {'question': question})


class AddQuestionView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        form = QuestionForm()
        return render(request, 'quora/feed/add_question.haml', {'form': form})

    def post(self, request, *args, **kwargs):
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = Question()
            question.question_text = form.cleaned_data['question']
            question.user = request.user
            topic = Topic.objects.get(topic_text=form.cleaned_data['topics'])
            question.save()
            question.topics.add(topic)
            question.save()
            return HttpResponseRedirect(reverse('quora:feed'))
        else:
            return render(request, 'quora/feed/add_question.haml', {'form': form})


class QuestionVotesView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        question_id = int(request.POST.get('id'))
        vote_type = request.POST.get('type')

        try:
            vote = QuestionVotes.objects.get(
                question__id=question_id, user=request.user)
        except ObjectDoesNotExist:
            vote = QuestionVotes()
            vote.question = Question.objects.get(pk=question_id)
            vote.user = request.user
            vote.save()
        finally:
            voting_logic(vote_type, vote)

            vote.save()
            up_count = QuestionVotes.objects.filter(
                question__id=question_id, value=1).count()
            down_count = QuestionVotes.objects.filter(
                question__id=question_id, value=-1).count()
            total = up_count - down_count
            return HttpResponse(json.dumps({'vote': vote.value, 'total': total,
                                            'up_count': up_count, 'down_count': down_count}))
