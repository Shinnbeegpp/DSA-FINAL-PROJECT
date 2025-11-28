from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, UserResume


# Form for the built-in User model (First Name, Last Name, Email)
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField() # specific validation for email

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

# Form for your custom UserProfile model (Image, Campus, Bio, etc.)
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'profile_picture', 
            'campus_institution', 
            'student_classification', 
            'date_of_birth',
            'gender',
            'education',
            'experience_level',
            'biography',
            'social_link',
            'phone_number'
        ]
        # This adds the calendar widget to the date field
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

class ResumeForm(forms.ModelForm):
    class Meta:
        model = UserResume
        fields = ['file']