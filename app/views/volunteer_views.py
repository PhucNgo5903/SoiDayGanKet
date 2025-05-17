from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .views import role_required

@role_required('volunteer')
def index_volunteer(request):
    return render(request, 'volunteer/index-volunteer.html')