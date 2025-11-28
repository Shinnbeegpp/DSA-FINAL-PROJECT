
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from .models import UserProfile, UserResume, Job
from .forms import UserUpdateForm, ProfileUpdateForm, ResumeForm

# Create your views here.

def homepage(request):
    return render(request,'homepage.html')


def find_job_notsigned(request):
    return render(request, 'find_job_notsigned.html')

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

        if user is not None:
            login(request, user)

            try:
        
                profile = UserProfile.objects.get(user=user)

                if profile.account_type == 'commissionee':
                    return redirect('find_job_candidate') 
                
                elif profile.account_type == 'commissioner':
 
                    return redirect('myprofile_commissioner')
                
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

@login_required
def commissioner_settings(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save() 
            p_form.save() 
            messages.success(request, 'Your profile has been updated!')
            return redirect('commissioner_settings') 

    else:
     
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.userprofile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'commissioner_settings.html', context)

def myprofile_commissioner(request):
    return render(request,'myprofile_commissioner.html')

def myprofile_commissionee(request):
    return render(request,'myprofile_commissionee.html')

#@never_cache      
#@login_required   
def find_job_candidate(request):
    return render(request,'find_job_candidate.html')

      
#@never_cache       <---  @never_cache   
#@login_required    <---  @login_required    
def myjobs(request):
    return render(request,'myjobs.html')

#@never_cache      
@login_required    
def commissionee_settings(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save() 
            p_form.save() 
            messages.success(request, 'Your profile has been updated!')
            return redirect('commissionee_settings') 

    else:
     
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.userprofile)

    resumes = UserResume.objects.filter(user=request.user)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'resumes': resumes,
    }

    return render(request,'commissionee_settings.html', context)

@login_required
def upload_resume(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            # Check if user already has 3 resumes (Optional limit)
            if UserResume.objects.filter(user=request.user).count() >= 3:
                messages.error(request, "You can only upload up to 3 resumes.")
            else:
                resume = form.save(commit=False)
                resume.user = request.user
                resume.save()
                messages.success(request, "Resume uploaded successfully!")
        else:
            messages.error(request, "Error uploading file. Please upload a valid PDF/Doc.")
    
    return redirect('commissionee_settings')

@login_required
def delete_resume(request, pk):

    resume = get_object_or_404(UserResume, pk=pk, user=request.user)
    resume.delete()
    messages.success(request, "Resume deleted.")
    return redirect('commissionee_settings')

#@never_cache      
#@login_required    
def post_job(request):
    return render(request,'post_job.html')

#@never_cache       
#@login_required    
def applied_jobs(request):
    return render(request,'applied_jobs.html')

#@never_cache      
#@login_required 
def favorite_jobs(request):
    return render(request,'favorite_jobs.html')

def saved_candidates(request):
    return render(request,'saved_candidates.html')


def manage_account_commissionee(request):
    return render(request,'commissionee_settings.html')

def manage_account_commissioner(request):
    return render(request,'commissioner_settings.html')

def view_details(request):
    return render(request,'view_details.html')

@login_required
def post_job(request):
    if request.method == 'POST':
        # 1. Get basic data
        title = request.POST.get('title')
        budget = request.POST.get('budget')
        
        # 2. Handle "Category" logic (Check if "Others" was used)
        category = request.POST.get('category')
        if category == 'Others':
            category = request.POST.get('category_other') # Get the text input instead

        # 3. Handle "Department" logic (Check if "Others" was used)
        department = request.POST.get('department')
        if department == 'Others':
            department = request.POST.get('department_other')

        campus = request.POST.get('campus')
        academic_level = request.POST.get('academic_level')
        description = request.POST.get('description')
        deliverables = request.POST.get('deliverables')

        # 4. Create the Job
        Job.objects.create(
            commissioner=request.user,
            title=title,
            category=category,
            budget=budget,
            campus=campus,
            department=department,
            academic_level=academic_level,
            description=description,
            deliverables=deliverables
        )

        # 5. Success Message (Triggers the Modal)
        messages.success(request, "Job posted successfully!")
        return redirect('post_job') # Stay on page to show modal

    return render(request, 'post_job.html')