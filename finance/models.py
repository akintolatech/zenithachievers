from django.core.exceptions import ValidationError
from django.db import models
import uuid
from django.conf import settings
from decimal import Decimal

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
        related_name="withdrawals"
    )
    reference_code = models.CharField(max_length=12, unique=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # New field for charge
    created = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        from account.models import Profile

        if not self.reference_code:
            self.reference_code = str(uuid.uuid4())[:12]

        profile, _ = Profile.objects.get_or_create(user=self.user)

        # Calculate 5% withdrawal charge
        self.charge = self.amount * Decimal("0.05")
        total_deduction = Decimal(self.amount) + Decimal(self.charge)

        if self.pk:  # If updating an existing withdrawal
            original_withdrawal = Withdraw.objects.get(pk=self.pk)

            if not original_withdrawal.approved and self.approved:
                # Approving withdrawal: Deduct from balance and update amount_withdrawn
                if profile.earning_balance >= total_deduction:
                    profile.earning_balance -= total_deduction
                    profile.amount_withdrawn += self.amount
                else:
                    raise ValidationError("Insufficient earnings balance for withdrawal approval.")

            elif original_withdrawal.approved and not self.approved:
                # Unapproving withdrawal: Reverse deduction
                profile.earning_balance += total_deduction
                profile.amount_withdrawn -= self.amount

        else:
            # Deduct from earning_balance immediately upon creation
            if profile.earning_balance >= total_deduction:
                profile.earning_balance -= total_deduction
            else:
                raise ValidationError("Insufficient earnings balance for withdrawal.")

        profile.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.amount} (Charge: {self.charge}) - {'Approved' if self.approved else 'Pending'}"

