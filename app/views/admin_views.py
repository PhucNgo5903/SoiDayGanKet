from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .views import role_required
from ..models import Event, EventRegistration
from django.db.models import Count, Q, F,Subquery, OuterRef # Cho tìm kiếm nâng cao
from django.core.paginator import Paginator, PageNotAnInteger,EmptyPage

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


def new_event_request(request):
    events = Event.objects.filter(status='pending').select_related('charity_org')
    # Xử lý tìm kiếm
    search_query = request.GET.get('q', '')
    
    if search_query:
        events = events.filter(
            Q(title__icontains=search_query) |
            Q(charity_org__user__user__first_name__icontains=search_query) |
            Q(charity_org__user__user__last_name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    
    # Sắp xếp kết quả (ví dụ theo ngày bắt đầu giảm dần)
    events = events.order_by('-start_time')
    
    # Phân trang - 10 items mỗi trang
    paginator = Paginator(events, 10)
    page_number = request.GET.get('page')
    
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    context = {
        'events': page_obj,
        'search_query': search_query,
    }
    return render(request, "admin/new-event-request.html", context)

def event_request_detail(request):
    return render(request, "admin/event-request-detail.html")

def approved_event(request):
    events = Event.objects.filter(status='approved').select_related('charity_org')
    
    # Xử lý tìm kiếm
    search_query = request.GET.get('q', '')
    
    if search_query:
        events = events.filter(
            Q(title__icontains=search_query) |
            Q(charity_org__user__user__first_name__icontains=search_query) |
            Q(charity_org__user__user__last_name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    
    # Sắp xếp kết quả (ví dụ theo ngày bắt đầu giảm dần)
    events = events.order_by('-start_time')
    
    # Phân trang - 10 items mỗi trang
    paginator = Paginator(events, 10)
    page_number = request.GET.get('page')
    
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    context = {
        'events': page_obj,
        'search_query': search_query,
    }
    
    return render(request, "admin/approved-event.html", context)

def rejected_event_request(request):
    events = Event.objects.filter(status='rejected').select_related('charity_org')
    # Xử lý tìm kiếm
    search_query = request.GET.get('q', '')
    
    if search_query:
        events = events.filter(
            Q(title__icontains=search_query) |
            Q(charity_org__user__user__first_name__icontains=search_query) |
            Q(charity_org__user__user__last_name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    
    # Sắp xếp kết quả (ví dụ theo ngày bắt đầu giảm dần)
    events = events.order_by('-start_time')
    
    # Phân trang - 10 items mỗi trang
    paginator = Paginator(events, 10)
    page_number = request.GET.get('page')
    
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    context = {
        'events': page_obj,
        'search_query': search_query,
    }
    return render(request, "admin/rejected-event-request.html", context)

def full_volunteer_event(request):
    approved_counts = EventRegistration.objects.filter(
    event=OuterRef('pk'),
    status='approved'
    ).values('event').annotate(
    cnt=Count('id')
    ).values('cnt')

    full_events = Event.objects.annotate(
    approved_volunteers=Subquery(approved_counts)
    ).filter(
    approved_volunteers__gte=F('volunteers_number'),
    status='approved'
    ).order_by('-start_time')
    # Xử lý tìm kiếm
    search_query = request.GET.get('q', '')
    if search_query:
        full_events = full_events.filter(
            Q(title__icontains=search_query) |
            Q(charity_org__user__user__first_name__icontains=search_query) |
            Q(charity_org__user__user__last_name__icontains=search_query)
        )

    # Phân trang
    paginator = Paginator(full_events, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'events': page_obj,
        'search_query': search_query,
    }
    return render(request, 'admin/full-volunteer-event.html', context)

def completed_event(request):
    events = Event.objects.filter(status='completed').select_related('charity_org')
    # Xử lý tìm kiếm
    search_query = request.GET.get('q', '')
    
    if search_query:
        events = events.filter(
            Q(title__icontains=search_query) |
            Q(charity_org__user__user__first_name__icontains=search_query) |
            Q(charity_org__user__user__last_name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    
    # Sắp xếp kết quả (ví dụ theo ngày bắt đầu giảm dần)
    events = events.order_by('-start_time')
    
    # Phân trang - 10 items mỗi trang
    paginator = Paginator(events, 10)
    page_number = request.GET.get('page')
    
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    context = {
        'events': page_obj,
        'search_query': search_query,
    }
    return render(request, "admin/completed-event.html", context)

def all_event(request):
    # Lấy tất cả sự kiện đã hoàn thành (hoặc theo điều kiện của bạn)
    events = Event.objects.all()
    
    # Xử lý tìm kiếm
    search_query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    
    if search_query:
        events = events.filter(
            Q(title__icontains=search_query) |
            Q(charity_org__user__user__first_name__icontains=search_query) |
            Q(charity_org__user__user__last_name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Lọc theo trạng thái nếu có
    if status_filter:
        events = events.filter(status=status_filter)
    
    # Sắp xếp kết quả (ví dụ theo ngày bắt đầu giảm dần)
    events = events.order_by('-start_time')
    
    # Phân trang - 10 items mỗi trang
    paginator = Paginator(events, 10)
    page_number = request.GET.get('page')
    
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    context = {
        'events': page_obj,
        'search_query': search_query,
    }
    
    return render(request, 'admin/all-event.html', context)
