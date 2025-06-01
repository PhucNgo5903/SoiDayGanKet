from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Beneficiary, NguoiDung, Event, AssistanceRequestTypeMap, AssistanceRequestImage, AssistanceRequest
from .views import role_required
from django.contrib import messages
from ..forms import AssistanceRequestForm, AssistanceRequestTypeForm, AssistanceRequestImageForm, BeneficiaryProfileForm
from django.utils.translation import gettext as _ 
from django.views.decorators.http import require_POST
from django.db.models import Q, Exists, OuterRef
from django.core.files.storage import FileSystemStorage
import uuid

@role_required('beneficiary')
def index_beneficiary(request):
    return render(request, 'beneficiary/index-beneficiary.html')

@role_required('beneficiary')
def send_request(request):
    request_form = AssistanceRequestForm()
    type_form = AssistanceRequestTypeForm()
    image_form = AssistanceRequestImageForm()

    if request.method == 'POST':
        request_form = AssistanceRequestForm(request.POST)
        type_form = AssistanceRequestTypeForm(request.POST)
        image_form = AssistanceRequestImageForm(request.POST, request.FILES)

        if request_form.is_valid() and type_form.is_valid() and image_form.is_valid():
            start_date = request_form.cleaned_data.get('start_date')
            end_date = request_form.cleaned_data.get('end_date')

            if start_date and end_date and start_date > end_date:
                messages.error(request, "Ngày bắt đầu phải trước ngày kết thúc.")
            else:
                assistance_request = request_form.save(commit=False)
                nguoidung = NguoiDung.objects.get(user=request.user)
                beneficiary = Beneficiary.objects.get(user=nguoidung)
                assistance_request.beneficiary = beneficiary
                assistance_request.status = 'pending'
                assistance_request.receiving_status = 'waiting'
                assistance_request.save()

                for type_item in type_form.cleaned_data['types']:
                    AssistanceRequestTypeMap.objects.create(
                        assistance_request=assistance_request, type=type_item
                    )

                # Lưu ảnh
                image = image_form.cleaned_data.get('image')
                if image:
                    from django.core.files.storage import default_storage
                    import os
                    file_path = default_storage.save(os.path.join('assistance_images', image.name), image)
                    file_url = default_storage.url(file_path)

                    AssistanceRequestImage.objects.create(
                        assistance_request=assistance_request,
                        image_url=file_url
                    )
                return redirect('support_status')
        else:
            messages.error(request, "Gửi thất bại. Vui lòng kiểm tra lại thông tin.")

    return render(request, 'beneficiary/send-request.html', {
        'request_form': request_form,
        'type_form': type_form,
        'image_form': image_form,
    })

    

@role_required('beneficiary')     
def support_status(request):
    nguoi_dung = get_object_or_404(NguoiDung, user=request.user)

    if nguoi_dung.role != 'beneficiary':
        return render(request, 'error.html', {'message': 'Bạn không có quyền truy cập trang này.'})

    beneficiary = get_object_or_404(Beneficiary, user=nguoi_dung)

    q = request.GET.get('q', '')
    status = request.GET.get('status', '')
    priority = request.GET.get('priority', '')
    receive_status = request.GET.get('receive_status', '')

    # Annotate has_completed_event
    completed_event_subquery = Event.objects.filter(
        assistance_request=OuterRef('pk'),
        status='completed'
    )

    assistance_requests = AssistanceRequest.objects.filter(
        beneficiary=beneficiary
    ).annotate(
        has_completed_event=Exists(completed_event_subquery)
    )

    if q:
        assistance_requests = assistance_requests.filter(
            Q(title__icontains=q) |
            Q(place__icontains=q)
        )

    if status:
        assistance_requests = assistance_requests.filter(status=status)

    if priority:
        assistance_requests = assistance_requests.filter(priority=priority)

    # if receive_status:
    #     assistance_requests = assistance_requests.filter(receiving_status=receive_status)
    if receive_status == 'N/A':
        assistance_requests = assistance_requests.filter(receiving_status__isnull=True)
    elif receive_status:
        assistance_requests = assistance_requests.filter(receiving_status=receive_status)
        assistance_requests = assistance_requests.order_by('-created_at')

    context = {
        'assistance_requests': assistance_requests,
    }
    return render(request, 'beneficiary/support-status.html', context)

@role_required('beneficiary')
def update_user_status(request, request_id):
    nguoi_dung = get_object_or_404(NguoiDung, user=request.user)
    beneficiary = get_object_or_404(Beneficiary, user=nguoi_dung)
    assistance_request = get_object_or_404(AssistanceRequest, id=request_id)

    # Kiểm tra request có thuộc beneficiary này không
    if assistance_request.beneficiary != beneficiary:
        return render(request, 'error.html', {'message': 'Bạn không có quyền thay đổi yêu cầu này.'})

    if request.method == "POST":
        new_status = request.POST.get("receiving_status")

        # Logic mới theo yêu cầu
        if assistance_request.status in ['pending', 'rejected']:
            # Pending/Rejected => receiving_status = NULL (không cho phép thay đổi)
            assistance_request.receiving_status = None
            
        elif assistance_request.status == 'approved':
            # Kiểm tra có event hoàn thành không
            has_completed_event = Event.objects.filter(
                assistance_request=assistance_request,
                status='completed'
            ).exists()
            
            if has_completed_event:
                # Approved + có event completed => cho phép chọn waiting/received
                if new_status in ['waiting', 'received']:
                    assistance_request.receiving_status = new_status
                else:
                    assistance_request.receiving_status = 'waiting'  # default
            else:
                # Approved + chưa có event completed => fix cứng là waiting
                assistance_request.receiving_status = 'waiting'

        assistance_request.save()
    
    return redirect(request.META.get('HTTP_REFERER'))

@role_required('beneficiary')    
def assistance_request_detail(request, pk):
    rq = get_object_or_404(AssistanceRequest, pk=pk)
    return render(request, 'beneficiary/assistance-request-detail.html', {'request_item': rq})

@role_required('beneficiary')    
def edit_beneficiary_profile(request):
    # Kiểm tra và lấy thông tin người dùng
    if not hasattr(request.user, 'nguoidung'):
        messages.error(request, "User profile not found")
        return redirect('home')  # hoặc trang nào đó phù hợp
    
    nguoidung = request.user.nguoidung
    
    if request.method == 'POST':
        form = BeneficiaryProfileForm(request.POST, instance=nguoidung, user=request.user)
        if form.is_valid():
            # Lưu thông tin người dùng (NguoiDung)
            nguoidung = form.save(commit=True)
            
            if 'avatar_file' in request.FILES:
                avatar_file = request.FILES['avatar_file']
                if avatar_file.content_type.startswith('image/'):
                    fs = FileSystemStorage()
                    ext = avatar_file.name.split('.')[-1]
                    filename = fs.save(f"avatars/{request.user.username}_{uuid.uuid4()}.{ext}", avatar_file)
                    nguoidung.avatar_url = fs.url(filename)

            nguoidung.save()
            # Cập nhật thông tin User liên quan
            user = request.user
            user.first_name = form.cleaned_data.get('first_name', '')
            user.last_name = form.cleaned_data.get('last_name', '')
            user.email = form.cleaned_data.get('email', '')
            user.save()
            
            messages.success(request, "Profile updated successfully!")
            return redirect('beneficiary_profile')
        else:
            messages.error(request, "Please correct the errors below")
    else:
        form = BeneficiaryProfileForm(instance=nguoidung, user=request.user)
    
    return render(request, 'beneficiary/beneficiary_profile_edit.html', {'form': form})