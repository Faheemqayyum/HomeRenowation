from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Sum, Count, Avg

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
    about = models.CharField(max_length = 10000, null = True, blank = True)
    

    
    @property
    def get_profile_pic(self):
        
        if self.profile_pic:
            print(self.profile_pic.url)
            return self.profile_pic.url
        else:
            return ""
    
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
    
    
class WorkerProfileModel(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name="worker_profile")
    cnic_front = models.ImageField(upload_to="images/", null = True)
    cnic_back = models.ImageField(upload_to="images/", null = True)
    experience = models.CharField(max_length = 200, null = True, blank = True)
    profession = models.CharField(max_length = 200, null = True, blank = True)
    about = models.CharField(max_length = 200, null = True, blank = True)
    
    count_projects = models.IntegerField(default = 0)
    rating = models.FloatField(default=5)

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
    
    @property
    def get_average_rating(self):
        average_rating = Feedback.objects.filter(user__id = self.user.id).aggregate(avg_rating=Avg('rating'))
        return average_rating['avg_rating'] if average_rating['avg_rating'] else 0
    
    
    @property
    def get_commulative_rating(self):
        
        feedbacks = Feedback.objects.filter(user__id = self.user.id).aggregate(avg_rating = Avg('rating'))
        
        return feedbacks['avg_rating']
        
    
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
    
    
    
class NewQuote(models.Model):
    client_name = models.CharField(max_length=1000, null = False)
    email = models.CharField(max_length=1000, null = False)
    description = models.CharField(max_length=1000, null = False)
    project_name = models.CharField(max_length=1000, null = False)
    location = models.CharField(max_length=1000, null = False)
    budget = models.CharField(max_length=1000, null = False)
    category = models.CharField(max_length=1000, null = False)
    
    order_placed = models.BooleanField(default = False)
    quotes = models.IntegerField(default= 0)
    date_placed = models.DateField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.project_name}"
    


class ChatRoom_Model(models.Model):
    room_name = models.CharField(max_length=100, default='', null=False,unique=True)

    user1 =models.ForeignKey(User, on_delete=models.CASCADE, null = False, related_name='user1') # user 1 client
    user2 =models.ForeignKey(User, on_delete=models.CASCADE, null = False, related_name='user2') # user 2 worker

    last_updated = models.DateTimeField(null = True)
    unseen_messages_user1 = models.IntegerField(default = 0)
    unseen_messages_user2 = models.IntegerField(default = 0)
    
    def display_name(self):
        disp_name = self.room_name
        if self.room_name.startswith("Private_"):
            disp_name = self.room_name.replace("Private_","")
            
        return disp_name.replace("_"," ")

    @property
    def getWorker(self):
        return f"{self.user2.first_name} {self.user2.last_name} "
    
    @property
    def getClient(self):
        return f"{self.user1.first_name} {self.user1.last_name} "
    
    @property
    def getWorkerUnseen(self):
        return self.unseen_messages_user2
    
    @property
    def getClientUnseen(self):
        return self.unseen_messages_user1

    def __str__(self):
        return self.room_name
    




    
class User_Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom_Model, on_delete=models.CASCADE, null = True, related_name='chatroom')
    time_sent = models.DateTimeField(auto_now_add=True)
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE, null = False)
    message_text = models.CharField(max_length=300,default='-', null=True)




    def __str__(self):
        return self.message_text[:10]




class UserRoom(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    chat_room = models.ForeignKey(ChatRoom_Model, on_delete=models.CASCADE, null=True)
    last_updated = models.DateTimeField(null = True)
    unseen_messages = models.IntegerField(default = 0)
    
    def __str__(self):
        return f"{self.user.name} {self.chat_room.display_name()}"



        
        
class Bid(models.Model):
    quote = models.ForeignKey(NewQuote, on_delete=models.CASCADE, null = False, related_name = "bids")
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "bids", null = True)
    
    bid_amount = models.CharField(max_length=100, null = False)
    bid_estimated_time = models.CharField(max_length=100, null = False)
    bid_description = models.CharField(max_length=100, null = False)
    
    status = models.CharField(default = "Sent", max_length=1000)
    
    accepted = models.BooleanField(default = False)
    declined = models.BooleanField(default = False)

    def __str__(self):
        return f"{self.quote.client_name}"

    
    
class Order(models.Model):
    bid = models.ForeignKey(Bid, related_name="order", null = False, on_delete=models.CASCADE)
    client = models.ForeignKey(User, related_name="order", null = True, on_delete=models.CASCADE)
    
    paid = models.BooleanField(default=False)
    payment_verified = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    TID = models.CharField(max_length=100, null = True, blank = True)
    receipt = models.ImageField(upload_to='images/', null = True, blank = True)
    completed = models.BooleanField(default=False)
    rating = models.FloatField(null = True, blank = True)
    feedback = models.CharField(max_length=1000, null = True, blank = True)
    
    payee_name = models.CharField(max_length=1000, null = True, blank = True)
    
    @property
    def get_receipt(self):
        if self.receipt:
            return self.receipt.url
        else:
            return ""
        
        
        
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null =True, blank = True, related_name='feebacks')
    feedback = models.CharField(max_length=1000, null = False, blank = False)
    rating = models.FloatField(default = 0.0)
    client_name = models.CharField(null=True, max_length=150)
    

    def to_json(self):
        return {
            "client": self.client_name,
            'feedback': self.feedback,
            'rating': self.rating
        }
    

class Prices(models.Model):
    category = models.CharField(max_length=1000)
    hour_price = models.IntegerField(default= 500)
    daily_price = models.IntegerField(default=1200)
    
    def __str__(self) -> str:
        return f"{self.category} | {self.daily_price}"
    
    