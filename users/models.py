from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    

    ACCT_TYPES = [
        ('commissioner', 'Commissioner'),
        ('commissionee', 'Commissionee'),
    ]
    account_type = models.CharField(max_length=21, choices=ACCT_TYPES)

    def __str__(self):
        return f"{self.user.username} - {self.account_type}"