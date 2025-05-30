from datetime import date
from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decouple import config
from ..models import NguoiDung
from django.contrib.auth.models import User

from ..forms import (
    LoginForm, 
    VolunteerRegisterForm, 
    BeneficiaryRegisterForm, 
    CharityOrgRegisterForm
)
from ..models import NguoiDung

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


def index(request):
    return render(request, 'share/index.html')


def gallery(request):
    return render(request, 'share/gallery.html')

# ==== Volunteer Views ====
class login_volunteer(View):
    def get(self, request):
        return render(request, 'share/login-volunteer.html', {'form': LoginForm()})

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('index_volunteer')
        return render(request, 'share/login-volunteer.html', {'form': form})


class signup_volunteer(View):
    def get(self, request):
        return render(request, 'share/signup_volunteer.html', {'form': VolunteerRegisterForm()})

    def post(self, request):
        form = VolunteerRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_volunteer')
        return render(request, 'share/signup_volunteer.html', {'form': form})


# ==== Beneficiary Views ====
class login_beneficiary(View):
    def get(self, request):
        return render(request, 'share/login-beneficiary.html', {'form': LoginForm()})

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('index_beneficiary')
        return render(request, 'share/login-beneficiary.html', {'form': form})


class signup_beneficiary(View):
    def get(self, request):
        return render(request, 'share/signup_beneficiary.html', {'form': BeneficiaryRegisterForm()})

    def post(self, request):
        form = BeneficiaryRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_beneficiary')
        return render(request, 'share/signup_beneficiary.html', {'form': form})


# ==== Charity Org Views ====
class login_charity_org(View):
    def get(self, request):
        return render(request, 'share/login-charity.html', {'form': LoginForm()})

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('index_charity')
        return render(request, 'share/login-charity.html', {'form': form})


class signup_charity_org(View):
    def get(self, request):
        return render(request, 'share/signup_charity.html', {'form': CharityOrgRegisterForm()})

    def post(self, request):
        form = CharityOrgRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_charity')
        return render(request, 'share/signup_charity.html', {'form': form})




# def login_admin(request):
#     return render(request, 'share/login-admin.html')




def login_admin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Lấy tài khoản admin từ .env
        admin_username = config('ADMIN_USERNAME')
        admin_password = config('ADMIN_PASSWORD')
        admin_email = config('ADMIN_EMAIL', default='admin@example.com')  

        if username == admin_username and password == admin_password:
            # Kiểm tra user đã tồn tại chưa
            user = User.objects.filter(username=admin_username).first()
            if not user:
                # Tạo mới User
                user = User.objects.create_user(
                    username=admin_username,
                    password=admin_password,
                    email=admin_email
                )
                # Tạo mới User
                user = User.objects.create_user(
                    username=admin_username,
                    password=admin_password,
                    email=admin_email
                )

                # Tạo bản ghi NguoiDung cho admin
                NguoiDung.objects.create(
                    user=user,
                    role='admin',
                    dob=date(1990, 1, 1),
                    phone='0123456789',
                    address='Trụ sở admin',
                    description='Tài khoản admin mặc định',
                    status='active'
                )

            # Xác thực và đăng nhập
            user = authenticate(username=admin_username, password=admin_password)
            if user:
                nguoidung = getattr(user, 'nguoidung', None)
                if nguoidung and nguoidung.role == 'admin':
                    login(request, user)
                    return redirect('index_admin')
                else:
                    messages.error(request, "Tài khoản không phải admin.")
            else:
                messages.error(request, "Không thể xác thực người dùng.")
        else:
            messages.error(request, "Sai thông tin đăng nhập.")

    return render(request, 'share/login-admin.html')

