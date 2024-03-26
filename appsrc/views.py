from django.shortcuts import render

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
  return  render(request, 'Website/Signup.html')
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
