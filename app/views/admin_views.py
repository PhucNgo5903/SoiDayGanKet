from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .views import role_required


@role_required('admin')
def index_admin(request):
    return render(request, "admin/index-admin.html")

@role_required('admin')
def new_assistance_request(request):
    return render(request, "admin/new-assistance-request.html")

@role_required('admin')
def assistance_request_detail(request):
    return render(request, "admin/assistance-request-detail.html")

@role_required('admin')
def accepted_assistance_request(request):
    return render(request, "admin/accepted-assistance-request.html")

@role_required('admin')
def status_updated_request_detail(request):
    return render(request, "admin/status-updated-request-detail.html")

@role_required('admin')
def rejected_assistance_request(request):
    return render(request, "admin/rejected-assistance-request.html")

@role_required('admin')
def total_volunteer(request):
    return render(request, "admin/total_volunteer.html")

@role_required('admin')
def admin_volunteer_detail(request):
    return render(request, "admin/admin-volunteer-detail.html")