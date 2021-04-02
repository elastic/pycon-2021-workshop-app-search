from app import app_search, settings

from django.db import models
from django.db.models import ObjectDoesNotExist
from django.db.models.signals import m2m_changed, post_delete, post_init, post_save
from django.dispatch import receiver


class State(models.Model):
    name = models.CharField(primary_key=True, max_length=64)


class Park(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    title = models.TextField()
    description = models.TextField()
    url = models.TextField()
    latitude = models.DecimalField(decimal_places=4, max_digits=8)
    longitude = models.DecimalField(decimal_places=4, max_digits=8)
    area = models.FloatField()
    established = models.DateTimeField()
    world_heritage_site = models.BooleanField()
    visitors = models.IntegerField()
    states = models.ManyToManyField(State)

    def to_app_search(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "location": f"{self.latitude}, {self.longitude}",
            "area": self.area,
            "established": self.established,
            "world_heritage_site": str(self.world_heritage_site).lower(),
            "visitors": self.visitors,
            "states": [state.name for state in self.states.all()],
        }


@receiver(post_save, sender=Park)
@receiver(m2m_changed, sender=Park.states.through)
def signal_park_index_document(sender, **kwargs):
    instance = kwargs["instance"]
    # Filter out all 'm2m_changed' actions that aren't post_*
    if "action" in kwargs and not kwargs["action"].startswith("post_"):
        return
    app_search.client.index_documents(
        engine_name=settings.APP_SEARCH_ENGINE_NAME,
        documents=[instance.to_app_search()],
    )


@receiver(post_delete, sender=Park)
def signal_park_delete_document(sender, **kwargs):
    instance = kwargs["instance"]
    app_search.client.delete_documents(
        engine_name=settings.APP_SEARCH_ENGINE_NAME,
        document_ids=[instance.id],
        ignore_status=404,
    )
