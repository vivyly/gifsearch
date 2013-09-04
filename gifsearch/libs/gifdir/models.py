from django.db import models
from json_field import JSONField
from django_extensions.db.fields import UUIDField

class GifMeta(models.Model):
    data = JSONField()

class GifObject(models.Model):
    guid = UUIDField()
    reddit_id = models.CharField(null=True)
    created = models.DateTimeField('date published')
    updated = models.DateTimeField('date updated')
    src = models.URLField()
    meta = models.ForeignKey(GifMeta)
