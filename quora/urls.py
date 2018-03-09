from django.conf.urls import url

from quora.views.common import HomeView, SignupView, LogoutView

app_name = 'quora'
urlpatterns = [
    url(r'^signup', SignupView.as_view(), name='signup'),
    url(r'^login', HomeView.as_view(), name='login'),
    url(r'^logout', LogoutView.as_view(), name='logout'),
    url(r'', HomeView.as_view(), name='home'),
]
