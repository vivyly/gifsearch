from django.db import models
from json_field import JSONField
from django_extensions.db.fields import UUIDField

class BaseObject(models.Model):
    """
    An abstract model that provides the guid, created, modified attrs
    """
    guid = UUIDField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class GifMeta(BaseObject):
    data = JSONField()

class GifObject(BaseObject):
    title = models.CharField(blank=True, max_length=255)
    src_id = models.CharField(blank=True, max_length=255)
    src = models.URLField()
    meta = models.ForeignKey(GifMeta)
