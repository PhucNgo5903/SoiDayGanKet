
import os
import django
from django.utils import timezone


# Thiết lập môi trường Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'donenv.settings')
django.setup()
from django.utils import timezone
from app.models import Event, CharityOrg, AssistanceRequest, NguoiDung
def insert_sample_event():
    try:
        charity_org = CharityOrg.objects.get(pk=2)  # Thay bằng ID thực tế
        assistance_request = AssistanceRequest.objects.get(pk=2)

        Event.objects.create(
        charity_org=charity_org,
        assistance_request=assistance_request,
        title="Mùa đông ấm 2025",
        description="Sưởi ấm trái tim những người cô đơn ở HUST",
        start_time=timezone.make_aware(timezone.datetime(2025, 6, 24, 8, 0)),
        end_time=timezone.make_aware(timezone.datetime(2025, 8, 15, 17, 0)),
        status='pending',  # 'pending', 'approved', 'rejected', 'completed' # Chỉ điền khi status là approved/rejected # Tùy chọn  # Hoặc False
        volunteers_number=2,
        )
        print("Thêm sự kiện thành công!")
    except Exception as e:
        print(f"Lỗi: {e}")

# def insert_sample_event_registrations():
#     try:
#         event = Event.objects.get(pk=2)  # Thay bằng ID thực tế
#         assistance_request = AssistanceRequest.objects.get(pk=2)

#         Event.objects.create(
#         charity_org=charity_org,
#         assistance_request=assistance_request,
#         title="Mùa thu mát 2023",
#         description="Sưởi ấm trái tim những người cô đơn ở HUST",
#         start_time=timezone.make_aware(timezone.datetime(2025, 6, 24, 8, 0)),
#         end_time=timezone.make_aware(timezone.datetime(2025, 8, 15, 17, 0)),
#         status='pending',  # 'pending', 'approved', 'rejected', 'completed' # Chỉ điền khi status là approved/rejected # Tùy chọn  # Hoặc False
#         volunteers_number=0,
#         )
#         print("Thêm sự kiện thành công!")
#     except Exception as e:
#         print(f"Lỗi: {e}")
if __name__ == '__main__':
    insert_sample_event()
    # insert_sample_event_registrations()