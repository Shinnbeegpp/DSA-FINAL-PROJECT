
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from .models import UserProfile, UserResume, Job
from .forms import UserUpdateForm, ProfileUpdateForm, ResumeForm
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
# Create your views here.

def homepage(request):
    return render(request,'homepage.html')




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
from django.db.models import Q # <--- IMPORT THIS at the top
from .models import Job

@login_required
def find_job_candidate(request):
    # 1. Start with all Open/Active jobs
    jobs = Job.objects.filter(status__in=['Open', 'Active']).order_by('-created_at')

    # 2. Search Bar
    query = request.GET.get('q')
    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query)
        )

    # 3. Campus Filter (Multi-select)
    campuses = request.GET.getlist('campus')
    if campuses:
        jobs = jobs.filter(campus__in=campuses)

    # 4. Budget Filter (Multi-select Checkboxes)
    budget_ranges = request.GET.getlist('budget_range') # Now accepts multiple
    if budget_ranges:
        # We use Q objects to combine ranges with "OR" logic
        budget_query = Q()
        
        for range_val in budget_ranges:
            if range_val == '100-500':
                budget_query |= Q(budget__gte=100, budget__lte=500) # |= means OR
            elif range_val == '500-1500':
                budget_query |= Q(budget__gte=500, budget__lte=1500)
            elif range_val == '1500-3000':
                budget_query |= Q(budget__gte=1500, budget__lte=3000)
            elif range_val == '3000-5000':
                budget_query |= Q(budget__gte=3000, budget__lte=5000)
            elif range_val == '5000+':
                budget_query |= Q(budget__gte=5000)
        
        # Apply the combined budget filter
        jobs = jobs.filter(budget_query)

    # 5. Category Filter (Multi-select + Smart "Others")
    selected_categories = request.GET.getlist('category')
    if selected_categories:
        # List of your "Standard" categories defined in HTML
        standard_list = [
            "Academic Assistance", "Graphic Design", "Programming", 
            "Video Editing", "Multimedia Arts", "Data Analysis", "Tutoring"
        ]

        category_query = Q()

        # Add the specific categories checked by user (e.g., Programming)
        category_query |= Q(category__in=[c for c in selected_categories if c != 'Others'])

        # If "Others" is checked, include ANY category that is NOT in the standard list
        if 'Others' in selected_categories:
            category_query |= ~Q(category__in=standard_list) # ~Q means NOT IN

        jobs = jobs.filter(category_query)
        
    paginator = Paginator(jobs, 5) # Show 5 jobs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'jobs': page_obj,
        'selected_campuses': campuses,
        'selected_categories': selected_categories,
        'selected_budget': budget_ranges, # Pass list back to HTML
        'query': query,
    }
    return render(request, 'find_job_candidate.html', context)

def find_job_notsigned(request):
    # 1. Start with all Open/Active jobs
    jobs = Job.objects.filter(status__in=['Open', 'Active']).order_by('-created_at')

    # 2. Search Bar
    query = request.GET.get('q')
    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query)
        )

    # 3. Campus Filter (Multi-select)
    campuses = request.GET.getlist('campus')
    if campuses:
        jobs = jobs.filter(campus__in=campuses)

    # 4. Budget Filter (Multi-select Checkboxes)
    budget_ranges = request.GET.getlist('budget_range') # Now accepts multiple
    if budget_ranges:
        # We use Q objects to combine ranges with "OR" logic
        budget_query = Q()
        
        for range_val in budget_ranges:
            if range_val == '100-500':
                budget_query |= Q(budget__gte=100, budget__lte=500) # |= means OR
            elif range_val == '500-1500':
                budget_query |= Q(budget__gte=500, budget__lte=1500)
            elif range_val == '1500-3000':
                budget_query |= Q(budget__gte=1500, budget__lte=3000)
            elif range_val == '3000-5000':
                budget_query |= Q(budget__gte=3000, budget__lte=5000)
            elif range_val == '5000+':
                budget_query |= Q(budget__gte=5000)
        
        # Apply the combined budget filter
        jobs = jobs.filter(budget_query)

    # 5. Category Filter (Multi-select + Smart "Others")
    selected_categories = request.GET.getlist('category')
    if selected_categories:
        # List of your "Standard" categories defined in HTML
        standard_list = [
            "Academic Assistance", "Graphic Design", "Programming", 
            "Video Editing", "Multimedia Arts", "Data Analysis", "Tutoring"
        ]

        category_query = Q()

        # Add the specific categories checked by user (e.g., Programming)
        category_query |= Q(category__in=[c for c in selected_categories if c != 'Others'])

        # If "Others" is checked, include ANY category that is NOT in the standard list
        if 'Others' in selected_categories:
            category_query |= ~Q(category__in=standard_list) # ~Q means NOT IN

        jobs = jobs.filter(category_query)
        
    paginator = Paginator(jobs, 5) # Show 5 jobs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'jobs': page_obj,
        'selected_campuses': campuses,
        'selected_categories': selected_categories,
        'selected_budget': budget_ranges, # Pass list back to HTML
        'query': query,
    }
    return render(request, 'find_job_notsigned.html', context)


#@never_cache       <---  @never_cache   
@login_required
def myjobs(request):
    # 1. Fetch only jobs posted by this user
    jobs = Job.objects.filter(commissioner=request.user).order_by('-created_at')
    
    # 2. Handle Status Filter (from the dropdown)
    status_filter = request.GET.get('status') # Get from URL ?status=Active
    if status_filter and status_filter != 'All Applications':
        jobs = jobs.filter(status=status_filter)

    # 3. Pass data to HTML
    context = {
        'jobs': jobs,
        'total_jobs': jobs.count(),
        'current_filter': status_filter or 'All Applications'
    }
    return render(request, 'myjobs.html', context)

def update_job_status(request):
    if request.method == 'POST':
        job_id = request.POST.get('job_id')
        new_status = request.POST.get('status')
        job = Job.objects.get(id=job_id, commissioner=request.user)
        job.status = new_status
        job.save()
        return redirect('myjobs')

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
        if department == 'Others / Not Listed':
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

@login_required
def delete_job(request, job_id):
    # 1. Get the job, but ONLY if it belongs to the current user
    # This prevents users from deleting other people's jobs by guessing the ID
    job = get_object_or_404(Job, id=job_id, commissioner=request.user)
    
    # 2. Delete it
    job.delete()
    
    # 3. Message and Redirect
    messages.success(request, "Job deleted successfully.")
    return redirect('myjobs')

@login_required
def view_commissionee(request):
    return render(request,'view_commissionee.html')