from django import template
from django.contrib.auth.models import User
from ask.models import *
from django.core.cache import cache

register = template.Library()


@register.simple_tag()
def is_disabled_que(q_id, u_id, v):
    v = int(v)
    if not u_id:
        return 'disabled_link'
    try:
        value = LikeToQuestion.objects.filter(question=Question.objects.get(id=q_id)).filter(owner=Profile.objects.get(user_id=u_id))[0].value
    except :
        return ''
    if value * v == 1:
        return 'disabled_link'
    return ''

@register.simple_tag()
def is_disabled_ans(a_id, u_id, v):
    v = int(v)
    if not u_id:
        return 'disabled_link'
    try:
        value = LikeToAnswer.objects.filter(answer=Answer.objects.get(id=a_id)).filter(owner=Profile.objects.get(user_id=u_id))[0].value
    except :
        return ''
    if value * v == 1:
        return 'disabled_link'
    return ''
