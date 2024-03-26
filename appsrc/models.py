from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    is_worker = models.BooleanField(default = False)
    is_approved = models.BooleanField(default = False)
    email = models.EmailField(max_length = 1000, null = False, unique=True)
    profile_pic = models.ImageField(upload_to="images/")
    is_profile_set = models.BooleanField(default = False)
    cnic = models.CharField(max_length = 20, null = True, blank = True)
    
    
    
    
class WorkerProfile(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name="worker_profile")
    cnic_front = models.ImageField(upload_to="images/", null = True)
    cnic_back = models.ImageField(upload_to="images/", null = True)
    experience = models.CharField(max_length = 200, null = True, blank = True)
    profession = models.CharField(max_length = 200, null = True, blank = True)
    about = models.CharField(max_length = 200, null = True, blank = True)
    
    
    
    
    