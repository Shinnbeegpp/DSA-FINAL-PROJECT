
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import UserProfile

# Create your views here.\
# Create your views here.

def homepage(request):
    return render(request,'homepage.html')


def find_job(request):
    return render(request, 'find_job.html')

def registration(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        account_type = request.POST.get('account_type')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        context = {
            'values': request.POST 
        }

        if not account_type:
            context['error_account_type'] = "Please select the type of account you want to create."
            return render(request, 'registration.html', context)
        
        if pass1 != pass2:
            context['error_password'] = "Passwords do not match."
            return render(request, 'registration.html', context)

        if User.objects.filter(username=username).exists():
            context['error_username'] = "This username is already taken."
            return render(request, 'registration.html', context)
        
 
        if User.objects.filter(email=email).exists():
            context['error_email'] = "This email is already registered."
            return render(request, 'registration.html', context)


        user = User.objects.create_user(username=username, email=email, password=pass1)
        

        user.first_name = first_name
        user.last_name = last_name
        user.save() 

        profile = UserProfile(user=user, account_type=account_type)
        profile.save()


        messages.success(request, "Account created successfully! Please sign in.")
        return redirect('sign_in')

        
    return render(request,'registration.html')

def sign_in(request):
    if request.method == 'POST':
    
        username = request.POST.get('username')
        password = request.POST.get('password')

      
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)
            try:
                profile = UserProfile.objects.get(user=user)
            
                if profile.account_type == 'commissionee':
                    return redirect('find_job_commissionee') 
                
                elif profile.account_type == 'commissioner':
                    return redirect('myjobs')
                
                else:
                    return redirect('homepage') 

            except UserProfile.DoesNotExist:
                messages.error(request, "Account setup incomplete. Please contact support.")
                return redirect('sign_in')
        else:
            return render(request, 'signin.html', {
                'error_login': "Invalid username or password.",
                'values': request.POST 
            })

    return render(request,'signin.html')

def myjobs(request):
    return render(request, "myjobs.html")

def find_job_commissionee(request):
    return render(request, "find_job_commissionee.html")