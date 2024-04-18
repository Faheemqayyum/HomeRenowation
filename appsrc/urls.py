from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static 


urlpatterns = [
    path('',views.Homepage,name='homepage'),
    path('homepage/',views.Homepage,name='homepage'),
    path('searchpros/',views.SearchPros,name='searchpros'),
    path('searchproject/',views.SearchProject,name='searchproject'),
    path('quoteproject/',views.QuoteProject,name='quoteproject'),
    
    path('login/',views.LoginPage,name='login'),
    path('logout/',views.logout,name='logout'),
    path('register/',views.SignUpPage,name='register'),
    path('resetpassword/',views.ResetPassword,name='resetpassword'),
    
    # Admin
    path('admindashboard/',views.AdminDashboard,name='admindashboard'),
    path('accept_reject_user/',views.acceptRejectUser,name='accept_reject_user'),
    
    path('recentmembers/',views.RecentMembers,name='recentmembers'),
    path('memberdetail/',views.MemberDetail,name='memberdetail'),
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
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)

