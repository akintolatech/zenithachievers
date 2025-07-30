from django.db import models
from django.conf import settings
import uuid
from decimal import Decimal


class Deposit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reference_code = models.CharField(max_length=12, unique=True, blank=True)
    amount = models.IntegerField(default=0)
    phone_number = models.CharField(max_length=15)
    created = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    checkout_request_id = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs):
        from account.models import Profile  # Import inside to prevent circular imports

        if not self.reference_code:
            self.reference_code = str(uuid.uuid4())[:12]  # Generate unique 12-character code

        # Check if this deposit instance is being marked as paid for the first time
        if self.pk:
            original = Deposit.objects.get(pk=self.pk)
            if not original.paid and self.paid:
                # Deposit is now confirmed, update the user's deposit balance
                profile, created = Profile.objects.get_or_create(user=self.user)

                profile.deposit_balance += Decimal(self.amount)  # Ensure amount is Decimal
                profile.save()

                # Update referral earnings which is changed to app earnings (75% of deposit amount)
                if profile.invited_by:  # Check if the user has an inviter
                    inviter_profile, created = Profile.objects.get_or_create(user=profile.invited_by)
                    referral_bonus = Decimal(self.amount) * Decimal("0.75")  # Convert to Decimal
                    # This is where the change happens ->
                    # inviter_profile.referral_earnings += referral_bonus
                    inviter_profile.earning_balance += referral_bonus
                    inviter_profile.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f'Deposit by {self.user.username}'


# class UssdPushRequest(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     request_ref_id = models.CharField(max_length=100, unique=True)
#     result_code = models.CharField(max_length=10, null=True, blank=True)
#     result_desc = models.TextField(null=True, blank=True)
#     status = models.CharField(max_length=20, default="PENDING")
#     transaction_id = models.CharField(max_length=100, null=True, blank=True)
#     deposit = models.ForeignKey("Deposit", on_delete=models.SET_NULL, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#
# class StkPushRequest(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=12, decimal_places=2)
#     phone_number = models.CharField(max_length=13)
#     merchant_request_id = models.CharField(max_length=64, blank=True)
#     checkout_request_id = models.CharField(max_length=64, blank=True)
#     response_code = models.CharField(max_length=10, blank=True)
#     response_description = models.CharField(max_length=255, blank=True)
#     customer_message = models.CharField(max_length=255, blank=True)
#     result_code = models.CharField(max_length=10, blank=True)
#     result_desc = models.CharField(max_length=255, blank=True)
#     mpesa_receipt = models.CharField(max_length=32, blank=True)
#     transaction_date = models.CharField(max_length=14, blank=True)
#     status = models.CharField(max_length=20, default="PENDING")
#     created = models.DateTimeField(auto_now_add=True)
#     deposit = models.ForeignKey(Deposit, null=True, blank=True, on_delete=models.SET_NULL)

