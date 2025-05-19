
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from app.models import AssistanceRequest, AssistanceRequestImage, AssistanceRequestTypeMap
from .views import role_required
from django.core.paginator import Paginator
from django.utils import timezone   

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
def assistance_request_detail(request, pk):
    assistance_request = get_object_or_404(AssistanceRequest, pk=pk)
    images = AssistanceRequestImage.objects.filter(assistance_request=assistance_request)
    support_types = AssistanceRequestTypeMap.objects.filter(assistance_request=assistance_request)

    if request.method == "POST":
        new_status = request.POST.get("status")
        new_remark = request.POST.get("admin_remark")

        old_status = assistance_request.status  # giữ lại status cũ

        # Cập nhật thông tin
        assistance_request.status = new_status
        assistance_request.admin_remark = new_remark

        # Nếu status thay đổi, cập nhật thời gian và người cập nhật
        if old_status != new_status:
            assistance_request.update_status_at = timezone.now()
            if hasattr(request.user, 'nguoidung'):  # kiểm tra tránh lỗi nếu chưa có liên kết
                assistance_request.update_by = request.user.nguoidung

        assistance_request.save()

        return render(request, "admin/assistance-request-detail.html", {
            'assistance_request': assistance_request,
            'images': images,
            'support_types': support_types,
            'success_message': "Updated successfully!",
        })

    return render(request, "admin/assistance-request-detail.html", {
        'assistance_request': assistance_request,
        'images': images,
        'support_types': support_types,
    })

@role_required('admin')
def accepted_assistance_request(request):
    # per_page = request.GET.get('entries', 'all')

    # assistance_requests = AssistanceRequest.objects.filter(status='approved').order_by('-created_at')

    # if per_page == 'all':
    #     page_obj = assistance_requests
    #     is_paginated = False
    # else:
    #     try:
    #         per_page_int = int(per_page)  # để vẫn giữ `per_page` là str, nhưng dùng int để phân trang
    #     except ValueError:
    #         per_page_int = 10
    #         per_page = '10'

    #     paginator = Paginator(assistance_requests, per_page_int)
    #     page_number = request.GET.get('page', 1)
    #     page_obj = paginator.get_page(page_number)
    #     is_paginated = page_obj.has_other_pages()

    # context = {
    #     'page_obj': page_obj,
    #     'per_page': per_page,  # luôn là string: '10', '20', 'all'
    #     'is_paginated': is_paginated,
    #     'total_count': assistance_requests.count(),
    # }
    per_page = request.GET.get('entries', 'all')
   
    assistance_requests = AssistanceRequest.objects.filter(status='approved').order_by('-created_at')
    
    
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
    return render(request, 'admin/accepted-assistance-request.html', context)
    

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