from django.shortcuts import redirect, render
from django.contrib import messages
from core.models import Student

def login_required_student(view_func):
    def wrapper(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            if Student.objects.filter(user=user).first():
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "You must be logged in as a student to access this resource.")
                return render(request, request.path, {}) 
        else:
            messages.error(request, "You must be logged in to access this resource.")
            return redirect(f'/login?next={request.path}')  # Redirect to your login page or any other desired page
    return wrapper
