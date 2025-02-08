from django.db import models
from django.conf import settings


class Profile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    photo = models.ImageField(
        upload_to='photos',
        blank=True,
        null=True
    )

    phone_number = models.CharField(max_length=11, null=True, blank=True)

    whatsapp_earnings = models.IntegerField(default=4)
    total_whatsapp_withdrawal = models.IntegerField(default=5)
    gold_plan_active = models.BooleanField(default=False)
    total_sent_transfers = models.IntegerField(default=2)
    deposit_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    earning_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    app_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    amount_withdrawn = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    order_details = models.TextField(blank=True, null=True)

    # invited_by = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     related_name='invited_users',
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True
    # )
    unique_referral = models.CharField(max_length=20 , null=True, blank=True, default="zenithachievers")

    def __str__(self):
        return f'Profile of {self.user.username}'
