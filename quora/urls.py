from django.conf.urls import url

from quora.views.common import HomeView, SignupView, LogoutView
from quora.views.questions import FeedView, QuestionView

app_name = 'quora'
urlpatterns = [
    url(r'^signup/$', SignupView.as_view(), name='signup'),
    url(r'^login/$', HomeView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^feed/$', FeedView.as_view(), name='feed'),
    url(r'^questions/(?P<id>[0-9])/$', QuestionView.as_view(), name='question'),
    url(r'', HomeView.as_view(), name='home'),
]
