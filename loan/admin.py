from django.contrib import admin
from .models import LoanRequest
# Register your models here.
@admin.register(LoanRequest)
class LoanRequestAdmin(admin.ModelAdmin):
    list_display = ["user", "amount",  "approved", "created"]