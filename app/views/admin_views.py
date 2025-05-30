
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from app import models
from app.models import AssistanceRequest, AssistanceRequestImage, AssistanceRequestType, AssistanceRequestTypeMap, CharityOrg, Event, EventRegistration, Volunteer, VolunteerSkill
from .views import role_required
from django.core.paginator import Paginator
from django.utils import timezone   
from django.db.models import Count, Sum, ExpressionWrapper, DurationField, F
from django.utils.timezone import now
from django.db.models import Q

@role_required('admin')
def index_admin(request):
    total_charity_orgs = models.CharityOrg.objects.count()
    total_volunteers = models.Volunteer.objects.count()
    total_pending_requests = models.AssistanceRequest.objects.filter(status='pending').count()
    total_accepted_requests = models.AssistanceRequest.objects.filter(status='approved').count()

    context = {
        'total_charity_orgs': total_charity_orgs,
        'total_volunteers': total_volunteers,
        'total_pending_requests': total_pending_requests,
        'total_accepted_requests': total_accepted_requests,
    }
    return render(request, "admin/index-admin.html", context)

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
    per_page = request.GET.get('entries', 'all')
   
    assistance_requests = AssistanceRequest.objects.filter(status='approved').order_by('-update_status_at')
    
    
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
def rejected_assistance_request(request):
        per_page = request.GET.get('entries', 'all')
        assistance_requests = AssistanceRequest.objects.filter(status='rejected').order_by('-update_status_at')
        
        
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
        return render(request, 'admin/rejected-assistance-request.html', context)



@role_required('admin')
def total_volunteer(request):
    current_time = now()
    start_of_month = current_time.replace(day=1)

    time_spent = ExpressionWrapper(
        F('checked_out_at') - F('checked_in_at'),
        output_field=DurationField()
    )

    def get_top_volunteers(queryset):
        results = []
        for stat in queryset:
            volunteer = Volunteer.objects.select_related('user__user').get(user_id=stat['volunteer'])
            nguoidung = volunteer.user  # liên kết đến NguoiDung
            results.append({
                'volunteer': volunteer,
                'name': f"{nguoidung.user.first_name} {nguoidung.user.last_name}".strip() or nguoidung.user.username,
                'username': nguoidung.user.username,
                'user_id': nguoidung.user.id,
                'avatar_url': nguoidung.avatar_url,
                'total_events': stat['total_events'],
                'total_hours': round(stat['total_hours'].total_seconds() / 3600),
            })
        return results

    # Top 3 tình nguyện viên hoạt động nhất mọi thời gian
    all_time_top = (
        EventRegistration.objects
        .filter(status='completed', checked_in_at__isnull=False, checked_out_at__isnull=False)
        .annotate(duration=time_spent)
        .values('volunteer')
        .annotate(
            total_events=Count('id'),
            total_hours=Sum('duration')
        )
        .order_by('-total_events', '-total_hours')[:3]
    )
    top_all_time_volunteers = get_top_volunteers(all_time_top)

    # Top 3 tình nguyện viên hoạt động nhiều nhất trong tháng
    month_top = (
        EventRegistration.objects
        .filter(
            status='completed',
            checked_in_at__gte=start_of_month,
            checked_out_at__isnull=False,
            checked_in_at__isnull=False
        )
        .annotate(duration=time_spent)
        .values('volunteer')
        .annotate(
            total_events=Count('id'),
            total_hours=Sum('duration')
        )
        .order_by('-total_events', '-total_hours')[:3]
    )
    top_month_volunteers = get_top_volunteers(month_top)

    # Danh sách tất cả tình nguyện viên + trạng thái hoạt động
    search_query = request.GET.get('search', '').strip()

    volunteers = Volunteer.objects.select_related('user__user')

    if search_query:
        volunteers = volunteers.filter(
            Q(user__user__first_name__icontains=search_query) |
            Q(user__user__last_name__icontains=search_query) |
            Q(user__user__username__icontains=search_query)
        )

    volunteer_data = []
    for v in volunteers:
        nguoidung = v.user

        has_approved_event = EventRegistration.objects.filter(
            volunteer=v,
            status='approved'
        ).exists()

        latest_registration = (
            EventRegistration.objects
            .filter(volunteer=v, status='approved')
            .order_by('-event__start_time')
            .first()
        )
    

        volunteer_data.append({
            'pk': v.pk,
            'id': nguoidung.user.id,
            'avatar_url': nguoidung.avatar_url, 
            'full_name': f"{nguoidung.user.first_name} {nguoidung.user.last_name}".strip() or nguoidung.user.username,
            'username': nguoidung.user.username,
            'status': 'Active' if has_approved_event else 'Inactive',
            'event_name': latest_registration.event.title if latest_registration else '--',
            'org_name': latest_registration.event.charity_org.user.user.username if latest_registration else '--',
        })
    context = {
        'top_all_time': top_all_time_volunteers,
        'top_month': top_month_volunteers,
        'volunteer_data': volunteer_data,
    }

    return render(request, 'admin/total_volunteer.html', context)


@login_required
@role_required('admin')
def admin_volunteer_detail(request, pk):
    # Lấy volunteer theo pk
    volunteer = get_object_or_404(Volunteer, pk=pk)

    # Thông tin user liên quan
    nguoidung = volunteer.user  # NguoiDung instance
    user = nguoidung.user       # Django User instance

    # Kỹ năng của volunteer
    skills = VolunteerSkill.objects.filter(volunteer=volunteer).select_related('skill')

    # Các sự kiện volunteer đã tham gia với status 'completed' và có check-in/out
    event_regs = (
        EventRegistration.objects
        .filter(
            volunteer=volunteer,
            status='completed',
            checked_in_at__isnull=False,
            checked_out_at__isnull=False
        )
        .annotate(
            duration=ExpressionWrapper(
                F('checked_out_at') - F('checked_in_at'),
                output_field=DurationField()
            )
        )
        .select_related('event')
    )

    # Tổng số sự kiện đã tham gia
    total_events = event_regs.count()

    # Tổng thời gian đã tham gia (tính bằng giờ)
    total_duration = event_regs.aggregate(total=Sum('duration'))['total']
    total_hours = round(total_duration.total_seconds() / 3600, 2) if total_duration else 0

    context = {
        'volunteer': volunteer,
        'nguoidung': nguoidung,
        'user': user,
        'skills': [vs.skill for vs in skills],
        'event_regs': event_regs,
        'total_events': total_events,
        'total_hours': total_hours,
    }
    return render(request, "admin/admin-volunteer-detail.html", context)



@role_required('admin')
def total_charity_orgs(request):
    current_time = now()
    start_of_month = current_time.replace(day=1)

    def get_top_charities(queryset):
        results = []
        for stat in queryset:
            charity = CharityOrg.objects.select_related('user__user').get(pk=stat['charity_org'])
            user = charity.user
            results.append({
                'charity_org': charity,
                'name': f"{user.user.first_name} {user.user.last_name}".strip() or user.user.username,
                'username': user.user.username,
                'user_id': user.user.id,
                'avatar_url': user.avatar_url,
                'total_events': stat['total_events'],
            })
        return results

    # Top 3 hội thiện nguyện mọi thời đại (dựa vào bảng Event)
    all_time_top = (
        Event.objects
        .filter(status='completed')
        .values('charity_org')
        .annotate(total_events=Count('id'))
        .order_by('-total_events')[:3]
    )
    top_all_time = get_top_charities(all_time_top)

    # Top 3 hội thiện nguyện trong tháng này
    month_top = (
        Event.objects
        .filter(status='completed', start_time__gte=start_of_month)
        .values('charity_org')
        .annotate(total_events=Count('id'))
        .order_by('-total_events')[:3]
    )
    top_month = get_top_charities(month_top)

    # Danh sách tất cả hội thiện nguyện với tổng số sự kiện completed
    all_charities = CharityOrg.objects.select_related('user__user').all()
    charity_data = []
    for c in all_charities:
        user = c.user

        num_completed_events = Event.objects.filter(
            charity_org=c,
            status='completed'
        ).count()

        charity_data.append({
            'pk': c.pk,
            'avatar_url': user.avatar_url,
            'name': f"{user.user.first_name} {user.user.last_name}".strip() or user.user.username,
            'username': user.user.username,
            'total_completed_events': num_completed_events,
        })

    # Sắp xếp theo số sự kiện hoàn thành giảm dần
    charity_data.sort(key=lambda x: x['total_completed_events'], reverse=True)

    context = {
        'top_all_time': top_all_time,
        'top_month': top_month,
        'charity_data': charity_data,
    }

    return render(request, 'admin/total_charity_orgs.html', context)


@login_required
@role_required('admin')
def admin_charity_org_detail(request, pk):
    # Lấy CharityOrg theo pk
    charity_org = get_object_or_404(CharityOrg, pk=pk)

    # Lấy thông tin liên quan
    nguoidung = charity_org.user  # NguoiDung instance
    user = nguoidung.user         # Django User instance

    # Các lĩnh vực hỗ trợ đã đăng ký
    support_types = (
        AssistanceRequestType.objects
        .filter(charityorgassistancerequesttype__charity_org=charity_org)
        .distinct()
    )

    # Danh sách các sự kiện đã hoàn thành
    completed_events = (
        Event.objects
        .filter(charity_org=charity_org, status='completed')
        .order_by('-start_time')
    )

    context = {
        'charity_org': charity_org,
        'nguoidung': nguoidung,
        'user': user,
        'support_types': support_types,
        'completed_events': completed_events,
    }

    return render(request, "admin/admin-charity-org-detail.html", context)