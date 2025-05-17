from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .views import role_required


def index_admin(request):
    return render(request, "admin/index-admin.html")


def new_assistance_request(request):
    return render(request, "admin/new-assistance-request.html")

def assistance_request_detail(request):
    return render(request, "admin/assistance-request-detail.html")

def accepted_assistance_request(request):
    return render(request, "admin/accepted-assistance-request.html")

def status_updated_request_detail(request):
    return render(request, "admin/status-updated-request-detail.html")

def rejected_assistance_request(request):
    return render(request, "admin/rejected-assistance-request.html")

def total_volunteer(request):
    return render(request, "admin/total_volunteer.html")

def admin_volunteer_detail(request):
    return render(request, "admin/admin-volunteer-detail.html")