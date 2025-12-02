from django.db import models
from django.contrib.auth.models import User
import os

class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    

    ACCT_TYPES = [
        ('commissioner', 'Commissioner'),
        ('commissionee', 'Commissionee'),
    ]
    account_type = models.CharField(max_length=21, choices=ACCT_TYPES)

    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    CAMPUS_CHOICES = [
        ('BatStateU - Pablo Borbon (Main I)', 'BatStateU - Pablo Borbon (Main I)'),
        ('BatStateU - Alangilan (Main II)', 'BatStateU - Alangilan (Main II)'),
        ('BatStateU - ARASOF Nasugbu', 'BatStateU - ARASOF Nasugbu'),
        ('BatStateU - Lipa', 'BatStateU - Lipa'),
        ('BatStateU - Malvar (JPLPC)', 'BatStateU - Malvar (JPLPC)'),
        ('BatStateU - Balayan', 'BatStateU - Balayan'),
        ('BatStateU - Lemery', 'BatStateU - Lemery'),
        ('BatStateU - Rosario', 'BatStateU - Rosario'),
        ('BatStateU - San Juan', 'BatStateU - San Juan'),
        ('BatStateU - Lobo', 'BatStateU - Lobo'),
        ('BatStateU - Mabini', 'BatStateU - Mabini'),
        ('BatStateU - Lima', 'BatStateU - Lima'),
    ]

    campus_institution = models.CharField(max_length=100, choices=CAMPUS_CHOICES, null=True, blank=True)

    # --- Education Level Choices ---
    EDUCATION_CHOICES = [
        ('1st Year', '1st Year'),
        ('2nd Year', '2nd Year'),
        ('3rd Year', '3rd Year'),
        ('4th Year', '4th Year'),
        ('5th Year', '5th Year'),
        ('Master\'s Degree', 'Master\'s Degree'),
        ('Doctorate / PhD', 'Doctorate / PhD'),
    ]
    education = models.CharField(max_length=50, choices=EDUCATION_CHOICES, null=True, blank=True)

    CLASSIFICATION_CHOICES = [
        ('Regular Student (Full Load)', 'Regular Student (Full Load)'),
        ('Irregular Student (Flexible Schedule)', 'Irregular Student (Flexible Schedule)'),
        ('Working Student', 'Working Student'),
        ('Graduating / Thesis Year', 'Graduating / Thesis Year'),
        ('Alumni / Graduate', 'Alumni / Graduate'),
    ]
    
    student_classification = models.CharField(max_length=100, choices=CLASSIFICATION_CHOICES, null=True, blank=True)
    
    EXPERIENCE_CHOICES = [
        ('Beginner (No paid experience)', 'Beginner (No paid experience)'),
        ('Academic Projects Only (Thesis/Capstone)', 'Academic Projects Only (Thesis/Capstone)'),
        ('Freelancing / Commissions', 'Freelancing / Commissions'),
        ('Internship / OJT Experience', 'Internship / OJT Experience'),
        ('Professional / Industry Work', 'Professional / Industry Work'),
    ]

    experience_level = models.CharField(max_length=100, choices=EXPERIENCE_CHOICES, null=True, blank=True)

    date_of_birth = models.DateField(null=True, blank=True)

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)

    biography = models.TextField(null=True, blank=True)

    # --- Contact Information (From your last screenshot) ---
    social_link = models.URLField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.account_type}"

    def __str__(self):
        return f"{self.user.username} - {self.account_type}"


class UserResume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def filename(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return f"{self.user.username} - Resume"


class Job(models.Model):
    # Link to the Commissioner who posted it
    commissioner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_jobs')
    
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Advanced Info
    campus = models.CharField(max_length=150)
    department = models.CharField(max_length=150)
    academic_level = models.CharField(max_length=100)
    
    # Details
    description = models.TextField()
    deliverables = models.TextField()
    
    # System fields
    STATUS_CHOICES = [
        ('Active', 'Active'),       # Job is open for applications
        ('Ongoing', 'Ongoing'),     # Applicant accepted, work in progress
        ('Done', 'Done'),           # Work completed
        ('Cancelled', 'Cancelled'), # Job cancelled by commissioner
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')

    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_applications')
    

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    
    date_applied = models.DateTimeField(auto_now_add=True)


    cover_letter = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('job', 'applicant') 

    def __str__(self):
        return f"{self.applicant.username} -> {self.job.title}"