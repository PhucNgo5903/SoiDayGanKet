from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .views import role_required
from app.models import AssistanceRequest, Event, NguoiDung, CharityOrg, CharityOrgAssistanceRequestType, Event, EventRegistration, AssistanceRequestType, Volunteer
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from app.forms import EventCreationForm, CharityOrgProfileForm
from django.http import JsonResponse
from django.db import transaction
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
import json


@role_required('charity')
def index_charity_org(request):
    # Lấy charity organization hiện tại
    try:
        charity_org = CharityOrg.objects.get(user__user=request.user)
    except CharityOrg.DoesNotExist:
        # Nếu user không phải charity org, trả về empty queryset
        requests = AssistanceRequest.objects.none()
        return render(request, 'charity-orgs/index-charity.html', {'requests': requests})
    
    # Lấy các loại assistance request type mà charity org này hỗ trợ
    supported_types = CharityOrgAssistanceRequestType.objects.filter(
        charity_org=charity_org
    ).values_list('assistance_request_type_id', flat=True)
    
    # Lọc các yêu cầu hỗ trợ:
    # 1. charity_org_id còn trống (chưa có org nào nhận)
    # 2. receiving_status = 'waiting' 
    # 3. status = 'approved' (đã được admin duyệt)
    # 4. có type thuộc danh sách mà charity org này hỗ trợ
    requests = AssistanceRequest.objects.prefetch_related('images').filter(
        charity_org__isnull=True,  # charity_org_id còn trống
        receiving_status='waiting',
        status='approved',  # chỉ lấy các yêu cầu đã được duyệt
        assistancerequesttypemap__type_id__in=supported_types  # có type liên quan
    ).distinct()  # distinct để tránh duplicate khi 1 request có nhiều type
    
    return render(request, 'charity-orgs/index-charity.html', {'requests': requests})

# @role_required('charity')
# def list_assistance_requests(request):
#     # Lấy tất cả yêu cầu cùng ảnh đầu tiên nếu có
#     requests = AssistanceRequest.objects.prefetch_related('images').all()
#     return render(request, 'charity-orgs/list-assistance-requests.html', {'requests': requests})

role_required('charity')
def assistance_request_detail(request, pk):
    req = get_object_or_404(AssistanceRequest, pk=pk)
    form = EventCreationForm() 
    return render(request, 'charity-orgs/assistance_request_detail.html', {'req': req, 'form': form})

@role_required('charity')
def create_event(request, req_id):
    assistance_request = get_object_or_404(AssistanceRequest, id=req_id)
    current_user = request.user.nguoidung

    try:
        charity_org = CharityOrg.objects.get(user=current_user)
    except CharityOrg.DoesNotExist:
        return JsonResponse({'success': False, 'errors': ['Bạn không thuộc tổ chức từ thiện.']})

    if request.method == 'POST':
        form = EventCreationForm(request.POST, assistance_request=assistance_request)
        if form.is_valid():
            volunteers_number = form.cleaned_data['volunteers_number']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']

            Event.objects.create(
                charity_org=charity_org,
                assistance_request=assistance_request,
                title=assistance_request.title,
                description=form.cleaned_data.get('description', ''),
                start_time=start_time,
                end_time=end_time,
                status='pending',
                created_at=timezone.now(),
                volunteers_number=volunteers_number
            )

            assistance_request.charity_org = charity_org
            assistance_request.save()

            return JsonResponse({'success': True, 'message': 'Đã tạo sự kiện thành công.'})
        else:
            # Trả lỗi JSON
            errors = form.errors.get_json_data()
            error_messages = []
            for field, messages in errors.items():
                for msg in messages:
                    error_messages.append(msg['message'])
            return JsonResponse({'success': False, 'errors': error_messages})

    # Nếu không phải POST, trả về lỗi JSON
    return JsonResponse({'success': False, 'errors': ['Yêu cầu không hợp lệ.']})

# Thông tin tổ chức từ thiện
@role_required('charity')
@login_required
def charity_profile_view(request):
    nguoidung = request.user.nguoidung
    charity_org = CharityOrg.objects.get(user=nguoidung)
    all_assist_types = AssistanceRequestType.objects.all()
    selected_types = CharityOrgAssistanceRequestType.objects.filter(charity_org=charity_org).values_list('assistance_request_type_id', flat=True)

    if request.method == "POST":
        user = request.user
        user.username = request.POST.get('username')
        user.first_name = request.POST.get('first_name')
        user.last_name = ""  # optional
        user.email = request.POST.get('email')
        user.save()

        nguoidung.dob = request.POST.get('dob')
        nguoidung.phone = request.POST.get('phone')
        nguoidung.address = request.POST.get('address')
        nguoidung.description = request.POST.get('description')
        
        # Upload avatar
        if 'avatar_file' in request.FILES:
            avatar_file = request.FILES['avatar_file']
            from django.core.files.storage import default_storage
            path = default_storage.save(f'avatars/{avatar_file.name}', avatar_file)
            nguoidung.avatar_url = default_storage.url(path)
        
        nguoidung.save()

        charity_org.website = request.POST.get('website')
        charity_org.save()

        # Update assistance types
        selected_ids = request.POST.getlist('assistance_types')
        CharityOrgAssistanceRequestType.objects.filter(charity_org=charity_org).delete()
        for id in selected_ids:
            CharityOrgAssistanceRequestType.objects.create(
                charity_org=charity_org,
                assistance_request_type_id=id
            )

        messages.success(request, "Cập nhật thông tin thành công.")
        return redirect('charity-profile')

    selected_assist_types = AssistanceRequestType.objects.filter(id__in=selected_types)
    return render(request, 'charity-orgs/profile.html', {
        'user': request.user,
        'nguoidung': nguoidung,
        'charity_org': charity_org,
        'all_assist_types': all_assist_types,
        'selected_assist_types': selected_assist_types
    })

# trang danh sách sự kiện

@role_required('charity')
def events_list_by_status(request, status):
    # Mapping trạng thái với tên hiển thị
    status_map = {
        'pending': 'Pending',
        'approved': 'Approved',
        'completed': 'Completed',
        'rejected': 'Rejected'
    }
    
    # Kiểm tra status hợp lệ
    if status not in status_map:
        return render(request, 'error.html', {'message': 'Trạng thái không hợp lệ'})
    
    display_status = status_map[status]

    # Lấy CharityOrg từ user hiện tại
    try:
        nguoi_dung = request.user.nguoidung
        charity_org = CharityOrg.objects.get(user=nguoi_dung)
    except (AttributeError, CharityOrg.DoesNotExist):
        return render(request, 'error.html', {'message': 'Không tìm thấy tổ chức từ thiện của bạn'})

    # Lọc sự kiện theo charity_org và status (sử dụng status gốc, không phải display_status)
    event_data = Event.objects.filter(
        charity_org=charity_org,
        status=status  # Sử dụng status parameter, không phải display_status
    ).select_related('charity_org', 'assistance_request').order_by('-start_time')

    # Thêm STT và đếm số tình nguyện viên cho mỗi sự kiện
    for i, event in enumerate(event_data, 1):
        event.stt = i
        
        # Đếm số tình nguyện viên đã đăng ký (status approved hoặc completed)
        if status in ['approved', 'completed']:
            event.volunteers = EventRegistration.objects.filter(
                event=event,
                status__in=['approved', 'completed']
            ).count()
        else:
            event.volunteers = 0

    return render(request, 'charity-orgs/event_list_status.html', {
        'event_data': event_data,
        'status_slug': status,
        'display_status': display_status,
    })


@role_required('charity')
def charity_event_completed_detail(request, event_id):
    """Chi tiết sự kiện đã hoàn thành với tính năng đánh giá TNV"""
    
    try:
        nguoi_dung = request.user.nguoidung
        charity_org = CharityOrg.objects.get(user=nguoi_dung)
    except CharityOrg.DoesNotExist:
        return render(request, 'error.html', {'message': 'Không tìm thấy tổ chức từ thiện của bạn'})
    
    event = get_object_or_404(Event, id=event_id, charity_org=charity_org, status='completed')
    
    # TNV chưa được đánh giá (rating = null)
    unrated_volunteers = EventRegistration.objects.filter(
        event=event,
        status='completed',
        rating__isnull=True
    ).select_related('volunteer__user__user')
    
    # TNV đã được đánh giá
    rated_volunteers = EventRegistration.objects.filter(
        event=event,
        status='completed',
        rating__isnull=False
    ).select_related('volunteer__user__user')
    
    context = {
        'event': event,
        'charity_org': charity_org,
        'unrated_volunteers': unrated_volunteers,
        'rated_volunteers': rated_volunteers,
        'total_unrated': unrated_volunteers.count(),
        'total_rated': rated_volunteers.count(),
    }
    
    return render(request, 'charity-orgs/event_completed_detail.html', context)

@role_required('charity')
def charity_event_detail(request, event_id):
    """Chi tiết sự kiện cho các trạng thái: pending, rejected, approved"""
    from django.db.models import Avg, Count
    
    # Lấy sự kiện và kiểm tra quyền truy cập
    try:
        nguoi_dung = request.user.nguoidung
        charity_org = CharityOrg.objects.get(user=nguoi_dung)
    except CharityOrg.DoesNotExist:
        return render(request, 'error.html', {'message': 'Không tìm thấy tổ chức từ thiện của bạn'})
    
    event = get_object_or_404(Event, id=event_id, charity_org=charity_org)
    
    context = {
        'event': event,
        'charity_org': charity_org,
    }
    
    # Xử lý theo từng trạng thái
    if event.status == 'approved':
        # Lấy danh sách TNV đã được chấp nhận
        approved_volunteers = EventRegistration.objects.filter(
            event=event, 
            status='approved'
        ).select_related('volunteer__user__user')
        
        # Lấy danh sách TNV đang chờ duyệt với thông tin đánh giá
        pending_volunteers = EventRegistration.objects.filter(
            event=event, 
            status='pending'
        ).select_related('volunteer__user__user')
        
        # Tính toán thông tin đánh giá cho từng TNV chờ duyệt
        for registration in pending_volunteers:
            volunteer_ratings = EventRegistration.objects.filter(
                volunteer=registration.volunteer,
                rating__isnull=False,
                status='completed'
            ).aggregate(
                avg_rating=Avg('rating'),
                total_reviews=Count('rating')
            )
            
            registration.avg_rating = round(volunteer_ratings['avg_rating'] or 0, 1)
            registration.total_reviews = volunteer_ratings['total_reviews'] or 0
        
        context.update({
            'approved_volunteers': approved_volunteers,
            'pending_volunteers': pending_volunteers,
            'total_approved': approved_volunteers.count(),
            'total_pending': pending_volunteers.count(),
        })
        
    elif event.status == 'completed':
        return redirect('charity_event_completed_detail', event_id=event_id)
    
    return render(request, 'charity-orgs/event_detail.html', context)


@role_required('charity')
def get_volunteer_reviews(request, volunteer_id):
    """API để lấy tất cả đánh giá của một tình nguyện viên"""
    try:
        volunteer = get_object_or_404(Volunteer, user__user__id=volunteer_id)
        
        reviews = EventRegistration.objects.filter(
            volunteer=volunteer,
            rating__isnull=False,
            status='completed'
        ).select_related('event').order_by('-checked_out_at')
        
        reviews_data = []
        for review in reviews:
            reviews_data.append({
                'event_title': review.event.title,
                'rating': review.rating,
                'review': review.review or "Không có nhận xét",
                'date': review.checked_out_at.strftime('%d/%m/%Y') if review.checked_out_at else "N/A"
            })
        
        return JsonResponse({
            'success': True,
            'volunteer_name': volunteer.user.user.get_full_name(),
            'reviews': reviews_data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Có lỗi xảy ra: {str(e)}'
        })
@role_required('charity')
def approve_volunteer_registration(request, registration_id):
    """Chấp nhận đăng ký TNV"""
    if request.method == 'POST':
        try:
            nguoi_dung = request.user.nguoidung
            charity_org = CharityOrg.objects.get(user=nguoi_dung)
            
            registration = get_object_or_404(
                EventRegistration, 
                id=registration_id, 
                event__charity_org=charity_org,
                status='pending'
            )
            
            with transaction.atomic():
                registration.status = 'approved'
                registration.save()
            
            return JsonResponse({
                'success': True,
                'message': f'Đã chấp nhận đăng ký của {registration.volunteer.user.user.get_full_name()}'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Có lỗi xảy ra: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Phương thức không hợp lệ'})


@role_required('charity')
def reject_volunteer_registration(request, registration_id):
    """Từ chối đăng ký TNV"""
    if request.method == 'POST':
        try:
            nguoi_dung = request.user.nguoidung
            charity_org = CharityOrg.objects.get(user=nguoi_dung)
            
            registration = get_object_or_404(
                EventRegistration, 
                id=registration_id, 
                event__charity_org=charity_org,
                status='pending'
            )
            
            with transaction.atomic():
                registration.status = 'rejected'
                registration.save()
            
            return JsonResponse({
                'success': True,
                'message': f'Đã từ chối đăng ký của {registration.volunteer.user.user.get_full_name()}'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Có lỗi xảy ra: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Phương thức không hợp lệ'})


import logging

@role_required('charity')
@csrf_protect
@require_http_methods(["POST"])
def rate_volunteer(request):
    """Đánh giá TNV sau khi hoàn thành sự kiện"""
    logger = logging.getLogger(__name__)
    try:
        # Log request info for debugging
        logger.info(f"Rate volunteer request from user: {request.user.username}")
        logger.info(f"Request body: {request.body.decode('utf-8')}")
        
        # Kiểm tra Content-Type
        if not request.content_type.startswith('application/json'):
            return JsonResponse({
                'success': False,
                'message': f'Content-Type không đúng: {request.content_type}'
            }, status=400)
        
        # Parse JSON data from request body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}")
            return JsonResponse({
                'success': False,
                'message': f'Dữ liệu JSON không hợp lệ: {str(e)}'
            }, status=400)
        
        # Kiểm tra user và charity org
        if not hasattr(request.user, 'nguoidung'):
            return JsonResponse({
                'success': False,
                'message': 'User không có thông tin NguoiDung'
            }, status=403)
            
        nguoi_dung = request.user.nguoidung
        
        try:
            charity_org = CharityOrg.objects.get(user=nguoi_dung)
        except CharityOrg.DoesNotExist:
            logger.error(f"CharityOrg not found for user: {request.user.username}")
            return JsonResponse({
                'success': False,
                'message': 'Không tìm thấy tổ chức từ thiện'
            }, status=403)
        
        # Validate input data
        registration_id = data.get('registration_id')
        if not registration_id:
            return JsonResponse({
                'success': False,
                'message': 'Thiếu registration_id'
            }, status=400)
        
        # Get rating and review from JSON data
        rating = data.get('rating')
        review = data.get('review', '')
        
        # Validate rating
        try:
            rating = int(rating)
            if not (1 <= rating <= 10):
                raise ValueError("Rating phải từ 1 đến 10")
        except (ValueError, TypeError) as e:
            logger.error(f"Invalid rating: {rating}, error: {str(e)}")
            return JsonResponse({
                'success': False,
                'message': 'Điểm đánh giá không hợp lệ (1-10)'
            }, status=400)
        
        # Get registration với nhiều kiểm tra hơn
        try:
            registration = EventRegistration.objects.select_related(
                'event', 'volunteer__user__user'
            ).get(
                id=registration_id, 
                event__charity_org=charity_org,
                event__status='completed',
                status='completed'
            )
        except EventRegistration.DoesNotExist:
            logger.error(f"Registration not found: {registration_id} for charity: {charity_org.user.user.username}")
            return JsonResponse({
                'success': False,
                'message': 'Không tìm thấy đăng ký tình nguyện viên hoặc sự kiện chưa hoàn thành'
            }, status=404)
        
        # Kiểm tra xem đã đánh giá chưa
        if registration.rating is not None:
            return JsonResponse({
                'success': False,
                'message': 'Tình nguyện viên này đã được đánh giá rồi'
            }, status=400)
        
        # Save rating
        with transaction.atomic():
            registration.rating = rating
            registration.review = review.strip()
            registration.save()
            
            logger.info(f"Successfully rated volunteer {registration.volunteer.user.user.username} with {rating}/10")
        
        # Lấy tên volunteer an toàn hơn
        try:
            volunteer_name = registration.volunteer.user.user.get_full_name()
            if not volunteer_name.strip():
                volunteer_name = registration.volunteer.user.user.username
        except AttributeError:
            volunteer_name = "Tình nguyện viên"
        
        return JsonResponse({
            'success': True,
            'message': f'Đã đánh giá {volunteer_name}: {rating}/10'
        })
        
    except Exception as e:
        # Log lỗi chi tiết để debug
        logger.error(f"Unexpected error in rate_volunteer: {str(e)}", exc_info=True)
        
        return JsonResponse({
            'success': False,
            'message': f'Có lỗi xảy ra: {str(e)}'
        }, status=500)

#---logout view      
def charity_logout(request):
    logout(request)  # xoá session, đăng xuất
    return redirect('index')