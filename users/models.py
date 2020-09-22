from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Giftcards(models.Model):    
    user = models.CharField(max_length=250, blank=False, null=False)
    product_id = models.IntegerField(null=False, blank=False)
    product_name = models.CharField(max_length=50, blank=False, null=False)
    counter = models.IntegerField(null=False, blank=False, default=0)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)    
    full_name = models.CharField(max_length=50, blank=False, null=False)
    email = models.EmailField(max_length=254, blank=False, null=False)

    def __str__(self):
        return self.user
