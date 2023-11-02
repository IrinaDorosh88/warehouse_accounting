from django.db import models
from django.contrib.auth.models import User as UserModel


class User(models.Model):
    USERS = 'users'
    WAREHOUSEMAN = 'warehouseman'
    USER_TYPES = [
        (USERS, USERS),
        (WAREHOUSEMAN, WAREHOUSEMAN)
    ]
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    user_type = models.CharField(choices=USER_TYPES, max_length=20)
    name = models.CharField(max_length=50)
    is_seller = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
  

    def __str__(self):
        return self.user.username



