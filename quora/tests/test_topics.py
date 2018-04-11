import datetime
import pytest

from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

from quora.models import validate_text, validate_date, validate_vote
from quora.models import Profile, Question, Topic, Answer, QuestionVotes, AnswerVotes


examples = (("text", "result", "comment"),
            [
                ("topic text", True, "topic is not empty"),
                ("", False, "empty topic"),
])


@pytest.mark.django_db
@pytest.mark.parametrize(*examples)
def test_topic_model(topic, text, result, comment):
    topic.topic_text = text
    if result is False:
        with pytest.raises(ValidationError):
            topic.save()
    else:
        topic.save()
        topic = Topic.objects.get(topic_text=text)
        assert topic.topic_text == text
