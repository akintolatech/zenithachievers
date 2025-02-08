from django.db import models
from django.conf import settings
import uuid

# Create your models here.

class Deposit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reference_code = models.CharField(max_length=12, unique=True, blank=True)
    amount = models.IntegerField(default=0)
    phone_number = models.CharField(max_length=11)
    created = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.reference_code:
            self.reference_code = str(uuid.uuid4())[:12]  # Generate unique 12-character code
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Deposit by {self.user.username}'
