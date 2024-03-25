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
    path('recentworkers/',views.RecentWorkers,name='recentworkers'),
    # Worker
    path('workerdashboard/',views.WorkerDashboard,name='workerdashboard'),
    path('workersample/',views.WorkerSample,name='workersample'),
]
