import datetime
import pytest

from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

from quora.models import validate_text, validate_date, validate_vote
from quora.models import Profile, Question, Topic, Answer, QuestionVotes, AnswerVotes


examples = (("date", "result", "comment"),
            [
                (timezone.now() + datetime.timedelta(days=5), False, "future date"),
                (timezone.now() - datetime.timedelta(days=5), True, "past date"),
                (timezone.now(), True, "now"),
            ])


@pytest.mark.parametrize(*examples)
def test_validate_date(date, result, comment):
    if result is False:
        with pytest.raises(ValidationError):
            validate_date(date)
    else:
        assert validate_date(date) is result


examples = (("text", "result", "comment"),
            [
                ("Not empty", True, "not empty string"),
                ("", False, "empty string"),
            ])


@pytest.mark.parametrize(*examples)
def test_validate_text(text, result, comment):
    if result is False:
        with pytest.raises(ValidationError):
            validate_text(text)
    else:
        assert validate_text(text) is result


examples = (("value", "result", "comment"),
            [
                (1, True, "Should be valid"),
                (0, True, "Should be valid"),
                (-1, True, "Should be valid"),
                (10, False, "Should not be valid"),
                (-10, False, "Should not be valid"),
            ])


@pytest.mark.parametrize(*examples)
def test_validate_vote(value, result, comment):
    if result is False:
        with pytest.raises(ValidationError):
            validate_vote(value)
    else:
        assert validate_vote(value) is result

