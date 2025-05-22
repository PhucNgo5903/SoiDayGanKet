
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
        title="Mùa hè xanh 2021",
        description="Phát quà và đồ dùng học tập",
        start_time=timezone.make_aware(timezone.datetime(2023, 6, 24, 8, 0)),
        end_time=timezone.make_aware(timezone.datetime(2023, 7, 15, 17, 0)),
        status='pending',  # 'pending', 'approved', 'rejected', 'completed' # Chỉ điền khi status là approved/rejected # Tùy chọn  # Hoặc False
        volunteers_number=20,
        )
        print("Thêm sự kiện thành công!")
    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == '__main__':
    insert_sample_event()