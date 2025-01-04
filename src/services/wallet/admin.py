from django.contrib import admin

from src.services.wallet.models import Wallet


# Register your models here.

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_coins', 'used_coins', 'available_coins', 'updated_at']
