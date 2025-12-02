"""
URL configuration for jobshark project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# 1. ADD THIS IMPORT for the built-in logout functionality
from django.contrib.auth import views as auth_views

from users import views

from users.views import homepage, sign_in, find_job_notsigned
from users.views import registration, myjobs, find_job_candidate
from users.views import commissionee_settings, commissioner_settings, post_job
from users.views import applied_jobs, active_commissions, myprofile_commissioner
from users.views import myprofile_commissionee, view_details, active_commissionees
from users.views import myprofile_commissionee, upload_resume, delete_resume
from users.views import update_application_status, update_job_status
from users.views import view_commissionee, apply_for_job

urlpatterns = [
    # General URLs
    path('', homepage, name="homepage"),
    path('find_job/', find_job_notsigned, name='find_job_notsigned'),
    path('admin/', admin.site.urls),
    path('sign_in/', sign_in, name="sign_in"),
    path('registration/', registration, name="registration"),
    path('logout/', auth_views.LogoutView.as_view(next_page="homepage"), name='logout'),
    
    # Commissioner URLs
    path('myjobs/', myjobs, name="myjobs"),
    path('settings/commissioner/', commissioner_settings, name="commissioner_settings"),
    path('post_job/', post_job, name="post_job"),
    path('my_profile/commissioner/', myprofile_commissioner, name="myprofile_commissioner"),
    path('resume/upload/', upload_resume, name='upload_resume'),
    path('resume/delete/<int:pk>/', delete_resume, name='delete_resume'),
    path('active_commissionees/', active_commissionees, name='active_commissionees'),
    path('job/update_status/', update_job_status, name='update_job_status'),
    path('job/<int:job_id>/applicants/', view_commissionee, name='view_commissionee'),
    path('job/delete/<int:job_id>/', views.delete_job, name='delete_job'),
    path('job/<int:job_id>/apply/', apply_for_job, name='apply_for_job'),
    path('application/<int:application_id>/update/<str:new_status>/', update_application_status, name='update_application_status'),
    
    # Commissionee URLs
    path('find_job_candidate/', find_job_candidate, name="find_job_candidate"),
    path('settings/commissionee/', commissionee_settings, name="commissionee_settings"),
    path('applied_jobs/', applied_jobs, name="applied_jobs"),
    path('my_profile/commissionee/', myprofile_commissionee, name="myprofile_commissionee"), 
    path('job/<int:job_id>/details/', view_details, name="view_details"),
    path('active_commissions/', active_commissions, name='active_commissions'),    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
