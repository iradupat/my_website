from django.urls import path
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.home_page),
    path('login', views.login_view),
    path('teaching', views.teaching_page),
    path('projects', views.projects_page),
    path('personal', views.personal_page),
    path('university/<id>', views.university),
    path('adduser', views.register)
    
]