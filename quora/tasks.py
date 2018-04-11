from __future__ import absolute_import
from celery import shared_task

from celery.decorators import task
from celery.utils.log import get_task_logger
from celery.contrib import rdb

from quora.emails import send_feedback_email

logger = get_task_logger(__name__)


@shared_task(name="send_feedback_email_task")
def send_feedback_email_task(email, message):
    logger.info("calling Send feedback email")
    return send_feedback_email(email, message)
