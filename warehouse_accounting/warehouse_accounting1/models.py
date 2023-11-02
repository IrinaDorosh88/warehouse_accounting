from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
    title = models.CharField(max_length=25)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Categories"


class Item(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, models.CASCADE)
    price = models.FloatField()
    description = models.TextField()
    quantity_on_stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_seller = models.BooleanField(default=False)
  

    def __str__(self):
        return self.user.username  

# автоматичне створення профілю користувача при створенні користувача 

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()




    



