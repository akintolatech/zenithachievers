from decimal import Decimal

from django.db import models
from django.conf import settings
from django.http import HttpRequest
from django.contrib.sites.shortcuts import get_current_site


# from django.contrib.auth.models import AbstractUser
# from django.db import models

# class CustomUser(AbstractUser):
#     email = models.EmailField(unique=True)  # Enforce unique emails
#

class ActiveProfileManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(account_status=Profile.AccountStatus.ACTIVE)


class Profile(models.Model):

    class AccountStatus(models.TextChoices):
        DORMANT = "DM", "Dormant"
        ACTIVE = "AC", "Active"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    account_status = models.CharField(
        max_length=2,
        choices=AccountStatus.choices,
        default=AccountStatus.DORMANT
    )

    photo = models.ImageField(
        upload_to='photos',
        blank=True,
        null=True
    )

    phone_number = models.CharField(max_length=11, null=True, blank=True)
    gold_plan_active = models.BooleanField(default=False)
    total_sent_transfers = models.IntegerField(default=0)
    whatsapp_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_whatsapp_withdrawal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    deposit_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    earning_balance = models.DecimalField(max_digits=100, decimal_places=2, default=Decimal("0.00"))
    # earning_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    referral_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    amount_withdrawn = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='invited_users',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    referral_link = models.URLField(
        max_length=255,
        blank=True,
        null=True
    )  # Store the referral link

    objects = models.Manager()  # Default manager
    active_profiles = ActiveProfileManager()  # Custom manager for active profiles

    # def get_referral_link(self):
    #     # Get the first domain from ALLOWED_HOSTS (ensure it's a valid domain)
    #     if settings.ALLOWED_HOSTS:
    #         domain = settings.ALLOWED_HOSTS[0]
    #         return f"https://{domain}/account/register/?invitedby={self.user.username}"
    #     return None


    def get_referral_link(self):
        return f"http://127.0.0.1:8000/account/register/?invitedby={self.user.username}"

    # def get_referral_link(self, request: HttpRequest):
    #     site = get_current_site(request)  # Gets the domain dynamically
    #     return f"http://{site.domain}/account/register/?invitedby={self.user.username}"

    def user_referrals(self):
        return Profile.objects.filter(invited_by=self.user)

    def referrals_count(self):
        return Profile.objects.filter(invited_by=self.user).count()

    def active_referrals_count(self):
        """Returns the count of active referrals."""
        return Profile.objects.filter(invited_by=self.user, account_status=Profile.AccountStatus.ACTIVE).count()

    def dormant_referrals_count(self):
        """Returns the count of dormant referrals."""
        return Profile.objects.filter(invited_by=self.user, account_status=Profile.AccountStatus.DORMANT).count()

    def activate_account(self):
        """Activate the account when a package is purchased."""
        if self.account_status != Profile.AccountStatus.ACTIVE:
            self.account_status = Profile.AccountStatus.ACTIVE
            self.save()

    def __str__(self):
        return f'Profile of {self.user.username}'
