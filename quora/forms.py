from django.forms import ModelChoiceField, ModelMultipleChoiceField, EmailField, CharField, Form
from django.forms import ModelForm, Textarea, PasswordInput

from quora.models import Topic


class SignupForm(Form):

    username = CharField(
        label='User Name',
        max_length=150,
        help_text='150 characters or fewer. Usernames may c  ontain alphanumeric, _, @, +, . and - characters.')
    first_name = CharField(label='First Name', max_length=150)
    last_name = CharField(label='Last Name', max_length=150)
    email = EmailField(label='Email')
    password = CharField(label='Password', widget=PasswordInput, max_length=150)


class LoginForm(Form):

    username = CharField(label='User Name', max_length=150)
    password = CharField(label='Password', widget=PasswordInput, max_length=150)


class AnswerForm(Form):

    answer = CharField(label='Answer', widget=Textarea)


class QuestionForm(Form):

    question = CharField(label='Ask your question')
    # topics = ModelMultipleChoiceField(queryset=Topic.objects.all())
    topics = CharField(label='Topics')
