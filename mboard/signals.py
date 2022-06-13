from django.db.models.signals import post_delete
from mboard.models import Post, Thread


def delete_media(instance, **kwargs):  # Signal receivers must accept keyword arguments (**kwargs).
    if instance.image:
        instance.image.delete(save=False)
        instance.thumbnail.delete(save=False)


post_delete.connect(delete_media, Post)
post_delete.connect(delete_media, Thread)
