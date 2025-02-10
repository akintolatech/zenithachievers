from django.contrib import admin
from .models import WhatsappScreenshot, WhatsappWithdrawal
# Register your models here.
@admin.register(WhatsappScreenshot)
class WhatsappScreenshotAdmin(admin.ModelAdmin):
    list_display = ["user", "number_of_views", "approved", "screenshot_reference_code"]

@admin.register(WhatsappWithdrawal)
class WhatsappWithdrawalAdmin(admin.ModelAdmin):
    list_display = ["user", "amount",  "approved", "whatsapp_withdrawal_reference_code"]