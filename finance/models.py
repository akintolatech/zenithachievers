from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import models
import uuid
from django.conf import settings
from decimal import Decimal
from django.contrib.auth import get_user_model


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

        # Send email notifications
        self.send_email_notifications()

    def send_email_notifications(self):
        User = get_user_model()  # Get the actual User model
        subject = "Transaction Notification"
        sender_email = self.sender.email  # Ensure sender has an email

        # Send email to sender
        if sender_email:
            message_sender = (
                f"Dear {self.sender.username},\n\n"
                f"You have successfully transferred Ksh{self.amount} to {self.receiver}.\n"
                f"Reference Code: {self.reference_code}\n\n"
                f"Thank you for using our service."
            )
            send_mail(subject, message_sender, settings.DEFAULT_FROM_EMAIL, [sender_email])

        # Lookup receiver's email if the username exists in the User model
        try:
            receiver_user = User.objects.get(username=self.receiver)
            receiver_email = receiver_user.email
            if receiver_email:
                message_receiver = (
                    f"Dear {receiver_user.username},\n\n"
                    f"You have received Ksh{self.amount} from {self.sender.username}.\n"
                    f"Reference Code: {self.reference_code}\n\n"
                    f"Thank you for using our service."
                )
                send_mail(subject, message_receiver, settings.DEFAULT_FROM_EMAIL, [receiver_email])
        except User.DoesNotExist:
            pass  # If the receiver is not a registered user, no email is sent


# class Transfer(models.Model):
#     sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_transfers', on_delete=models.CASCADE)
#     receiver = models.CharField(max_length=255)  # Store the receiver's username as text
#     reference_code = models.CharField(max_length=12, unique=True, blank=True)
#     amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     created = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         ordering = ["-created"]
#
#     def save(self, *args, **kwargs):
#
#         if not self.reference_code:
#             self.reference_code = str(uuid.uuid4())[:12]
#
#         super().save(*args, **kwargs)
#
#     def __str__(self):
#         return f"Transfer from {self.sender} to {self.receiver} - {self.amount}"



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
        send_email = False

        if self.pk:  # If updating an existing withdrawal
            original_withdrawal = Withdraw.objects.get(pk=self.pk)

            if not original_withdrawal.approved and self.approved:
                # Approving withdrawal: Deduct from balance and update amount_withdrawn
                if profile.earning_balance >= total_deduction:
                    profile.earning_balance -= total_deduction
                    profile.amount_withdrawn += self.amount
                    send_email = True
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
        # Send email only if the withdrawal was just approved
        if send_email:
            self.send_email_notifications()

    def send_email_notifications(self):
        User = get_user_model()  # Get the actual User model
        subject = "Withdrawal Notification"

        try:
            receiver_user = User.objects.get(username=self.user)
            receiver_email = receiver_user.email
            if receiver_email:
                message_receiver = (
                    f"Dear {receiver_user.username},\n\n"
                    f"Your Withdrawal of Ksh{self.amount} from Zenith Achievers with."
                    f"Reference Code: {self.reference_code}\n\n has been successfully approved\n"
                    f"Remaining balance: {receiver_user.profile.earning_balance}\n"
                    f"You will receive an alert on your registered Mpesa number, Thank you for using our service."
                )
                send_mail(subject, message_receiver, settings.DEFAULT_FROM_EMAIL, [receiver_email])
        except User.DoesNotExist:
            pass  # If the receiver is not a registered user, no email is sent


    def __str__(self):
        return f"{self.user.username} - {self.amount} (Charge: {self.charge}) - {'Approved' if self.approved else 'Pending'}"

