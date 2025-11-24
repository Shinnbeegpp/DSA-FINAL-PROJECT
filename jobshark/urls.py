from django.contrib import admin
from django.urls import path



from users.views import homepage, sign_in, find_job, registration, myjobs, find_job_commissionee


urlpatterns = [
    path('', homepage, name="homepage"),
    path('find_job/', find_job, name='find_job'),
    path('admin/', admin.site.urls),
    path('sign_in/', sign_in, name="sign_in"),
    path('registration/', registration, name="registration"),
    path('myjobs/', myjobs, name="myjobs"),
    path('find_job_commissionee/', find_job_commissionee, name="find_job_commissionee"),

]
