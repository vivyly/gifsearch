from django.db import models
from json_field import JSONField
from gifsearch.scraper.models import BaseObject, GifObject

class GifMetaGame(BaseObject):
    gif = models.ForeignKey(GifObject)
    data = JSONField()
