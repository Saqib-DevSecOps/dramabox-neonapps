from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.


class Wallet(models.Model):
    user = models.OneToOneField(
        'users.User',
        on_delete=models.CASCADE,
        related_name='wallet'
    )
    total_coins = models.PositiveIntegerField(default=0)
    used_coins = models.PositiveIntegerField(default=0)
    available_coins = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Wallet')
        verbose_name_plural = _('Wallets')

    def __str__(self):
        return f"{self.user.username}'s Wallet"
