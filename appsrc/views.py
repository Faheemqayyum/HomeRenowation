from django.shortcuts import render, redirect
from .models import *

from datetime import datetime, timedelta
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q
from django.http import JsonResponse

# Create your views here.
def Homepage(request):
  
  # GET BEST PROS
  best_workers = WorkerProfileModel.objects.filter(user__is_approved = True).order_by('-rating','-count_projects')[:4]
  return  render(request, 'Website/homepage.html',{'workers':best_workers})

def SearchPros(request):
  pros = User.objects.filter(is_approved = True, ).all()
  
  return  render(request, 'Website/Search_pros.html',{"pros":pros})


@login_required(login_url='login')
def messagePro(request):
  
  print(request.GET)
  is_pro = request.GET.get("is_pro")
  
  pro_id = request.GET.get("pro_id")
  client_id = request.user.id
  if is_pro:
    pro_id, client_id = client_id, pro_id
    
  room_name = f"{client_id}_{pro_id}"
  
  if ChatRoom_Model.objects.filter(Q(Q(user1__id = client_id) & Q(user2__id = pro_id)) | (Q(user1__id = client_id) & Q(user2__id = pro_id))).exists() == False:
    
    room_name = f"{client_id}_{pro_id}"
    try:
      ChatRoom_Model.objects.create(
        room_name = room_name,
        user1 = User.objects.get(id = client_id),
        user2 = User.objects.get(id = pro_id)
      )
      redirect_url = request.build_absolute_uri(
            reverse('chat', kwargs={'room_name': room_name})
            )
      return redirect(redirect_url)
    except Exception as e:
        print("<><><><><><><>",e)
        return redirect('searchpros')
  
  else:
    try:
      chatroom = ChatRoom_Model.objects.get(Q(Q(user1__id = client_id) & Q(user2__id = pro_id)) | (Q(user1__id = client_id) & Q(user2__id = pro_id)))
      chatroom = chatroom.room_name
      
      redirect_url = request.build_absolute_uri(
              reverse('chat', kwargs={'room_name': room_name})
              )
      return redirect(redirect_url)
    except Exception as e: 
      print(">>>>>>>", e)
      
    return redirect('searchpros')

def SearchProject(request):
  
  msg = request.session.get('msg')
  quotes = NewQuote.objects.filter(order_placed = False).order_by('-date_placed')
  
  request.session['msg'] = ""
  return  render(request, 'Website/Search_project.html',{'jobs':quotes, "msg":msg})

def QuoteProject(request):
  if not request.user.is_authenticated:
    login_url = request.build_absolute_uri(
            reverse('login')
            )+"?next=quoteproject"



    return redirect(login_url)
  
  
  uploaded = False
  if request.method == "POST":
    name = request.POST.get('Name')
    Email = request.POST.get('Email')
    project_desc = request.POST.get('project_desc')
    project_name = request.POST.get('project_name')
    project_location = request.POST.get('project_location')
    project_budget = request.POST.get('project_budget')
    
    category = request.POST.get('category')
    
    NewQuote.objects.create(
      client_name = name,
      email = Email,
      description = project_desc,
      project_name = project_name,
      location = project_location,
      budget = project_budget,
      category = category
    )
    uploaded = True
    
    
  prices = Prices.objects.values().all()
  prices = list(prices)
  print(prices)
  return  render(request, 'Website/Quotepage.html', {'uploaded':uploaded,'prices':prices})


def MeetTeam(request):

  return  render(request, 'Website/meetourteam.html')


def FAQS(request):
  return  render(request, 'Website/faqs.html')

def SendBid(request):
  if request.user.is_authenticated:
    print(request.POST)
    if request.user.is_worker:
      bid_amount = request.POST.get("bid_amount")
      bid_estimated_time = request.POST.get("bid_estimated_time")
      bid_description = request.POST.get("bid_description")
      quote_id = request.POST.get("quote_id")
      
      quote = NewQuote.objects.get(id = quote_id)
      Bid.objects.create(
        bid_amount = bid_amount,
        bid_estimated_time = bid_estimated_time,
        bid_description = bid_description,
        quote = quote,
        user = request.user
      )
      quote.quotes = quote.quotes+1
      quote.save()
      request.session['msg'] = "Quote is sent"
    else:
      request.session['msg'] = "You are not a worker you cannot bid"
  else:
    request.session['msg'] = "Please login to send bid."
  return redirect('searchproject')




def LoginPage(request):
  error = ""
  email = None
  if request.method == "POST":
    email = request.POST.get("email")
    password = request.POST.get("password")
    
    
    if User.objects.filter(username = email).exists():
      user = User.objects.get(username = email)
      user_data = authenticate(username= email, password = password)
      if user_data is not None:
        auth_login(request, user_data)  
        if user.is_superuser:
          if request.GET.get("next"):
            return redirect(request.GET.get("next"))
          return redirect("admindashboard")

        elif user.is_worker:
          if request.GET.get("next"):
            return redirect(request.GET.get("next"))
          return redirect("workerdashboard")

        else:
          if request.GET.get("next"):
            return redirect(request.GET.get("next"))
          return redirect("clientdashboard")
        
      else:
        error = "Invalid password"
    else:
        error = "Invalid Username or password"
      

  return  render(request, 'Website/Login.html', {'error':error, 'email':email})


def logout(request):
  auth_logout(request)
  
  return redirect('homepage')
  
def SignUpPage(request):
  form = request.POST
  error = {}
  if request.method == "POST":
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    email = request.POST.get("email")
    password = request.POST.get("password")
    confirm_password = request.POST.get("password2")
    account_type = request.POST.get('account_type')
    
    if len(password) < 8:
      error['password'] = "Password must be 8 or more characters long"
    elif password != confirm_password:
      error['password2'] = "Password do not match"
    elif User.objects.filter(email = email).exists():
      error["email"] = "Email already exists"
    
    else:
      user_instance = User.objects.create(
        email = email,
        username = email,
        first_name = first_name,
        last_name = last_name,
        is_worker = account_type == "worker"
        )
      user_instance.set_password(password)
      user_instance.save()
      
      if account_type == "worker":
        WorkerProfileModel.objects.create(user = user_instance)
      
      return redirect('login')
      
  return  render(request, 'Website/Signup.html', {"form":form, 'error':error})

def ResetPassword(request):
  return  render(request, 'Website/ResetPassword.html')
# Admin
@login_required(login_url='login')
def AdminDashboard(request):
  if not request.user.is_authenticated:
    return redirect('login')
  if request.user.is_superuser:
    
    workers = User.objects.filter(is_worker = True, is_approved = False, is_profile_set=True)
    clients = User.objects.filter(is_worker = False, is_approved = False, is_superuser = False)
    
    return  render(request, 'Admin/AdminDashboard.html',{"worker_requests":workers, "clients":clients})
  elif request.user.is_worker:
    return redirect("workerdashboard")
  else:
    return redirect("clientdashboard")
  
@login_required(login_url='login')
def acceptRejectUser(request):
  if request.method == "POST":
    
    id = request.POST.get('member_id')
    if User.objects.filter(id = id).exists():
      user = User.objects.get(id = id)
      status = request.POST.get("status")
      print(status)
      if status == "Accept":
        user.is_approved = True
      else:
        user.is_declined = True
      
      user.save()
      print(user)
      print(status, id)

  return redirect('admindashboard')

@login_required(login_url='login')
def RecentMembers(request):
  members = User.objects.filter(is_worker = False, is_superuser = False).order_by('-id')
  return  render(request, 'Admin/RecentMembers.html', {"members":members})


@login_required(login_url='login')
def RecentWorkers(request):
  members = User.objects.filter(is_worker = True).order_by('-id')
  return  render(request, 'Admin/RecentWorkers.html',{"workers":members})


@login_required(login_url='login')
def RecentWorkersDetail(request, id):
  
  if User.objects.filter(id = id, is_worker = True).exists():
    user = User.objects.get(id = id)
  else:
    if request.user.is_superuser:
      return redirect("admindashboard")
    else:
      return redirect("homepage")
    
  if request.method == "POST":
    if request.POST.get("action") == "accept":
      user.is_approved = True
    elif request.POST.get("action") == "decline":
      user.is_declined = True
    
    user.save()
     

  return  render(request, 'Admin/RecentWorkerDetail.html', {"worker":user})


@login_required(login_url='login')
def MemberDetail(request, id):
  if request.user.is_superuser:
    if User.objects.filter(id = id).exists():
      user = User.objects.get(id = id)
    else:
      return redirect("admindashboard")
  else:
    return redirect("homepage")
  
  return  render(request, 'Admin/RecentMemberDetail.html', {"user":user})
def NewProjects(request):
  return  render(request, 'Admin/NewProjects.html')
def PaymentApprove(request):
  
  
  if request.method == "POST":
    order_id = request.POST.get("order_id")
    action = request.POST.get("action")
    
    if action == "accept":
      order = Order.objects.get(id = order_id)
      order.payment_verified = True
      order.save()
  
  approvals = Order.objects.filter(paid = True, payment_verified=False)
  approved =  Order.objects.filter(paid = True, payment_verified=True).order_by('-id')
  
  return  render(request, 'Admin/PaymentApproval.html',{"approvals":approvals, 'approved':approved})
def ActiveProject(request):
  return  render(request, 'Admin/ActiveProjects.html')

# Worker
@login_required(login_url='login')
def WorkerDashboard(request):
  if not request.user.is_profile_set:
    return redirect("editworkerprofile")
  
  
  quotes = Bid.objects.filter(user = request.user)[:5]
  print(quotes)
  
  return  render(request, 'Worker/WorkerDashboard.html', {'quotes':quotes})


@login_required(login_url='login')
def WorkerSample(request):
  if request.method == "POST":
    id = request.POST.get("sample_id")
    if WorkerSampleProject.objects.filter(id = id).exists():
       WorkerSampleProject.objects.get(id = id).delete()
    print(id)

  
  samples = WorkerSampleProject.objects.filter(user = request.user)

  return  render(request, 'Worker/Workersamples.html', {'samples':samples})


@login_required(login_url='login')
def WorkerOrders(request): 
  on_going_orders = Order.objects.filter(bid__user = request.user, completed = False)
  completed_orders = Order.objects.filter(bid__user = request.user, completed = True)
  
  
  return render(request , 'Worker/WorkerOrders.html',{'orders':on_going_orders, 'completed':completed_orders})

@login_required(login_url='login')
def RecentQuotes(request): 
  
  quotes = Bid.objects.filter(user = request.user)
  print(quotes)
  return render(request , 'Worker/RecentQuotes.html', {'quotes':quotes})

def OrderDetail(request): 
  return render(request , 'Worker/OrderDetail.html')


@login_required(login_url='login')
def WorkerChat(request): 
  user_rooms = ChatRoom_Model.objects.filter(Q(user1__id = request.user.id) | Q(user2__id = request.user.id))
  
  return render(request , 'Worker/Chatpage.html', {'rooms':user_rooms})

@login_required(login_url='login')
def Chat(request, room_name):
  print(room_name)
  
  if ChatRoom_Model.objects.filter(Q(Q(user1__id = request.user.id) & Q(room_name = room_name)) | (Q(user2__id = request.user.id) & Q(room_name = room_name))).exists():
    chatroom = ChatRoom_Model.objects.get(Q(Q(user1__id = request.user.id) & Q(room_name = room_name)) | (Q(user2__id = request.user.id) & Q(room_name = room_name)))
    messages = User_Message.objects.filter(chat_room = chatroom)
    user_rooms = ChatRoom_Model.objects.filter(Q(user1__id = request.user.id) | Q(user2__id = request.user.id))
    
    print(">>>>>>><>>>>>>>>>>>>><<<<<<<<<<<")
    selected_user_name = chatroom.getClient if request.user.is_worker else chatroom.getWorker
    return render(request, 'Worker/Chatpage.html', {'messages':messages, 'selected_user':selected_user_name,'selected':room_name,'rooms':user_rooms})
  
  return redirect("workerchat")

@login_required(login_url='login')
def AddWorkerSample(request):
  if request.method == "POST":
    title = request.POST.get('project-title')
    budget = request.POST.get('project-budget')
    desc = request.POST.get('project-desc')
    days = request.POST.get('project-days')
    thumbnail = request.FILES.get('thumbnail')
    images = request.FILES.getlist('sample_images')

    work_sample = WorkerSampleProject.objects.create(
                      budget = budget,
                      title = title,
                      description = desc,
                      completed_days = days,
                      thumbnail = thumbnail,
                      user = User.objects.get(id = request.user.id)
                    )
    work_sample.save()
    for img in images:
      SampleProjectImages.objects.create(image = img, project = work_sample)

  return  render(request, 'Worker/AddWorkSamples.html')


def WorkerProfile(request):
  
  user = User.objects.get(id = request.user.id)
  return  render(request, 'Worker/Profile.html', {'user':user})



@login_required(login_url='login')
def EditWorkerProfile(request):
  if request.method == "POST":
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    phone = request.POST.get("phone")
    address = request.POST.get("address")
    profession = request.POST.get("profession")
    experience = request.POST.get("experience")
    cnic = request.POST.get("cnic")
    about = request.POST.get("about")
    
    profile_pic = request.FILES.get("profile_pic")
    cnic_front = request.FILES.get("cnic_front")
    cnic_back = request.FILES.get("cnic_back")
    
    
    print(request.FILES)  
    
    user = User.objects.get(id = request.user.id)
    worker_instance = WorkerProfileModel.objects.get(user = user)
    
    user.first_name = first_name
    user.last_name = last_name
    user.phone = phone
    user.address = address
    user.cnic = cnic
    
    worker_instance.experience = experience
    worker_instance.profession = profession
    worker_instance.about = about
    
    if profile_pic:
      user.profile_pic = profile_pic
      
    if cnic_front:
      worker_instance.cnic_front = cnic_front
    if cnic_back:
      worker_instance.cnic_back = cnic_back
    
    user.is_profile_set = True
    
    user.save()
    worker_instance.save()
    
    
  
  user = User.objects.get(id = request.user.id)
    
  return  render(request, 'Worker/EditProfile.html', {"user":user})

# Client
@login_required(login_url='login')
def ClientDashboard(request):
  
  # recent bids
  bids = Bid.objects.filter(quote__email = request.user.email, status__iexact = 'Sent').order_by('-id')[:10]
  
  return  render(request, 'Client/Dashboard.html',{'bids':bids})


@login_required(login_url='login')
def ShowJobs(request):

  if request.method == "POST":
    job_id = request.POST.get('id')
    if Job.objects.filter(id = job_id).exists():
      Job.objects.get(id = job_id).delete()
      
  return  render(request, 'Client/PostJob.html')


@login_required(login_url='login')
def AddJob(request):
  if request.method == "POST":
    user = User.objects.get(id = request.user.id)
    title = request.POST.get("title")
    budget = request.POST.get("budget")
    description = request.POST.get("description")
    category = request.POST.get("category")
    due_date = request.POST.get("due_date")
    thumbnail = request.FILES.get("thumbnail")

    job = Job.objects.create(
      user = user,
      title = title,
      budget = budget,
      description = description,
      category = category,
      due_date = due_date,
      thumbnail  = thumbnail,
    )
    job.save()
    for image in request.FILES.getlist('sample_images'):
      JobImages.objects.create(job = job, image = image)
      
  return  render(request, 'Client/AddJob.html')


def ClientProfile(request):
  user = User.objects.get(id = request.user.id)
  return  render(request, 'Client/Profile.html', {"user":user})

@login_required(login_url='login')
def EditClientProfile(request):
  if request.method == "POST":
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    address = request.POST.get('address')
    cnic = request.POST.get('cnic')
    phone = request.POST.get('phone')
    profile_pic = request.FILES.get('profile_pic')
    

    
    user = User.objects.get(id = request.user.id)
    
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.address = address
    user.cnic = cnic
    user.phone = phone
    if profile_pic:
      user.profile_pic = profile_pic
    
    
    user.save()
    return redirect("clientprofile")

  user = User.objects.get(id = request.user.id)

  return  render(request, 'Client/EditProfile.html', {"user":user})

def ClientChat(request):
  user_rooms = ChatRoom_Model.objects.filter(Q(user1__id = request.user.id) | Q(user2__id = request.user.id))

  return render(request, 'Client/Chatpage.html')

def ClientQuotes(request):
  quotes = NewQuote.objects.filter(email = request.user.email).order_by('-id')
  
  return render(request, 'Client/ClientQuotes.html', {'quotes':quotes})



@login_required(login_url='login')
def ClientOrders(request): 
  
  
  if request.method == "POST":
    action = request.POST.get("action")
    if action.strip().lower() == "complete":
      order_id = request.POST.get("order_id")
      if Order.objects.filter(id = order_id, client__id = request.user.id).exists():
        order = Order.objects.get(id = order_id)
        order.completed = True
        order.save()
    elif action == "feedback":
      order_id = request.POST.get("order_id")
      feedback = request.POST.get("feedback")
      rating = request.POST.get("rating")
      if Order.objects.filter(id = order_id, client__id = request.user.id).exists():
        try:
              order = Order.objects.get(id = order_id)
              order.feedback = feedback
              order.rating = float(rating)
              order.save()
              
              Feedback.objects.create(
                user = order.bid.user,
                feedback = feedback,
                rating = rating,
                client_name = f"{request.user.first_name} {request.user.last_name}"
        )
          
              worker = User.objects.get(id = order.bid.user.id)
              worker_profile = WorkerProfileModel.objects.get(user = worker)
              rating_total = worker_profile.rating * worker_profile.count_projects
              rating_total += float(rating)
              worker_profile.count_projects += 1
              rating_total = round(rating_total / worker_profile.count_projects, 1)
              
              worker_profile.save()
              worker.save()
  

        except:
               pass

  on_going_orders = Order.objects.filter(client = request.user, completed = False)
  completed_orders = Order.objects.filter(client = request.user, completed = True)
  
  
  return render(request , 'Client/ClientOrders.html',{'orders':on_going_orders, 'completed':completed_orders})



@login_required(login_url='login')
def WorkerQuotes(request, id):
  
  if NewQuote.objects.filter(id = id, email__iexact = request.user.email).exists():
    bids = Bid.objects.filter(quote__id = id)
  else:
    return redirect('homepage')
  
  return render(request, 'Client/WorkerQuotes.html', {'bids':bids})

@login_required(login_url='login')
def AcceptOrder(request, id):
  
  bid = Bid.objects.get(id = id)
  
  if request.method == "POST":
    action = request.POST.get("action")
    if action == "Accept":
      bid.accepted = True
      bid.status = "accepted"
      bid.save()
      order = Order.objects.create(
        bid = bid,
        client = User.objects.get(id = request.user.id),
      )
      order.save()
      redirect_url = request.build_absolute_uri(
            reverse('paymentpage', kwargs={'order_id': order.id})
            )
      return redirect(redirect_url)
    elif action == "Reject":
      bid.declined = True
      bid.status = "declined"
      bid.save()
      return redirect("clientdashboard")
  
  return render(request, 'Client/AcceptOrder.html',{'bid':bid})
def PaymentPage(request, order_id):

  order = Order.objects.get(id = order_id)
  if request.method == "POST":
    
    transaction_id = request.POST.get('transaction-id ')
    receipt = request.FILES.get('receipt')
    name = request.POST.get('name')
    
    order.paid= True
    order.payee_name = name
    order.receipt = receipt
    order.TID = transaction_id
    
    order.save()
    
    return redirect("clientorders")
  return render(request, 'Client/PaymentPage.html', {"order":order})


def getReviews(request):
  
  id = request.GET.get('worker_id')
  feedbacks = Feedback.objects.filter(user_id = id).order_by('-rating')
  feedbacks_list = []
  for feedback in feedbacks:
    feedbacks_list.append(feedback.to_json())
    
  
  return JsonResponse({'feedbacks':feedbacks_list})



def AllBlogs(request):
    blogs = Blog.objects.filter(is_active = True).order_by('-id')
    
    return render(request,'Website/Blogs.html', {'blogs':blogs})

def ReadBlog(request):
    image = []
    if request.GET.get('blog'):
        blog = Blog.objects.get(id = int(request.GET.get('blog')))
        images = BlogImage.objects.filter(blog = blog)
        
    else:
        blog = Blog.objects.all().first()
        images = BlogImage.objects.filter(blog = blog)
        
    return render(request,'Website/SingleBlog.html',{'blog':blog, 'images':images})



def AddBlog(request):
  
  if request.method == "POST":
    
            title = request.POST.get('addtitle')
            subtitle = request.POST.get('subtitle')
            desc = request.POST.get('adddesc')
            author = request.POST.get("AuthorName")
            image = request.FILES.get('blog_image')
            date_str = request.POST.get('Date')
            date_value = datetime.strptime(date_str, '%Y-%m-%d')
            
            first_para = request.POST.get('first_para')
            second_para = request.POST.get('second_para')
            third_para = request.POST.get('third_para')
            list1 = request.POST.get('list1')
            list2 = request.POST.get('list2')
            image2 = request.FILES.get('blog_image2')
            # reviewer = request.POST.get('reviewer')
            # review = request.POST.get('review')
            heading1 = request.POST.get('heading1')
            heading2 = request.POST.get('heading2')
            
            if Blog.objects.filter(
                title = title,
                subtitle = subtitle,
                description = desc,
                date = date_value,
                author = author,
                first_para = first_para 
                ).exists():
                
                pass
            else:
                blog = Blog.objects.create(
                    title = title,
                    subtitle = subtitle,
                    description = desc,
                    image = image,
                    is_active = True,
                    date = date_value,
                    author = author,
                    first_para = first_para,
                    second_para = second_para,
                    third_para = third_para,
                    list1 = list1,
                    list2 = list2,
                    image2 = image2,
                    # reviewer = reviewer,    
                    # review = review,    
                    heading1 = heading1,
                    heading2 = heading2

                )
                
                url = request.POST.get("youtubeurl")
                if url != "":
                    blog.video_url = url
                else:
                    video = request.FILES.get("video")
                    blog.video = video
                
                blog.save()

                for img in request.FILES.getlist("small_images"):
                    BlogImage.objects.create(
                        image = img,
                        blog = blog,
                    )
                
                return redirect("adminBlogs")
  return render(request,'Admin/AddBlog.html',{})
  pass



def AdminBlogs(request):
    
  if request.method == "POST":
    if request.POST.get("action") == "delete_blog":
      id = request.POST.get("blog_id")
      try:
        Blog.objects.get(id = id).delete()
      except: 
        pass
  
  active_blogs = Blog.objects.filter(is_active = True).order_by('-id')
  return render(request, 'Admin/Blogs.html', {'blogs':active_blogs})
    

def EditBlog(request):
    print(request.method)
    if request.method == "GET":
        blog_id = request.GET.get('blog_id')
        if(Blog.objects.filter(id=int(blog_id)).exists()):
            blog_instance = Blog.objects.get(id = int(blog_id))
            images = BlogImage.objects.filter(blog = blog_instance)
        
            return render(request, 'Admin/EditBlog.html',{'blog':blog_instance, 'images':images})

    else:
        
        action = request.POST.get('action')
        if action is None:
            blog_id = request.POST.get("id")

            blog_instance = None
            
            if(Blog.objects.filter(id=int(blog_id)).exists()):
                blog_instance = Blog.objects.get(id = int(blog_id))
            
            else:
                return None
            
            print(type(blog_instance))
            title = request.POST.get('addtitle')
            subtitle = request.POST.get('subtitle')
            desc = request.POST.get('adddesc')
            author = request.POST.get("AuthorName")
            image = request.FILES.get('image')
            date_str = request.POST.get('Date')
            date_value = datetime.strptime(date_str, '%Y-%m-%d')
            
            first_para = request.POST.get('first_para')
            second_para = request.POST.get('second_para')
            third_para = request.POST.get('third_para')
            list1 = request.POST.get('list1')
            list2 = request.POST.get('list2')
            # reviewer = request.POST.get('reviewer')
            # review = request.POST.get('review')
            heading1 = request.POST.get('heading1')
            heading2 = request.POST.get('heading2')
            
            if image is not None:
                blog_instance.image = image
                
            blog_instance.title = title
            blog_instance.subtitle = subtitle
            blog_instance.description = desc
            blog_instance.date = date_value
            blog_instance.author = author
            blog_instance.first_para = first_para  
            blog_instance.second_para = second_para   
            blog_instance.third_para = third_para   
            blog_instance.list1 = list1   
            blog_instance.list2 = list2
            blog_instance.heading1 = heading1
            blog_instance.heading2 = heading2
            
            
            
            url = request.POST.get("youtubeurl")
            if url != "" and url is not None:
                if blog_instance.video:
                    blog_instance.video = None
                    
                blog_instance.video_url = url
            else:
                video = request.FILES.get("video")
                if video:
                    if blog_instance.video_url != None or blog_instance.video_url != "":
                        blog_instance.video_url = ""
                    blog_instance.video = video
            
            imgs = request.FILES.getlist("small_images")
            
            if len(imgs)>0:
                # BlogImage.objects.filter(blog = blog_instance).delete()
                for img in imgs:
                    BlogImage.objects.create(
                        image = img,
                        blog = blog_instance,
                    )      
            
            
            blog_instance.save()
        
        elif action == "deleteImage":
            id = request.POST.get('img_id')
            if BlogImage.objects.filter(id = id).exists():
                blog_id = BlogImage.objects.get(id = id).blog.id
                BlogImage.objects.get(id = id).delete()
                redirect_url = reverse('editBlogs') + f'?blog_id={blog_id}'
                return redirect(redirect_url)
            pass
        elif action == "deleteVideo":
            blog_id = request.POST.get("blog_id")
            
            if Blog.objects.filter(id = blog_id).exists():
                blog = Blog.objects.get(id = blog_id)
                blog.url = ""
                blog.video = None
                blog.save()
                redirect_url = reverse('editBlogs') + f'?blog_id={blog_id}'
                return redirect(redirect_url)
            pass
        
        return redirect("adminBlogs")
