from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .views import role_required
from app.models import (
    Event, Volunteer, EventRegistration, Skill, VolunteerSkill,
    NguoiDung, AssistanceRequestTypeMap, SkillAssistanceRequestType
)
from django.utils import timezone
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib import messages
from django.utils.timezone import now
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import logout
from django.db.models import Q
import uuid


# ==== Sidebar context ====
def volunteer_sidebar_info(request):
    if request.user.is_authenticated:
        try:
            nguoidung = NguoiDung.objects.select_related('user').get(user=request.user)
            return {
                'avatar_url': nguoidung.avatar_url,
                'username': nguoidung.user.username,
                'email': nguoidung.user.email
            }
        except NguoiDung.DoesNotExist:
            return {}
    return {}

# ==== Trang chủ ====
@role_required('volunteer')
def volunteer_home(request):
    now_time = timezone.now()
    completed_events = Event.objects.filter(end_time__lt=now_time).order_by('-end_time')[:6]
    volunteers = Volunteer.objects.select_related('user__user').all()
    return render(request, 'volunteer/home-volunteer.html', {
        'completed_events': completed_events,
        'volunteers': volunteers
    })

# ==== Chi tiết sự kiện ====
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    volunteer = request.user.nguoidung.volunteer
    registration = EventRegistration.objects.filter(event=event, volunteer=volunteer).first()
    approved_count = EventRegistration.objects.filter(event=event, status='approved').count()
    is_full = approved_count >= event.volunteers_number

    source_page = request.GET.get('from', '')
    if source_page == 'home':
        back_url = reverse('volunteer_home')
    elif source_page == 'registered':
        back_url = reverse('volunteer_registered_events')
    else:
        back_url = reverse('volunteer_events')

    context = {
        'event': event,
        'registration': registration,
        'event_has_ended': event.end_time < now(),
        'approved_count': approved_count,
        'is_full': is_full,
        'back_url': back_url,
    }
    return render(request, 'volunteer/event_detail.html', context)

# ==== Sự kiện chưa đăng ký (lọc theo kỹ năng) ====
@role_required('volunteer')
def volunteer_events(request):
    volunteer = get_object_or_404(Volunteer, user=request.user.nguoidung)
    now_time = timezone.now()
    skills = Skill.objects.filter(volunteerskill__volunteer=volunteer)
    registered_ids = EventRegistration.objects.filter(volunteer=volunteer).values_list('event_id', flat=True)
    query = request.GET.get('q', '')

    events = Event.objects.filter(
        start_time__gt=now_time,
        status='approved',
        assistance_request__assistancerequesttypemap__type__skillassistancerequesttype__skill__in=skills
    ).exclude(id__in=registered_ids).distinct()

    if query:
        events = events.filter(
            Q(title__icontains=query) |
            Q(assistance_request__place__icontains=query)
        )

    events = events.order_by('start_time')

    return render(request, 'volunteer/events-volunteer.html', {
        'events': events,
        'registered': False,
        'query': query
    })

# ==== Sự kiện đã đăng ký (chờ duyệt hoặc bị từ chối) ====
@role_required('volunteer')
def volunteer_registered_events(request):
    volunteer = get_object_or_404(Volunteer, user=request.user.nguoidung)
    query = request.GET.get('q', '')

    registrations = EventRegistration.objects.filter(
        volunteer=volunteer,
        status__in=['pending', 'rejected']
    )
    events = Event.objects.filter(
        id__in=registrations.values_list('event_id', flat=True)
    )

    if query:
        events = events.filter(
            Q(title__icontains=query) |
            Q(assistance_request__place__icontains=query)
        )

    events = events.order_by('-start_time')

    return render(request, 'volunteer/events-volunteer.html', {
        'events': events,
        'registered': True,
        'query': query
    })

# ==== Sự kiện đang tham gia (approved) ====
@role_required('volunteer')
def volunteer_ongoing_events(request):
    volunteer = get_object_or_404(Volunteer, user=request.user.nguoidung)

    ongoing_regs = EventRegistration.objects.filter(
        volunteer=volunteer,
        status='approved',
        event__end_time__gt=timezone.now()
    ).select_related('event')

    events = [reg.event for reg in ongoing_regs]
    query = request.GET.get('q', '')

    if query:
        events = [e for e in events if query.lower() in e.title.lower() or query.lower() in (e.assistance_request.place if e.assistance_request else '').lower()]

    return render(request, 'volunteer/events-volunteer.html', {
        'events': events,
        'registered': True,
        'query': query,
        'ongoing': True
    })

# ==== Đăng ký sự kiện ====
@role_required('volunteer')
@require_POST
def register_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    volunteer = get_object_or_404(Volunteer, user=request.user.nguoidung)

    if EventRegistration.objects.filter(event=event, volunteer=volunteer).exists():
        messages.warning(request, "Bạn đã đăng ký sự kiện này.")
        return redirect('volunteer_event_detail', event_id=event.id)

    EventRegistration.objects.create(event=event, volunteer=volunteer, status='pending')
    messages.success(request, "Đăng ký thành công! Vui lòng chờ duyệt.")
    return redirect('volunteer_event_detail', event_id=event.id)

# ==== Thống kê sự kiện đã tham gia ====
@role_required('volunteer')
def volunteer_statistics(request):
    volunteer = get_object_or_404(Volunteer, user=request.user.nguoidung)
    completed_regs = EventRegistration.objects.filter(volunteer=volunteer, status='completed').select_related('event', 'event__assistance_request')
    completed_events = [reg.event for reg in completed_regs]
    return render(request, 'volunteer/statistics-volunteer.html', {
        'completed_events': completed_events,
        'completed_count': len(completed_events),
    })

# ==== Trang hồ sơ ====
@role_required('volunteer')
def volunteer_profile(request):
    volunteer = get_object_or_404(Volunteer, user=request.user.nguoidung)
    nguoidung = volunteer.user
    user = nguoidung.user
    all_skills = Skill.objects.all()
    selected_skills = Skill.objects.filter(volunteerskill__volunteer=volunteer)

    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()

        nguoidung.dob = request.POST.get('dob')
        nguoidung.phone = request.POST.get('phone')
        nguoidung.address = request.POST.get('address')
        nguoidung.description = request.POST.get('description')

        if 'avatar_file' in request.FILES:
            avatar_file = request.FILES['avatar_file']
            if avatar_file.content_type.startswith('image/'):
                fs = FileSystemStorage()
                ext = avatar_file.name.split('.')[-1]
                filename = fs.save(f"avatars/{user.username}_{uuid.uuid4()}.{ext}", avatar_file)
                nguoidung.avatar_url = fs.url(filename)

        nguoidung.save()

        volunteer.gender = request.POST.get('gender')
        volunteer.save()

        selected_ids = request.POST.getlist('skills')
        VolunteerSkill.objects.filter(volunteer=volunteer).delete()
        for skill_id in selected_ids:
            skill = get_object_or_404(Skill, id=skill_id)
            VolunteerSkill.objects.create(volunteer=volunteer, skill=skill)

        messages.success(request, "Profile updated successfully!")

    return render(request, 'volunteer/profile-volunteer.html', {
        'user': user,
        'nguoidung': nguoidung,
        'volunteer': volunteer,
        'all_skills': all_skills,
        'selected_skills': selected_skills
    })

# ==== Context processor phụ ====
def volunteer_context(request):
    if request.user.is_authenticated and hasattr(request.user, 'nguoidung'):
        try:
            return {
                'volunteer': request.user.nguoidung.volunteer
            }
        except Volunteer.DoesNotExist:
            return {}
    return {}

# ==== Logout ====
def logout_view(request):
    logout(request)
    return redirect('login_volunteer')
