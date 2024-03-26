from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.Homepage,name='homepage'),
    path('homepage/',views.Homepage,name='homepage'),
    path('searchpros/',views.SearchPros,name='searchpros'),
    path('searchproject/',views.SearchProject,name='searchproject'),
    
    path('login/',views.LoginPage,name='login'),
    path('register/',views.SignUpPage,name='register'),
    path('resetpassword/',views.ResetPassword,name='resetpassword'),
    
    # Admin
    path('admindashboard/',views.AdminDashboard,name='admindashboard'),
    path('recentmembers/',views.RecentMembers,name='recentmembers'),
    # path('recentmemberdetail/',views.RecentMembersDetail,name='recentmemberdetail'),
    path('recentworkers/',views.RecentWorkers,name='recentworkers'),
    path('recentworkersdetail/',views.RecentWorkersDetail,name='recentworkersdetail'),
    # Worker
    path('workerdashboard/',views.WorkerDashboard,name='workerdashboard'),
    path('workersample/',views.WorkerSample,name='workersample'),
    path('addwork/',views.AddWorkerSample,name='addwork'),
    path('workerprofile/',views.WorkerProfile,name='workerprofile'),
    path('editworkerprofile/',views.EditWorkerProfile,name='editworkerprofile'),
     # Client
    path('clientdashboard/',views.ClientDashboard,name='clientdashboard'),
    path('showjob/',views.ShowJobs,name='showjob'),
    path('addjob/',views.AddJob,name='addjob'),
    path('clientprofile/',views.ClientProfile,name='clientprofile'),
    path('editclientprofile/',views.EditClientProfile,name='editclientprofile'),
]
