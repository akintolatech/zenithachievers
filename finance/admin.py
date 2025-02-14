from django.contrib import admin
from .models import Transfer

# Register your models here.
@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ["sender", "receiver", "amount", "created"]
