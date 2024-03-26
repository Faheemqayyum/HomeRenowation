from django.shortcuts import render, redirect
from .models import *
# Create your views here.

def Homepage(request):
  request.session['abc'] = 'ABCD'
  return  render(request, 'Website/homepage.html')

def SearchPros(request):
  return  render(request, 'Website/Search_pros.html')
def SearchProject(request):
  return  render(request, 'Website/Search_project.html')

def LoginPage(request):
  return  render(request, 'Website/Login.html')
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
      
      return redirect('login')
      
  return  render(request, 'Website/Signup.html', {"form":form, 'error':error})
def ResetPassword(request):
  return  render(request, 'Website/ResetPassword.html')
# Admin
def AdminDashboard(request):
  return  render(request, 'Admin/AdminDashboard.html')
def RecentMembers(request):
  return  render(request, 'Admin/RecentMembers.html')
def RecentWorkers(request):
  return  render(request, 'Admin/RecentWorkers.html')

# Worker
def WorkerDashboard(request):
  return  render(request, 'Worker/WorkerDashboard.html')
def WorkerSample(request):
  return  render(request, 'Worker/Workersamples.html')
def AddWorkerSample(request):
  return  render(request, 'Worker/AddWorkSamples.html')
def WorkerProfile(request):
  return  render(request, 'Worker/Profile.html')
def EditWorkerProfile(request):
  return  render(request, 'Worker/EditProfile.html')

# Client
def ClientDashboard(request):
  return  render(request, 'Worker/Dashboard.html')
def ShowJobs(request):
  return  render(request, 'Worker/PostJobs.html')
def AddJob(request):
  return  render(request, 'Worker/AddJob.html')
def ClientProfile(request):
  return  render(request, 'Worker/Profile.html')
