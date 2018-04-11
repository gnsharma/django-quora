import datetime
import pytest

from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

from quora.models import validate_text, validate_date, validate_vote
from quora.models import Profile, Question, Topic, Answer, QuestionVotes, AnswerVotes


examples = (("value", "result", "comment"),
            [
                (1, True, "Should be valid"),
                (0, True, "Should be valid"),
                (-1, True, "Should be valid"),
                (10, False, "Should not be valid"),
                (-10, False, "Should not be valid"),
])


@pytest.mark.django_db
@pytest.mark.parametrize(*examples)
def test_questionvotes_model(questionvotes, value, result, comment):
    questionvotes.value = value
    if result is False:
        with pytest.raises(ValidationError):
            questionvotes.save()


@pytest.mark.django_db
@pytest.mark.parametrize(*examples)
def test_answervotes_model(answervotes, value, result, comment):
    answervotes.value = value
    if result is False:
        with pytest.raises(ValidationError):
            answervotes.save()
