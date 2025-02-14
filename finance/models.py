from django.db import models, transaction
from django.conf import settings
import uuid
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist

class Transfer(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_transfers', on_delete=models.CASCADE)
    receiver = models.CharField(max_length=255)  # Store the receiver's username as text
    reference_code = models.CharField(max_length=12, unique=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def save(self, *args, **kwargs):

        if not self.reference_code:
            self.reference_code = str(uuid.uuid4())[:12]

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Transfer from {self.sender} to {self.receiver} - {self.amount}"

class Withdraw(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="withdrawals"  # Allows user.whatsapp_screenshots.all() to access screenshots
    )
    reference_code = models.CharField(max_length=12, unique=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)