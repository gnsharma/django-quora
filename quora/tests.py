import datetime

from django.utils import timezone

from quora.models import Question


def test_was_published_recently_with_future_question():
    time = timezone.now() + datetime.timedelta(days=30)
    future_question = Question(pub_date=time)
    assert future_question.was_published_recently() is False


def test_was_published_recently_with_old_question():
    time = timezone.now() - datetime.timedelta(days=1, seconds=1)
    old_question = Question(pub_date=time)
    assert old_question.was_published_recently() is False


def test_was_published_recently_with_recent_question():
    time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
    recent_question = Question(pub_date=time)
    assert recent_question.was_published_recently() is True

