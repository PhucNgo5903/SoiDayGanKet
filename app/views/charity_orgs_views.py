from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .views import role_required

@role_required('charity')
def index_charity_org(request):
    return render(request, 'charity-orgs/index-charity.html')