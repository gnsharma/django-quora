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


@pytest.mark.django_db
@pytest.fixture(scope="module")
def user():
    user = User(username='gns', email='gns@gns.com', password='123')
    user.save()
    return user


@pytest.mark.django_db
@pytest.fixture(scope="module")
def profile(user):
    profile = Profile(user=user)
    profile.save()
    return profile


@pytest.mark.django_db
@pytest.fixture(scope="module")
def topic():
    topic = Topic(topic_text='default topic')
    topic.save()
    return topic


@pytest.mark.django_db
@pytest.fixture(scope="module")
def question(user):
    question = Question(question_text='default question', user=user)
    question.save()
    return question


@pytest.mark.django_db
@pytest.fixture(scope="module")
def answer(user, question):
    answer = Answer(answer_text='default answer', question=question, user=user)
    answer.save()
    return answer


@pytest.mark.django_db
@pytest.fixture(scope="module")
def questionvotes(question, user):
    questionvote = QuestionVotes(question=question, user=user)
    questionvote.save()
    return questionvote


@pytest.mark.django_db
@pytest.fixture(scope="module")
def answervotes(answer, user):
    answervote = AnswerVotes(answer=answer, user=user)
    answervote.save()
    return answervote


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
        assert Topic.objects.get(topic_text=text)


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
        assert Question.objects.get(question_text=text, pub_date=date)


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


examples = (("text", "date", "result", "comment"),
            [
                ("question text", timezone.now() + datetime.timedelta(days=5), False, "future question"),
                ("question text", timezone.now() - datetime.timedelta(days=5), False, "old question"),
                ("question text", timezone.now() - datetime.timedelta(hours=5), True, "recent question"),
            ])


@pytest.mark.parametrize(*examples)
def test_question_was_published_recently(question, text, date, result, comment):
    question.pub_date = date
    question.question_text = text
    assert question.was_published_recently() is result


def test_str_returns_username_in_profile(profile):
    profile.user.username = 'some username'
    assert str(profile) == profile.user.username


def test_str_returns_topic_text_in_topic(topic):
    topic.topic_text = 'some topic'
    assert str(topic) == topic.topic_text


def test_str_returns_question_text_in_question(question):
    question.question_text = 'some question'
    assert str(question) == question.question_text


def test_str_returns_answer_text_in_answer(answer):
    answer.answer_text = 'some answer'
    assert str(answer) == answer.answer_text


def test_str_returns_vote_value_in_questionvotes(questionvotes):
    questionvotes.value = 1
    assert str(questionvotes) == str(questionvotes.value)


def test_str_returns_vote_value_in_answervotes(answervotes):
    answervotes.value = 1
    assert str(answervotes) == str(answervotes.value)

