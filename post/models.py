from django.db import models
from django.contrib.auth.models import User

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class Category(models.Model):
    name = models.CharField(unique=True, max_length=20)
    description = models.CharField(max_length=250)
    is_active = models.BooleanField(default=False)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Post(models.Model):

    STATUS_DRAFT = 0
    STATUS_PUBLISHED = 100
    STATUS_REJECTED = 20
    STATUS_TRASHED = 25
    STATUS_AUTHORIZED = 80

    STATUSES = (
        (STATUS_DRAFT, 'Draft'),
        (STATUS_PUBLISHED, 'Published'),
        (STATUS_REJECTED, 'Rejected'),
        (STATUS_TRASHED, 'Trashed'),
        (STATUS_AUTHORIZED, 'Authorized')
    )

    status = models.SmallIntegerField(choices=STATUSES, default=STATUS_DRAFT)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(unique=True, max_length=255)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=Post)
def send_post(sender, instance=None, created=False, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'post_ws', {
                'type': 'new_post',
                'message': instance.pk,
            }
        )
