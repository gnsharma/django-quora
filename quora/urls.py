from django.urls import path

from quora.views.common import RedirectView, HomeView

app_name = 'quora'
urlpatterns = [
    path('', RedirectView.as_view(), name='redirect'),
    path('quora', HomeView.as_view(), name='home'),
]
