from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    is_worker = models.BooleanField(default = False)
    is_approved = models.BooleanField(default = False)
    is_declined = models.BooleanField(default = False)
    email = models.EmailField(max_length = 1000, null = False, unique=True)
    profile_pic = models.ImageField(upload_to="images/")
    is_profile_set = models.BooleanField(default = False)
    cnic = models.CharField(max_length = 20, null = True, blank = True)
    phone = models.CharField(max_length = 20, null = True, blank = True)
    address = models.CharField(max_length = 1000, null = True, blank = True)
    
    @property
    def get_profile_pic(self):
        
        if self.profile_pic:
            print(self.profile_pic.url)
            return self.profile_pic.url
        else:
            return ""
    
class WorkerProfileModel(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name="worker_profile")
    cnic_front = models.ImageField(upload_to="images/", null = True)
    cnic_back = models.ImageField(upload_to="images/", null = True)
    experience = models.CharField(max_length = 200, null = True, blank = True)
    profession = models.CharField(max_length = 200, null = True, blank = True)
    about = models.CharField(max_length = 200, null = True, blank = True)
    
    @property
    def get_cnic_front(self):
        
        if self.cnic_front:
            return self.cnic_front.url
        else:
            return ""
    @property
    def get_cnic_back(self):
        
        if self.cnic_back:
            return self.cnic_back.url
        else:
            return ""
    
    
class WorkerSampleProject(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name="sample_projects")
    title = models.CharField(max_length = 1000, null = True, blank = True)
    budget = models.CharField(max_length = 1000, null = True, blank = True)
    description = models.CharField(max_length = 1000, null = True, blank = True)
    completed_days = models.CharField(max_length = 1000, null = True, blank = True)
    thumbnail = models.ImageField(upload_to = "images/", null =True)

    @property
    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            return ""
class SampleProjectImages(models.Model):
    image = models.ImageField(upload_to = "images/", null = False)
    project = models.ForeignKey(WorkerSampleProject, on_delete = models.CASCADE, related_name="project_images")
    


class Job(models.Model):
    title = models.CharField(max_length = 2000, null = False, blank = False)
    budget = models.CharField(max_length = 1000, null =False)
    description = models.CharField(max_length = 5000, null = False, blank = False)
    category = models.CharField(max_length = 2000, null = False, blank = False)
    due_date = models.CharField(max_length = 2000, null = False, blank = False)
    thumbnail = models.ImageField(upload_to = "images/", null = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_jobs")

    @property
    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        return ""

class JobImages(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="job_images")
    image = models.ImageField(null = True, upload_to="images/")
    
    @property
    def get_image(self):
        if self.image:
            return self.image.url
        return ""