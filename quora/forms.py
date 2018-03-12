from django.forms import EmailField, CharField, Form
from django.forms import PasswordInput


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

    answer = CharField(label='Answer')
