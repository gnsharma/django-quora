import datetime
import pytest

from django.contrib.auth.models import User
from django.utils import timezone

from quora.models import Profile, Question, Topic, Answer, QuestionVotes, AnswerVotes


@pytest.fixture(scope="module")
def user():
    return User()


@pytest.fixture
def profile(user):
    return Profile(user=user)


@pytest.fixture
def topic():
    return Topic()


@pytest.fixture
def question(user):
    return Question(user=user)


@pytest.fixture
def answer(question, user):
    return Answer(question=question, user=user)


@pytest.fixture
def questionvotes(question, user):
    return QuestionVotes(question=question, user=user)


@pytest.fixture
def answervotes(answer, user):
    return AnswerVotes(answer=answer, user=user)


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


examples = (("text", "date", "result", "comment"),
            [
                ("question text", timezone.now() + datetime.timedelta(days=5), False, "future date"),
                ("question text", timezone.now() - datetime.timedelta(days=5), True, "past date"),
                ("question text", timezone.now(), True, "now"),
            ])


@pytest.mark.parametrize(*examples)
def test_question_has_correct_date(question, text, date, result, comment):
    question.pub_date = date
    question.question_text = text
    assert question.has_correct_date() is result


examples = (("text", "date", "result", "comment"),
            [
                ("question text", timezone.now(), True, "Question text not empty"),
                ("", timezone.now(), False, "Question text is empty"),
            ])


@pytest.mark.parametrize(*examples)
def test_is_question_text_valid(question, text, date, result, comment):
    question.pub_date = date
    question.question_text = text
    assert question.is_question_text_valid() is result


examples = (("text", "result", "comment"),
            [
                ("topic text", True, "Topic text not empty"),
                ("", False, "Topic text is empty"),
            ])


@pytest.mark.parametrize(*examples)
def test_is_topic_text_valid(topic, text, result, comment):
    topic.topic_text = text
    assert topic.is_topic_text_valid() is result


examples = (("text", "result", "comment"),
            [
                ("answer text", True, "Answer text not empty"),
                ("", False, "Answer text is empty"),
            ])


@pytest.mark.parametrize(*examples)
def test_is_answer_text_valid(answer, text, result, comment):
    answer.answer_text = text
    assert answer.is_answer_text_valid() is result


examples = (("value", "result", "comment"),
            [
                (1, True, "Should be valid"),
                (0, True, "Should be valid"),
                (-1, True, "Should be valid"),
                (10, False, "Should not be valid"),
                (-10, False, "Should not be valid"),
            ])


@pytest.mark.parametrize(*examples)
def test_questionvotes_has_correct_value(questionvotes, value, result, comment):
    questionvotes.value = value
    assert questionvotes.has_correct_value() is result


@pytest.mark.parametrize(*examples)
def test_answervotes_has_correct_value(answervotes, value, result, comment):
    answervotes.value = value
    assert answervotes.has_correct_value() is result


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

