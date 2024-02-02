from importlib import resources
from os import name
from tracemalloc import start
from django.shortcuts import redirect, render
from core.decorators import login_required_student
from django.contrib import messages
from django.contrib.auth.models import User
from core.models import  Course, Evaluation, Post, Score, Student, StudentCourse, University
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from urllib.parse import urlparse, urlunparse
from core.utils import email_sender
from .forms import FileUploadForm
import pandas as pd
import random

# from django.contrib import messages

# Create your views here.


def login_view(request):
    if request.method == 'POST':
        # form = AuthenticationForm(request, data=request.POST)
        passcode = request.POST.get('passcode')
        # print(form.is_valid())
        if passcode:
            # Authenticate the user
            # username = form.cleaned_data.get('username')
            # password = form.cleaned_data.get('username')
            user = User.objects.filter(username=passcode).first()

            if user is not None:
                # Log in the user
                print(user.first_name)
                login(request, user)
                messages.success(request, f"Welcome, {user.first_name}!")  
                # Redirect to the 'next' parameter if present, otherwise to the home page
                next_param = request.GET.get('next')
                if next_param:
                    # Validate and sanitize the 'next' parameter to prevent open redirects
                    next_url = urlparse(next_param)
                    if not next_url.netloc:
                        return redirect(next_url.path)
                
                return redirect('/')  # Redirect to your home page or any other desired page after login
            else:
                messages.error(request, "Invalid passcode.")
        else:
            messages.error(request, "The passcode is required please.")
        # form = AuthenticationForm()
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            course = form.cleaned_data.get('course')
            # print(course.name)
            if course is None:
                messages.error(request,f"Error class not found")
                return render(request, 'registerusers.html', {'form': form}) 
            
            try:
                # Read the Excel file using pandas
                df = pd.read_excel(excel_file)

                # Loop through the rows and create profiles
                for index, row in df.iterrows():

                    code = random.randint(10, 9999999)

                    user = User.objects.create(
                        first_name=row[0],
                        last_name=row[1],
                        email=row[2],
                        password="",
                        username=code
                    )
                    
                    student = Student.objects.create(
                        student_id=row[3],
                        user = user,
                        university=course.university
                    )
                    
                    StudentCourse.objects.create(
                        student = student,
                        course = course
                    )
                    email_sender('Temporary elearning platform', f'{user.first_name}, this is your code to access the platform {code}. This is your code, do not share it with anyone.', user.email)
                
                # Optionally, you can add additional logic here
                messages.info(request, f'Registared {index+1} students in the {course.name} course - {course.university.name} University.')
                return redirect('/')  # Redirect to a success page or wherever needed
            except Exception as e:
                # Handle any errors that may occur during file processing
                messages.error(request,f"Error processing file: {str(e)}")
                return render(request, 'registerusers.html', {'form': form})
    else:
        form = FileUploadForm()

    return render(request, 'registerusers.html', {'form': form})


def home_page(request):
    context = {
        "page":"Patrick Iradukunda"
    }
    # messages.error(request, "You must be studented of the selected university to access this resource.")
    
    return render(request, 'home.html', context=context)


def teaching_page(request):
    resources = Post.objects.filter(public=True, p_type='r')
    universities = University.objects.all()
    context = {
        "page":"Teaching Activities",
        "resources":resources,
        "universities":universities
    }
    return render(request, 'core/teaching.html', context=context)


def personal_page(request):
    context = {
        "page":"Personal Information"
    }
    return render(request, 'core/personal.html', context=context)


def projects_page(request):
    posts = Post.objects.filter(public=True)
    context = {
        "page":"Research Activities - Projects",
        "posts":posts
    }
    return render(request, 'core/projects.html', context=context)


@login_required_student
def university(request, id):
    university = University.objects.filter(id=id).first()
    student = Student.objects.filter(user=request.user, university=university).first()
    if university:
        if student:
            courses_student = StudentCourse.objects.filter(student=student)
            resources = []
            courses = []
            for cs in courses_student:
                course = cs.course
                courses.append(course)
                resource = Post.objects.filter(course=course)
                resources.append(resource)
                
            scores = Score.objects.filter(student=student)
            # print(resources)
            context = {
                "student":student,
                "resources": resources,
                "scores": scores,
                "courses": courses,
                "university":university,
            }
            return render(request, 'core/university.html', context)
        
    messages.error(request, "You must be studented of the selected university to access this resource.")
    return redirect('/login')