import datetime
import pytest

from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

from quora.models import validate_text, validate_date, validate_vote
from quora.models import Profile, Question, Topic, Answer, QuestionVotes, AnswerVotes


@pytest.mark.django_db
def test_str_returns_username_in_profile(profile):
    profile.user.username = 'some username'
    assert str(profile) == profile.user.username


@pytest.mark.django_db
def test_str_returns_topic_text_in_topic(topic):
    topic.topic_text = 'some topic'
    assert str(topic) == topic.topic_text


@pytest.mark.django_db
def test_str_returns_question_text_in_question(question):
    question.question_text = 'some question'
    assert str(question) == question.question_text


@pytest.mark.django_db
def test_str_returns_answer_text_in_answer(answer):
    answer.answer_text = 'some answer'
    assert str(answer) == answer.answer_text


@pytest.mark.django_db
def test_str_returns_vote_value_in_questionvotes(questionvotes):
    questionvotes.value = 1
    assert str(questionvotes) == str(questionvotes.value)


@pytest.mark.django_db
def test_str_returns_vote_value_in_answervotes(answervotes):
    answervotes.value = 1
    assert str(answervotes) == str(answervotes.value)
