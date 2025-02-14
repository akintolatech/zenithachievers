from django.contrib import admin
from .models import Transfer, Withdraw

# Register your models here.
@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ["sender", "receiver", "amount", "created"]


@admin.register(Withdraw)
class WithdrawAdmin(admin.ModelAdmin):
    list_display = ["user", "reference_code", "amount", "charge", "created", "approved"]
