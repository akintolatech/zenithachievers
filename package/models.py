from django.db import models
from django.contrib.auth.models import User

class Package(models.Model):
    name = models.CharField(max_length=50, unique=True)  # Now dynamic
    price = models.DecimalField(max_digits=10, decimal_places=2)
    lifetime = models.CharField(max_length=50, default="Lifetime")  # Default to lifetime access
    earning_methods = models.TextField(help_text="Comma-separated values")  # Store as a list of methods
    ksh_per_view = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)

    def get_earning_methods(self):
        """Returns earning methods as a list"""
        return self.earning_methods.split(", ")

    def __str__(self):
        return self.name

class UserPackage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.package.name}"
