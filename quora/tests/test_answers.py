import datetime
import pytest

from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

from quora.models import validate_text, validate_date, validate_vote
from quora.models import Profile, Question, Topic, Answer, QuestionVotes, AnswerVotes


examples = (("text", "result", "comment"),
            [
                ("answer text", True, "Answer text not empty"),
                ("", False, "Answer text is empty"),
            ])


@pytest.mark.django_db
@pytest.mark.parametrize(*examples)
def test_answer_model(answer, text, result, comment):
    answer.answer_text = text
    if result is False:
        with pytest.raises(ValidationError):
            answer.save()
    else:
        answer.save()
        answer = Answer.objects.get(answer_text=text)
        assert answer.answer_text == text

