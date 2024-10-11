from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_resized import ResizedImageField
from phonenumber_field.modelfields import PhoneNumberField

USER_TYPE = (
    ('admin', 'Admin'),
    ('user', 'User'),
)


class User(AbstractUser):
    profile_image = ResizedImageField(size=[300, 300], quality=100, upload_to='profile_images', blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)

    email = models.EmailField(unique=True, max_length=200)
    user_type = models.CharField(max_length=10, choices=USER_TYPE, default='user')

    REQUIRED_FIELDS = ["username"]
    USERNAME_FIELD = "email"

    class Meta:
        ordering = ['-id']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.is_staff:
            self.user_type = 'admin'
        else:
            self.user_type = 'user'
        super(User, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.profile_image.delete(save=True)
        super(User, self).delete(*args, **kwargs)


@receiver(post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid="user_registered")
def on_user_registration(sender, instance, created, **kwargs):
    """
    :TOPIC if user creates at any point the statistics model will be initialized
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    pass
