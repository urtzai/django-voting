# coding: utf-8

from __future__ import unicode_literals

from datetime import datetime

from django.utils.encoding import python_2_unicode_compatible
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

try:
    from django.utils.timezone import now
except ImportError:
    now = datetime.now

from voting.managers import VoteManager
from voting.utils.user_model import get_user_model_name

User = get_user_model_name()

SCORES = (
    (+1, '+1'),
    (-1, '-1'),
)

@python_2_unicode_compatible
class Vote(models.Model):
    """
    A vote on an object by a User.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    object = GenericForeignKey('content_type', 'object_id')
    vote = models.SmallIntegerField(choices=SCORES)
    time_stamp = models.DateTimeField(editable=False, default=now)

    objects = VoteManager()

    class Meta:
        db_table = 'votes'
        # One vote per user per object
        unique_together = (('user', 'content_type', 'object_id'),)

    def __str__(self):
        return '%s: %s on %s' % (self.user, self.vote, self.object)

    def is_upvote(self):
        return self.vote == 1

    def is_downvote(self):
        return self.vote == -1
