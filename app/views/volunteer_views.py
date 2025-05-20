from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .views import role_required
from app.models import Event


@role_required('volunteer')
def volunteer_home(request):
    completed_events = Event.objects.filter(
        status='completed'
    ).order_by('-end_time')[:6]  # lấy tối đa 6 sự kiện đã hoàn thành gần nhất

    return render(request, 'volunteer/home-volunteer.html', {
        'completed_events': completed_events
    })

@role_required('volunteer')
def volunteer_events(request):
    return render(request, 'volunteer/events-volunteer.html')

@role_required('volunteer')
def volunteer_statistics(request):
    return render(request, 'volunteer/statistics-volunteer.html')

@role_required('volunteer')
def volunteer_profile(request):
    return render(request, 'volunteer/profile-volunteer.html')

def logout_view(request):
    logout(request)
    return redirect('login_volunteer')
