from django.shortcuts import render

# Create your views here.

def homepage(request):
    return render(request,'homepage.html')


def find_job(request):
    return render(request, 'find_job.html')

def registration(request):
    return render(request,'createAccount.html')

