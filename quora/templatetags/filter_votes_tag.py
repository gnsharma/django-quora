from django import template
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()


@register.assignment_tag
def filter_votes(model_obj, user_obj, *args, **kwargs):
    try:
        up_count = model_obj.filter(vote=1).count()
        down_count = model_obj.filter(vote=-1).count()
        total = up_count - down_count
        vote_obj = model_obj.get(user=user_obj)
        return {'vote_obj': vote_obj, 'total': total, 'up_count': up_count, 'down_count': down_count}
    except ObjectDoesNotExist:
        return {'vote_obj': None, 'total': total, 'up_count': up_count, 'down_count': down_count}
