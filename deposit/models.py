from django.db import models
from django.conf import settings
import uuid

class Deposit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reference_code = models.CharField(max_length=12, unique=True, blank=True)
    amount = models.IntegerField(default=0)
    phone_number = models.CharField(max_length=11)
    created = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

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
                profile.deposit_balance += self.amount
                #Todo: update the referral referral_earnings as referral cashback 75% of user
                profile.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f'Deposit by {self.user.username}'
