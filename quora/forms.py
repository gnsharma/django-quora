from django.forms import ModelChoiceField, ModelMultipleChoiceField, EmailField, CharField, Form
from django.forms import ModelForm, Textarea, HiddenInput, PasswordInput

from quora.models import Topic
from quora.tasks import send_feedback_email_task


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


class TopicForm(Form):

    topic = CharField(label='Topic')


class FeedbackForm(Form):
    email = EmailField(label="Email Address")
    message = CharField(label="Message", widget=Textarea(attrs={'rows': 5}))
    honeypot = CharField(widget=HiddenInput(), required=False)

    def send_email(self):
        send_feedback_email_task.delay(self.cleaned_data['email'], self.cleaned_data['message'])
