from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    is_worker = models.BooleanField(default = False)
    is_approved = models.BooleanField(default = False)
    email = models.EmailField(max_length = 1000, null = False, unique=True)
    profile_pic = models.ImageField(upload_to="images/")
    
class WorkerProfile(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name="worker_profile")
    nic = models.ImageField(upload_to="images/", null = True)