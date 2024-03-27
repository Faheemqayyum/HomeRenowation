from django.shortcuts import render, redirect
from .models import *

from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.

def Homepage(request):
  return  render(request, 'Website/homepage.html')

def SearchPros(request):
  return  render(request, 'Website/Search_pros.html')
def SearchProject(request):
  return  render(request, 'Website/Search_project.html')


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
          return redirect("admindashboard")
        elif user.is_worker:
          return redirect("workerdashboard")
        else:
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
def RecentWorkersDetail(request):
  return  render(request, 'Admin/RecentWorkerDetail.html')
# def RecentMembersDetail(request):
#   return  render(request, 'Admin/RecentMemberDetail.html')

# Worker
@login_required(login_url='login')
def WorkerDashboard(request):
  if not request.user.is_profile_set:
    return redirect("editworkerprofile")
  return  render(request, 'Worker/WorkerDashboard.html')


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
  
  return  render(request, 'Client/Dashboard.html')


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
