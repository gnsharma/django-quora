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

from quora.models import Profile, Question, Answer, Topic, AnswerVotes
from quora.forms import AnswerForm


class AddAnswerView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        topics = Topic.objects.all()
        question = Question.objects.get(pk=request.GET.get('qid'))
        form = AnswerForm()
        return render(request, 'quora/feed/add_answer.haml', {'topics': topics, 'question': question, 'form': form})

    def post(self, request, *args, **kwargs):
        topics = Topic.objects.all()
        question = Question.objects.get(pk=request.POST.get('qid'))
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = Answer()
            answer.answer_text = form.cleaned_data['answer']
            answer.question = Question.objects.get(pk=request.POST.get('qid'))
            answer.user = request.user
            answer.save()
            return HttpResponseRedirect(reverse('quora:question') + "?id=" + kwargs['id'])
        else:
            return render(request, 'quora/feed/add_answer.haml',
                          {'topics': topics, 'question': question, 'form': form})


class AnswerVotesView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        answer_id = int(request.POST.get('id'))
        vote_type = request.POST.get('type')

        try:
            vote = AnswerVotes.objects.get(answer__id=answer_id, user=request.user)
        except ObjectDoesNotExist:
            vote = AnswerVotes()
            vote.answer = Answer.objects.get(pk=answer_id)
            vote.user = request.user
            vote.save()
        finally:
            current_vote = vote.vote
            if (vote_type == 'up'):
                if (current_vote == 0):
                    vote.vote = 1
                if (current_vote == 1):
                    vote.vote = 0
                if (current_vote == -1):
                    vote.vote = 1
            elif (vote_type == 'down'):
                if (current_vote == 0):
                    vote.vote = -1
                if (current_vote == 1):
                    vote.vote = 0
                if (current_vote == -1):
                    vote.vote = 0
            else:
                return HttpResponse('Error - bad action')

            vote.save()
            up_count = AnswerVotes.objects.filter(answer__id=answer_id, vote=1).count()
            down_count = AnswerVotes.objects.filter(answer__id=answer_id, vote=-1).count()
            total = up_count - down_count
            return HttpResponse(json.dumps({'vote': vote.vote, 'total': total,
                                            'up_count': up_count, 'down_count': down_count}))
