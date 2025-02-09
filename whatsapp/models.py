from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
import uuid
from decimal import Decimal

class WhatsappScreenshot(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="whatsapp_screenshots"  # Allows user.whatsapp_screenshots.all() to access screenshots
    )

    screenshot_reference_code = models.CharField(max_length=12, unique=True, blank=True)
    phone_number = models.CharField(max_length=15)
    number_of_views = models.PositiveIntegerField()
    screenshot = models.ImageField(upload_to='screenshots/')
    created = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs):
        from account.models import Profile

        if not self.screenshot_reference_code:
            self.screenshot_reference_code = str(uuid.uuid4())[:12]

        profile, created = Profile.objects.get_or_create(user=self.user)
        whatsapp_earnings_calculation = Decimal(self.number_of_views) * 100

        if self.pk:
            original_screenshot = WhatsappScreenshot.objects.get(pk=self.id)

            # Case 1: Approving a screenshot for the first time
            if not original_screenshot.approved and self.approved:
                profile.whatsapp_earnings += whatsapp_earnings_calculation

            # Case 2: Unapproving a previously approved screenshot
            elif original_screenshot.approved and not self.approved:
                profile.whatsapp_earnings -= whatsapp_earnings_calculation

            profile.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.phone_number}"


class WhatsappWithdrawal(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="whatsapp_withdrawals"
    )

    whatsapp_withdrawal_reference_code = models.CharField(max_length=12, unique=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount for withdrawal
    created = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs):
        from account.models import Profile

        if not self.whatsapp_withdrawal_reference_code:
            self.whatsapp_withdrawal_reference_code = str(uuid.uuid4())[:12]

        profile, _ = Profile.objects.get_or_create(user=self.user)

        if self.pk:  # If updating an existing withdrawal
            original_withdrawal = WhatsappWithdrawal.objects.get(pk=self.pk)

            if not original_withdrawal.approved and self.approved:
                # Approving withdrawal (already deducted, so just update total_withdrawals)
                profile.total_whatsapp_withdrawal += self.amount

            elif original_withdrawal.approved and not self.approved:
                # Unapproving withdrawal: Reverse deduction
                profile.whatsapp_earnings += self.amount
                profile.total_whatsapp_withdrawal -= self.amount

        else:
            # Deduct earnings immediately on creation
            if profile.whatsapp_earnings >= self.amount:
                profile.whatsapp_earnings -= self.amount
            else:
                raise ValidationError("Insufficient WhatsApp earnings for withdrawal.")

        profile.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {'Approved' if self.approved else 'Pending'}"