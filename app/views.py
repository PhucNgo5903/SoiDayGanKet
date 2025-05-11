

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import (
    LoginForm, 
    VolunteerRegisterForm, 
    BeneficiaryRegisterForm, 
    CharityOrgRegisterForm
)
from .models import NguoiDung

# ==== Decorator kiểm tra role ====
def role_required(required_role):
    def decorator(view_func):
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if hasattr(request.user, 'nguoidung') and request.user.nguoidung.role.lower() == required_role.lower():
                return view_func(request, *args, **kwargs)
            return redirect('login_' + required_role.lower())
        return _wrapped_view
    return decorator


# ==== Volunteer Views ====
class login_volunteer(View):
    def get(self, request):
        return render(request, 'login-volunteer.html', {'form': LoginForm()})

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('index_volunteer')
        return render(request, 'login-volunteer.html', {'form': form})


class signup_volunteer(View):
    def get(self, request):
        return render(request, 'signup_volunteer.html', {'form': VolunteerRegisterForm()})

    def post(self, request):
        form = VolunteerRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_volunteer')
        return render(request, 'signup_volunteer.html', {'form': form})


# ==== Beneficiary Views ====
class login_beneficiary(View):
    def get(self, request):
        return render(request, 'login-beneficiary.html', {'form': LoginForm()})

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('index_beneficiary')
        return render(request, 'login-beneficiary.html', {'form': form})


class signup_beneficiary(View):
    def get(self, request):
        return render(request, 'signup_beneficiary.html', {'form': BeneficiaryRegisterForm()})

    def post(self, request):
        form = BeneficiaryRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_beneficiary')
        return render(request, 'signup_beneficiary.html', {'form': form})


# ==== Charity Org Views ====
class login_charity_org(View):
    def get(self, request):
        return render(request, 'login-charity.html', {'form': LoginForm()})

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('index_charity')
        return render(request, 'login-charity.html', {'form': form})


class signup_charity_org(View):
    def get(self, request):
        return render(request, 'signup_charity.html', {'form': CharityOrgRegisterForm()})

    def post(self, request):
        form = CharityOrgRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_charity')
        return render(request, 'signup_charity.html', {'form': form})


# ==== Index Views từng vai trò ====
@role_required('volunteer')
def index_volunteer(request):
    return render(request, 'index-volunteer.html')


@role_required('beneficiary')
def index_beneficiary(request):
    return render(request, 'index-beneficiary.html')


@role_required('charity')
def index_charity_org(request):
    return render(request, 'index-charity.html')


# ==== Trang admin login giữ nguyên ====
def login_admin(request):
    return render(request, 'login-admin.html')


# ==== Trang chủ ====
def index(request):
    return render(request, 'index.html')


# ==== Trang thư viện ảnh ====
def gallery(request):
    return render(request, 'gallery.html')

def index_admin(request):
    return render(request, "index-admin.html")

def new_assistance_request(request):
    return render(request, "new-assistance-request.html")

def assistance_request_detail(request):
    return render(request, "assistance-request-detail.html")

def accepted_assistance_request(request):
    return render(request, "accepted-assistance-request.html")

def status_updated_request_detail(request):
    return render(request, "status-updated-request-detail.html")

def rejected_assistance_request(request):
    return render(request, "rejected-assistance-request.html")

def total_volunteer(request):
    return render(request, "total_volunteer.html")

def admin_volunteer_detail(request):
    return render(request, "admin-volunteer-detail.html")

def new_event_request(request):
    return render(request, "new-event-request.html")