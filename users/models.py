from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Giftcards(models.Model):    
    user = models.CharField(max_length=250, blank=False, null=False)
    product_id = models.IntegerField(null=False, blank=False)
    product_name = models.CharField(max_length=50, blank=False, null=False)
    counter = models.IntegerField(null=False, blank=False, default=0)

class UserProfile(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    country = models.CharField(max_length=50, null=False, blank=False)
    street_address = models.CharField(max_length=50, null=False, blank=False)
    city = models.CharField(max_length=50, null=False, blank=False)
    postcode = models.CharField(max_length=50, null=False, blank=False)
    phone_number = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.user
