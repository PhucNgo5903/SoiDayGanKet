from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .views import role_required


@role_required('beneficiary')
def index_beneficiary(request):
    return render(request, 'beneficiary/index-beneficiary.html')