import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_text(value):
    if value == '':
        raise ValidationError(
            _('%(value) Subject can not be empty string.'),
            params={'value': value},
        )
    else:
        return True


def validate_date(value):
    if value >= timezone.now():
        raise ValidationError(
            _('%(value), Date can not be in future.'),
            params={'value': value},
        )
    else:
        return True


def validate_vote(value):
    if value not in [+1, 0, -1]:
        raise ValidationError(
            _('%(value), Vote value should be in [+1, 0, -1].'),
            params={'value': value},
        )
    else:
        return True


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Topic(models.Model):
    topic_text = models.CharField(max_length=256, validators=[validate_text])

    def __str__(self):
        return self.topic_text

    def save(self, *args, **kwargs):
        self.full_clean()
        # Call the "real" save() method in the base class 'models.Model'
        super(Topic, self).save(*args, **kwargs)


class Question(models.Model):
    question_text = models.CharField(max_length=256, validators=[validate_text])
    pub_date = models.DateTimeField('date published', default=timezone.now, validators=[validate_date])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topics = models.ManyToManyField(Topic, blank=True)

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.shor_description = 'Published recently?'

    def save(self, *args, **kwargs):
        self.full_clean()
        # Call the "real" save() method in the base class 'models.Model'
        super(Question, self).save(*args, **kwargs)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=200, validators=[validate_text])
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.answer_text

    def save(self, *args, **kwargs):
        self.full_clean()
        # Call the "real" save() method in the base class 'models.Model'
        super(Answer, self).save(*args, **kwargs)


class QuestionVotes(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(default=0, validators=[validate_vote])

    def __str__(self):
        return str(self.value)

    def save(self, *args, **kwargs):
        self.full_clean()
        # Call the "real" save() method in the base class 'models.Model'
        super(QuestionVotes, self).save(*args, **kwargs)


class AnswerVotes(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(default=0, validators=[validate_vote])

    def __str__(self):
        return str(self.value)

    def save(self, *args, **kwargs):
        self.full_clean()
        # Call the "real" save() method in the base class 'models.Model'
        super(AnswerVotes, self).save(*args, **kwargs)
