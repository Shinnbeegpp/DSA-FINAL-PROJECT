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


from users.views import homepage, sign_in, find_job_notsigned
from users.views import registration, success, myjobs, find_job_candidate
from users.views import commissionee_settings, commissioner_settings, post_job

urlpatterns = [
    path('', homepage, name="homepage"),
    path('find_job/', find_job_notsigned, name='find_job_notsigned'),
    path('admin/', admin.site.urls),
    path('sign_in/', sign_in, name="sign_in"),
    path('registration/', registration, name="registration"),
    path('success/', success, name="success"),
    path('myjobs/', myjobs, name="myjobs"),
    path('find_job_candidate/', find_job_candidate, name="find_job_candidate"),
    path('settings/commissionee/', commissionee_settings, name="commissionee_settings"),
    path('settings/commissioner/', commissioner_settings, name="commissioner_settings"),
    path('post_job/', post_job, name="post_job")
]
