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
from users.views import applied_jobs, favorite_jobs, myprofile_commissioner
from users.views import myprofile_commissionee, manage_account_commissionee
from users.views import view_details, saved_candidates, manage_account_commissioner
from users.views import myprofile_commissionee, upload_resume, delete_resume, saved_candidates, update_job_status, view_commissionee

urlpatterns = [
    path('', homepage, name="homepage"),
    path('find_job/', find_job_notsigned, name='find_job_notsigned'),
    path('admin/', admin.site.urls),
    path('sign_in/', sign_in, name="sign_in"),
    path('registration/', registration, name="registration"),
    path('myjobs/', myjobs, name="myjobs"),
    path('find_job_candidate/', find_job_candidate, name="find_job_candidate"),
    path('settings/commissionee/', commissionee_settings, name="commissionee_settings"),
    path('settings/commissioner/', commissioner_settings, name="commissioner_settings"),
    path('post_job/', post_job, name="post_job"),
    path('applied_jobs/', applied_jobs, name="applied_jobs"),
    path('favorite_jobs/', favorite_jobs, name="favorite_jobs"),
    path('my_profile/commissioner/', myprofile_commissioner, name="myprofile_commissioner"),
    path('my_profile/commissionee/', myprofile_commissionee, name="myprofile_commissionee"),
    path('manage_account/commissionee/', manage_account_commissionee, name="manage_account_commissionee"),
    path('applied_jobs/view_details/', view_details, name="view_details"),
    path('manage_account/commissioner/', manage_account_commissioner, name="manage_account_commissioner"),
    path('resume/upload/', upload_resume, name='upload_resume'),
    path('resume/delete/<int:pk>/', delete_resume, name='delete_resume'),
    path('saved_candidates', saved_candidates, name='saved_candidates'),
    path('job/update_status/', update_job_status, name='update_job_status'),
    path('view_commissionee', view_commissionee, name='view_commissionee'),

    path('job/delete/<int:job_id>/', views.delete_job, name='delete_job'),


    
    path('logout/', auth_views.LogoutView.as_view(next_page="homepage"), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
