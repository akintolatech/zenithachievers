from django.contrib import admin
from .models import (Deposit)

# Register your models here.
# admin.site.register(StkPushRequest)
@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ["user", "amount", "phone_number", "paid", "reference_code"]
