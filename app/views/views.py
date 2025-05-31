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
from django.core.paginator import Paginator
from django.db.models import Count, Q
from ..models import AssistanceRequest, Event, Beneficiary

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

def gallery_view(request):
    """
    View để hiển thị gallery các yêu cầu hỗ trợ đã hoàn thành
    """
    # Query các yêu cầu đã hoàn thành (approved và received)
    completed_requests = AssistanceRequest.objects.filter(
        status='approved',
        receiving_status='received'
    ).select_related(
        'beneficiary__user__user',
        'charity_org__user__user',
        'update_by__user'
    ).prefetch_related(
        'images',
        'assistancerequesttypemap_set__type'
    ).order_by('-update_status_at')

    # Lọc theo tham số từ URL (nếu có)
    search_query = request.GET.get('search', '')
    priority_filter = request.GET.get('priority', '')

    if search_query:
        completed_requests = completed_requests.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )

    if priority_filter:
        completed_requests = completed_requests.filter(priority=priority_filter)

    # Phân trang
    paginator = Paginator(completed_requests, 12)  # 12 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Thống kê
    total_completed = AssistanceRequest.objects.filter(
        status='approved',
        receiving_status='received'
    ).count()

    total_beneficiaries = Beneficiary.objects.filter(
        assistancerequest__status='approved',
        assistancerequest__receiving_status='received'
    ).distinct().count()

    total_events = Event.objects.filter(
        status='completed'
    ).count()

    context = {
        'completed_requests': page_obj,
        'total_completed': total_completed,
        'total_beneficiaries': total_beneficiaries,
        'total_events': total_events,
        'has_more': page_obj.has_next(),
        'search_query': search_query,
        'priority_filter': priority_filter,
    }

    return render(request, 'gallery.html', context)


def gallery_api_view(request):
    """
    API endpoint để load thêm dữ liệu (AJAX)
    """
    from django.http import JsonResponse
    from django.template.loader import render_to_string
    
    page = request.GET.get('page', 1)
    search_query = request.GET.get('search', '')
    priority_filter = request.GET.get('priority', '')

    completed_requests = AssistanceRequest.objects.filter(
        status='approved',
        receiving_status='received'
    ).select_related(
        'beneficiary__user__user',
        'charity_org__user__user'
    ).prefetch_related(
        'images',
        'assistancerequesttypemap_set__type'
    ).order_by('-update_status_at')

    if search_query:
        completed_requests = completed_requests.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )

    if priority_filter:
        completed_requests = completed_requests.filter(priority=priority_filter)

    paginator = Paginator(completed_requests, 12)
    page_obj = paginator.get_page(page)

    # Render HTML for the new items
    html = render_to_string('gallery_items.html', {
        'completed_requests': page_obj
    })

    return JsonResponse({
        'html': html,
        'has_more': page_obj.has_next(),
        'page': page_obj.number,
        'total_pages': paginator.num_pages
    })