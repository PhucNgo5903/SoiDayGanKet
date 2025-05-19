from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app.models import AssistanceRequest
from .views import role_required
from django.core.paginator import Paginator

@role_required('admin')
def index_admin(request):
    return render(request, "admin/index-admin.html")

@role_required('admin')
def new_assistance_request(request):
    per_page = request.GET.get('entries', 'all')
   
    assistance_requests = AssistanceRequest.objects.filter(status='pending').order_by('-created_at')
    
    
    if per_page == 'all':
        page_obj = assistance_requests  
        is_paginated = False
    else:
        try:
            per_page = int(per_page)
        except ValueError:
            per_page = 10  

        paginator = Paginator(assistance_requests, per_page)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        is_paginated = page_obj.has_other_pages()
    
    context = {
        'page_obj': page_obj,
        'per_page': per_page,
        'is_paginated': is_paginated,
        'total_count': assistance_requests.count(),
    }
    return render(request, 'admin/new-assistance-request.html', context)



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