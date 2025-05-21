from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .views import role_required
from app.models import Event, Volunteer, EventRegistration
from django.utils import timezone
from django.shortcuts import redirect
from app.forms import EventRegisterForm
from django.views.decorators.http import require_http_methods
from django.views.decorators.http import require_POST
from django.contrib import messages

@role_required('volunteer')
def volunteer_home(request):
    now = timezone.now()

    # Chỉ lấy các sự kiện đã kết thúc (diễn ra trong quá khứ)
    completed_events = Event.objects.filter(
        end_time__lt=now
    ).order_by('-end_time')[:6]

    volunteers = Volunteer.objects.select_related('user__user').all()

    return render(request, 'volunteer/home-volunteer.html', {
        'completed_events': completed_events,
        'volunteers': volunteers  
    })

@role_required('volunteer')
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    volunteer = request.user.nguoidung.volunteer

    registration = EventRegistration.objects.filter(
        event=event,
        volunteer=volunteer
    ).first()

    return render(request, 'volunteer/event_detail.html', {
        'event': event,
        'registration': registration
    })
@role_required('volunteer')
def volunteer_events(request):
    now = timezone.now()
    events = Event.objects.filter(start_time__gt=now).order_by('start_time')
    return render(request, 'volunteer/events-volunteer.html', {'events': events})
@role_required('volunteer')
@require_http_methods(["GET", "POST"])
def register_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    volunteer = get_object_or_404(Volunteer, user=request.user.nguoidung)

    # Kiểm tra nếu đã đăng ký rồi
    registration = EventRegistration.objects.filter(event=event, volunteer=volunteer).first()
    if registration:
        messages.warning(request, "Bạn đã đăng ký sự kiện này.")
        return redirect('event_detail', event_id=event.id)

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        skills = request.POST.get('skills')

        # (Tuỳ bạn xử lý thêm nếu cần lưu thông tin bổ sung)

        EventRegistration.objects.create(
            event=event,
            volunteer=volunteer,
            status='pending'
        )

        messages.success(request, "Đăng kí thành công! Vui lòng chờ duyệt.")
        return redirect('event_detail', event_id=event.id)

    return render(request, 'volunteer/register_event.html', {'event': event})
@role_required('volunteer')
def volunteer_statistics(request):
    return render(request, 'volunteer/statistics-volunteer.html')

@role_required('volunteer')
def volunteer_profile(request):
    return render(request, 'volunteer/profile-volunteer.html')

def logout_view(request):
    logout(request)
    return redirect('login_volunteer')
