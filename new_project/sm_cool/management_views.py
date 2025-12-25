from django.http import HttpResponse
from django.core.management import call_command

def migrate(request):
    call_command("migrate")
    return HttpResponse("Migrations complete.")

def create_admin(request):
    from django.contrib.auth.models import User
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@example.com", "Admin@123")
        return HttpResponse("Admin user created! username=admin password=Admin@123")
    return HttpResponse("Admin already exists!")
