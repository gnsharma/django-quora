from django.conf.urls import url

from quora.views.common import HomeView, SignupView, LogoutView
from quora.views.questions import FeedView, AddQuestionView, QuestionView, QuestionVotesView
from quora.views.answers import AddAnswerView, AnswerVotesView
from quora.views.topics import AddTopicView

app_name = 'quora'
urlpatterns = [
    url(r'^signup$', SignupView.as_view(), name='signup'),
    url(r'^login$', HomeView.as_view(), name='login'),
    url(r'^logout$', LogoutView.as_view(), name='logout'),
    url(r'^feed$', FeedView.as_view(), name='feed'),
    # url(r'^questions/(?P<id>[0-9])/$', QuestionView.as_view(), name='question'),
    url(r'^questions', QuestionView.as_view(), name='question'),
    url(r'^vote/question$', QuestionVotesView.as_view(), name='question-vote'),
    url(r'^vote/answer$', AnswerVotesView.as_view(), name='answer-vote'),
    url(r'^add/answers/(?P<qid>[0-9])/$', AddAnswerView.as_view(), name='add-answer'),
    url(r'^add/questions$', AddQuestionView.as_view(), name='add-question'),
    url(r'^add/topics$', AddTopicView.as_view(), name='add-topic'),
    url(r'', HomeView.as_view(), name='home'),
]
