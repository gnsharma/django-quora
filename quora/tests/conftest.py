import pytest

from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

from quora.models import validate_text, validate_date, validate_vote
from quora.models import Profile, Question, Topic, Answer, QuestionVotes, AnswerVotes


@pytest.mark.django_db
@pytest.fixture
def user():
    user = User(username='gns', email='gns@gns.com', password='123')
    user.save()
    return user


@pytest.mark.django_db
@pytest.fixture
def profile(user):
    profile = Profile(user=user)
    profile.save()
    return profile


@pytest.mark.django_db
@pytest.fixture
def topic():
    topic = Topic(topic_text='default topic')
    topic.save()
    return topic


@pytest.mark.django_db
@pytest.fixture
def question(user):
    question = Question(question_text='default question', user=user)
    question.save()
    return question


@pytest.mark.django_db
@pytest.fixture
def answer(user, question):
    answer = Answer(answer_text='default answer', question=question, user=user)
    answer.save()
    return answer


@pytest.mark.django_db
@pytest.fixture
def questionvotes(question, user):
    questionvote = QuestionVotes(question=question, user=user)
    questionvote.save()
    return questionvote


@pytest.mark.django_db
@pytest.fixture
def answervotes(answer, user):
    answervote = AnswerVotes(answer=answer, user=user)
    answervote.save()
    return answervote
