from django.db import models
from django.conf import settings
from datetime import timedelta


class LoanRequest(models.Model):
    DURATION_CHOICES = [
        ('14_days', '14 days'),
        ('1_month', '1 month'),
        ('3_months', '3 months'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="loan_requests"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    duration = models.CharField(
        max_length=10,
        choices=DURATION_CHOICES,
    )
    created = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def get_duration_timedelta(self):
        if self.duration == '14_days':
            return timedelta(days=14)
        elif self.duration == '1_month':
            return timedelta(days=30)  # Approximate duration for 1 month
        elif self.duration == '3_months':
            return timedelta(days=90)  # Approximate duration for 3 months
        return timedelta(days=0)  # Default to zero if no match
