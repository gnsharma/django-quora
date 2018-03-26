import datetime
import pytest

from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

from quora.models import validate_text, validate_date, validate_vote
from quora.models import Profile, Question, Topic, Answer, QuestionVotes, AnswerVotes


examples = (("text", "date", "result", "comment"),
            [
                ("question text 1", timezone.now() + datetime.timedelta(days=5), False, "future date"),
                ("question text 2", timezone.now() - datetime.timedelta(days=5), True, "past date"),
                ("question text 3", timezone.now(), True, "now"),
                ("question text 4", timezone.now(), True, "question is not empty"),
                ("", timezone.now(), False, "empty question"),
            ])


@pytest.mark.django_db
@pytest.mark.parametrize(*examples)
def test_question_model(question, user, text, date, result, comment):
    question.pub_date = date
    question.question_text = text
    question.user = user
    if result is False:
        with pytest.raises(ValidationError):
            question.save()
    else:
        question.save()
        question = Question.objects.get(question_text=text, pub_date=date)
        assert question.question_text == text
        assert question.pub_date == date


examples = (("text", "date", "result", "comment"),
            [
                ("question text", timezone.now() + datetime.timedelta(days=5), False, "future question"),
                ("question text", timezone.now() - datetime.timedelta(days=5), False, "old question"),
                ("question text", timezone.now() - datetime.timedelta(hours=5), True, "recent question"),
            ])


@pytest.mark.django_db
@pytest.mark.parametrize(*examples)
def test_question_was_published_recently(question, text, date, result, comment):
    question.pub_date = date
    question.question_text = text
    assert question.was_published_recently() is result
