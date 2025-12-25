"""
URL configuration for new_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

""" old urls 
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("new_project.sm_cool.urls")),

]"""

from django.contrib import admin
from django.urls import path, include

# Temporary management functions (for FREE deployment – no Shell required)
from django.core.management import call_command
from django.http import HttpResponse

def run_migrations(request):
    call_command("migrate")
    return HttpResponse("✓ Migrations completed. Database is ready.")

def create_admin(request):
    from django.contrib.auth.models import User
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@example.com", "Admin@123")
        return HttpResponse("✓ Admin created → username: admin / password: Admin@123")
    return HttpResponse("⚠ Admin already exists.")

urlpatterns = [
    path('admin/', admin.site.urls),

    # your app
    path('', include("sm_cool.urls")),


    # temporary public admin-creation endpoints (REMOVE AFTER USE)
    path("run/migrate/", run_migrations),
    path("run/createadmin/", create_admin),
]
