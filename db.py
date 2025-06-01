import os
import django
import sqlite3
from django.contrib.auth.hashers import make_password
from datetime import datetime, timedelta
import random

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'donenv.settings')
django.setup()

conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()

# Helper function for random dates
def random_date(start_year=1970, end_year=2000):
    start = datetime(year=start_year, month=1, day=1)
    end = datetime(year=end_year, month=12, day=31)
    delta = end - start
    return (start + timedelta(days=random.randint(0, delta.days))).date()

def random_datetime_future(days_ahead=30):
    return datetime.now() + timedelta(days=random.randint(1, days_ahead))

def random_datetime_past(days_back=30):
    return datetime.now() - timedelta(days=random.randint(1, days_back))

print("Bắt đầu tạo dữ liệu test cho Charity Organization...")

# ========== 1. Tạo Users và NguoiDung ==========
print("Tạo Users và NguoiDung...")

# Xóa dữ liệu cũ nếu có
cur.execute('DELETE FROM app_eventregistration')
cur.execute('DELETE FROM app_event')
cur.execute('DELETE FROM app_assistancerequesttypemap')
cur.execute('DELETE FROM app_assistancerequestimage')
cur.execute('DELETE FROM app_assistancerequest')
cur.execute('DELETE FROM app_charityorgassistancerequesttype')
cur.execute('DELETE FROM app_volunteerskill')
cur.execute('DELETE FROM app_charityorg')
cur.execute('DELETE FROM app_beneficiary')
cur.execute('DELETE FROM app_volunteer')
cur.execute('DELETE FROM app_nguoidung')
cur.execute('DELETE FROM app_assistancerequesttype')
cur.execute('DELETE FROM app_skill')
cur.execute('DELETE FROM auth_user WHERE id > 0')
conn.commit()

# Tạo 30 users
users_data = []
for i in range(1, 31):
    username = f'testuser{i}'
    password = make_password(f'Test{i}123')
    email = f'testuser{i}@charity.test'
    first_name = f'Test{i}'
    last_name = f'User{i}'
    date_joined = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    users_data.append((password, username, 0, 0, 1, last_name, email, date_joined, first_name))

cur.executemany('''
INSERT INTO auth_user (password, username, is_superuser, is_staff, is_active, last_name, email, date_joined, first_name)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', users_data)
conn.commit()

# Lấy user IDs
cur.execute('SELECT id FROM auth_user ORDER BY id')
user_ids = [row[0] for row in cur.fetchall()]

# Tạo NguoiDung
nguoidung_data = []
roles = ['admin', 'volunteer', 'charity', 'beneficiary']

for i, user_id in enumerate(user_ids):
    if user_id == 3:  # User ID 3 sẽ là charity chính
        role = 'charity'
    elif i < 5:
        role = 'admin'
    elif i < 20:
        role = 'volunteer'
    elif i < 25:
        role = 'beneficiary'
    else:
        role = 'charity'
    
    dob = random_date()
    phone = f'09{random.randint(10000000, 99999999)}'
    address = f'{random.randint(100, 999)} Đường Nguyễn Văn {chr(65 + i%26)}, Quận {random.randint(1,12)}, TP.HCM'
    description = f'Mô tả chi tiết cho {role} {user_id}'
    status = 'active'
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    nguoidung_data.append((user_id, role, dob.isoformat(), phone, address, description, status, created_at))

cur.executemany('''
INSERT INTO app_nguoidung (user_id, role, dob, phone, address, description, status, created_at)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', nguoidung_data)
conn.commit()

# ========== 2. Tạo Volunteer, Beneficiary, CharityOrg ==========
print("Tạo Volunteer, Beneficiary, CharityOrg...")

genders = ['male', 'female', 'other']
org_types = ['local', 'national', 'international']

# Lấy role của từng user
cur.execute('SELECT user_id, role FROM app_nguoidung')
user_roles = dict(cur.fetchall())

volunteer_data = []
beneficiary_data = []
charityorg_data = []

for user_id, role in user_roles.items():
    if role == 'volunteer':
        gender = random.choice(genders)
        volunteer_data.append((user_id, gender))
    elif role == 'beneficiary':
        gender = random.choice(genders)
        beneficiary_data.append((user_id, gender))
    elif role == 'charity':
        if user_id == 3:
            org_type = 'local'
            website = 'https://charitytest.org'
        else:
            org_type = random.choice(org_types)
            website = f'https://charity{user_id}.test'
        charityorg_data.append((user_id, org_type, website))

cur.executemany('INSERT INTO app_volunteer (user_id, gender) VALUES (?, ?)', volunteer_data)
cur.executemany('INSERT INTO app_beneficiary (user_id, gender) VALUES (?, ?)', beneficiary_data)
cur.executemany('INSERT INTO app_charityorg (user_id, type, website) VALUES (?, ?, ?)', charityorg_data)
conn.commit()

# Lấy IDs
cur.execute('SELECT user_id FROM app_volunteer')
volunteer_ids = [row[0] for row in cur.fetchall()]
cur.execute('SELECT user_id FROM app_beneficiary')
beneficiary_ids = [row[0] for row in cur.fetchall()]
cur.execute('SELECT user_id FROM app_charityorg')
charityorg_ids = [row[0] for row in cur.fetchall()]

print(f"Tạo {len(volunteer_ids)} volunteers, {len(beneficiary_ids)} beneficiaries, {len(charityorg_ids)} charity orgs")

# ========== 3. Tạo Skills và VolunteerSkill ==========
print("Tạo Skills và VolunteerSkill...")

skills = [
    'Tổ chức sự kiện', 'Chăm sóc y tế', 'Giáo dục trẻ em', 'Nấu ăn', 'Thiết kế đồ họa',
    'Lập trình web', 'Giao tiếp công chúng', 'Quản lý dự án', 'Marketing online', 'Hỗ trợ tâm lý',
    'Vận tải hàng hóa', 'Phiên dịch', 'Tư vấn pháp lý', 'Sửa chữa điện', 'Huấn luyện thể thao',
    'Chụp ảnh', 'Làm video', 'Kế toán', 'Điều dưỡng', 'Xây dựng'
]

cur.executemany('INSERT INTO app_skill (name) VALUES (?)', [(s,) for s in skills])
conn.commit()

cur.execute('SELECT id FROM app_skill')
skill_ids = [row[0] for row in cur.fetchall()]

# Tạo VolunteerSkill
volunteer_skill_data = []
for vid in volunteer_ids:
    chosen_skills = random.sample(skill_ids, random.randint(2, 5))
    for sid in chosen_skills:
        volunteer_skill_data.append((vid, sid))

cur.executemany('INSERT INTO app_volunteerskill (volunteer_id, skill_id) VALUES (?, ?)', volunteer_skill_data)
conn.commit()

# ========== 4. Tạo AssistanceRequestType ==========
print("Tạo AssistanceRequestType...")

assistance_types = [
    'Hỗ trợ tiền bạc', 'Cung cấp thực phẩm', 'Tặng quần áo', 'Hỗ trợ chỗ ở',
    'Giáo dục miễn phí', 'Khám chữa bệnh', 'Tư vấn pháp lý', 'Hỗ trợ tâm lý',
    'Vận chuyển đồ', 'Sửa chữa nhà', 'Đào tạo nghề', 'Tìm việc làm'
]

cur.executemany('INSERT INTO app_assistancerequesttype (name) VALUES (?)', [(t,) for t in assistance_types])
conn.commit()

cur.execute('SELECT id FROM app_assistancerequesttype')
artype_ids = [row[0] for row in cur.fetchall()]

# ========== 5. Tạo CharityOrgAssistanceRequestType cho charity ID 3 ==========
print("Tạo CharityOrgAssistanceRequestType...")

# Charity org ID 3 hỗ trợ 6 loại đầu tiên
charity_3_supported_types = artype_ids[:6]
charity_artype_data = []

for aid in charity_3_supported_types:
    charity_artype_data.append((3, aid))

# Các charity khác cũng hỗ trợ random
for cid in charityorg_ids:
    if cid != 3:
        chosen_types = random.sample(artype_ids, random.randint(3, 6))
        for aid in chosen_types:
            charity_artype_data.append((cid, aid))

cur.executemany('INSERT INTO app_charityorgassistancerequesttype (charity_org_id, assistance_request_type_id) VALUES (?, ?)', charity_artype_data)
conn.commit()

# ========== 6. Tạo 10 AssistanceRequest đặc biệt cho Charity ID 3 ==========
print("Tạo 10 AssistanceRequest đặc biệt...")

special_requests = []
priority_choices = ['low', 'medium', 'high']

for i in range(10):
    beneficiary_id = random.choice(beneficiary_ids)
    charity_org_id = None  # Chưa được nhận bởi charity nào
    title = f'Yêu cầu hỗ trợ khẩn cấp #{i+1}'
    description = f'Mô tả chi tiết yêu cầu hỗ trợ #{i+1}. Cần sự giúp đỡ khẩn cấp từ tổ chức từ thiện có uy tín. Hoàn cảnh rất khó khăn, mong nhận được sự quan tâm.'
    priority = random.choice(priority_choices)
    start_date = datetime.now() + timedelta(days=random.randint(1, 10))
    end_date = start_date + timedelta(days=random.randint(7, 21))
    status = 'approved'  # Đã được duyệt
    receiving_status = 'waiting'  # Đang chờ nhận hỗ trợ
    created_at = random_datetime_past(15)
    update_by = random.choice([uid for uid, role in user_roles.items() if role == 'admin'])
    update_status_at = created_at + timedelta(hours=random.randint(1, 48))
    place = f'Địa chỉ nhận hỗ trợ #{i+1}: {random.randint(100, 999)} Đường ABC, Phường {random.randint(1, 20)}, Quận {random.randint(1, 12)}, TP.HCM'
    proof_url = f'https://storage.charity.test/proof_{i+1}.jpg'
    admin_remark = f'Đã xác minh thông tin. Hoàn cảnh khó khăn, cần hỗ trợ gấp.'

    special_requests.append((
        beneficiary_id, charity_org_id, title, description, priority,
        start_date.strftime('%Y-%m-%d %H:%M:%S'),
        end_date.strftime('%Y-%m-%d %H:%M:%S'),
        status, receiving_status,
        created_at.strftime('%Y-%m-%d %H:%M:%S'),
        update_by,
        update_status_at.strftime('%Y-%m-%d %H:%M:%S'),
        place, proof_url, admin_remark
    ))

cur.executemany('''
INSERT INTO app_assistancerequest 
(beneficiary_id, charity_org_id, title, description, priority, start_date, end_date, status, receiving_status, created_at, update_by_id, update_status_at, place, proof_url, admin_remark)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', special_requests)
conn.commit()

# Lấy assistance request IDs
cur.execute('SELECT id FROM app_assistancerequest ORDER BY id DESC LIMIT 10')
special_request_ids = [row[0] for row in cur.fetchall()]

# Tạo AssistanceRequestTypeMap cho 10 requests đặc biệt
artype_map_data = []
for arid in special_request_ids:
    # Mỗi request có 1-3 loại hỗ trợ mà charity 3 có thể làm
    chosen_types = random.sample(charity_3_supported_types, random.randint(1, 3))
    for tid in chosen_types:
        artype_map_data.append((arid, tid))

cur.executemany('INSERT INTO app_assistancerequesttypemap (assistance_request_id, type_id) VALUES (?, ?)', artype_map_data)
conn.commit()

# Tạo AssistanceRequestImage
ari_data = []
sample_images = [
    'https://aashritha.org/wp-content/uploads/2024/05/Untitled-design-17-1024x576.png',
    'https://example.com/charity1.jpg',
    'https://example.com/charity2.jpg',
    'https://example.com/charity3.jpg'
]

for arid in special_request_ids:
    for _ in range(random.randint(1, 3)):
        image_url = random.choice(sample_images)
        ari_data.append((arid, image_url))

cur.executemany('INSERT INTO app_assistancerequestimage (assistance_request_id, image_url) VALUES (?, ?)', ari_data)
conn.commit()

# ========== 7. Tạo 20 Events cho Charity ID 3 ==========
print("Tạo 20 Events cho Charity ID 3...")

event_statuses = ['pending', 'approved', 'rejected', 'completed']
events_data = []

# 5 events cho mỗi status (5x4 = 20)
for status_idx, status in enumerate(event_statuses):
    for i in range(5):
        event_num = status_idx * 5 + i + 1
        charity_org_id = 3
        
        # Một số event liên kết với assistance request
        assistance_request_id = random.choice(special_request_ids + [None, None])
        
        title = f'Sự kiện từ thiện #{event_num} - {status.upper()}'
        description = f'''Mô tả chi tiết sự kiện #{event_num}:
- Loại sự kiện: {status}
- Mục tiêu: Hỗ trợ cộng đồng khó khăn
- Địa điểm: Trung tâm từ thiện ABC
- Hoạt động chính: Phát quà, tư vấn, hỗ trợ
- Đối tượng: Người già, trẻ em khó khăn
- Dự kiến tham gia: {random.randint(20, 100)} người'''
        
        if status in ['pending', 'rejected']:
            start_time = random_datetime_future(30)
        else:  # approved, completed
            start_time = random_datetime_future(15)
            
        end_time = start_time + timedelta(hours=random.randint(4, 8))
        created_at = random_datetime_past(20)
        
        if status in ['approved', 'completed']:
            approved_by = random.choice([uid for uid, role in user_roles.items() if role == 'admin'])
            approved_at = created_at + timedelta(hours=random.randint(1, 72))
        else:
            approved_by = None
            approved_at = None
            
        report_url = f'https://reports.charity.test/event_{event_num}.pdf' if status == 'completed' else None
        confirmed_by = status in ['approved', 'completed']
        volunteers_number = random.randint(10, 50)
        
        if status == 'rejected':
            reason = f'Lý do từ chối: Không đủ điều kiện thực hiện tại thời điểm này. Cần bổ sung thêm thông tin về {random.choice(["ngân sách", "nhân lực", "địa điểm", "giấy phép"])}.'
        else:
            reason = None

        events_data.append((
            charity_org_id, assistance_request_id, title, description,
            start_time.strftime('%Y-%m-%d %H:%M:%S'),
            end_time.strftime('%Y-%m-%d %H:%M:%S'),
            status, created_at.strftime('%Y-%m-%d %H:%M:%S'),
            approved_by,
            approved_at.strftime('%Y-%m-%d %H:%M:%S') if approved_at else None,
            report_url, int(confirmed_by), volunteers_number, reason
        ))

cur.executemany('''
INSERT INTO app_event (charity_org_id, assistance_request_id, title, description, start_time, end_time, status, created_at, approved_by_id, approved_at, report_url, confirmed_by, volunteers_number, reason)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', events_data)
conn.commit()

# Lấy Event IDs
cur.execute('SELECT id, status FROM app_event WHERE charity_org_id = 3 ORDER BY id')
event_data = cur.fetchall()

# ========== 8. Tạo EventRegistration với một số chưa được đánh giá ==========
print("Tạo EventRegistration với một số tình nguyện viên chưa được đánh giá...")

registration_statuses = ['pending', 'approved', 'rejected', 'completed']
reviews_templates = [
    "Sự kiện rất ý nghĩa, tôi cảm thấy hạnh phúc khi được giúp đỡ cộng đồng.",
    "Tổ chức chuyên nghiệp, hoạt động bổ ích. Tôi sẽ tham gia các sự kiện khác.",
    "Được tham gia sự kiện này là một trải nghiệm tuyệt vời. Cảm ơn ban tổ chức!",
    "Hoạt động thiết thực, giúp ích nhiều cho người dân. Tôi rất hài lòng.",
    "Sự kiện được chuẩn bị kỹ lưỡng, tôi học được nhiều điều từ hoạt động này.",
    "Môi trường làm việc tích cực, mọi người rất nhiệt tình. Đáng tham gia!",
    "Cảm ơn vì cơ hội được đóng góp cho cộng đồng. Sự kiện rất bổ ích.",
    "Hoạt động ý nghĩa, tôi cảm thấy được lan tỏa yêu thương đến nhiều người."
]

registrations_data = []
unrated_volunteers_count = 0

for event_id, event_status in event_data:
    # Số lượng volunteer đăng ký cho mỗi event
    num_volunteers = random.randint(8, 15)
    selected_volunteers = random.sample(volunteer_ids, min(len(volunteer_ids), num_volunteers))
    
    for idx, volunteer_id in enumerate(selected_volunteers):
        if event_status == 'pending':
            reg_status = random.choice(['pending', 'approved'])
        elif event_status == 'rejected':
            reg_status = random.choice(['pending', 'rejected'])
        elif event_status == 'approved':
            # ⭐ THAY ĐỔI TẠI ĐÂY: Thêm volunteers có status "pending" cho events "approved"
            if idx < 3:  # 3 volunteers đầu tiên sẽ có status "pending"
                reg_status = 'pending'
                print(f"  🔄 Event #{event_id} (approved): Volunteer {volunteer_id} = PENDING (cần duyệt)")
            else:
                reg_status = random.choice(['approved', 'completed'])
        else:  # completed
            reg_status = 'completed'
        
        registered_at = random_datetime_past(25)
        
        # Chỉ set check-in time cho volunteers đã approved/completed
        if reg_status in ['approved', 'completed']:
            checked_in_at = registered_at + timedelta(days=random.randint(1, 10))
        else:
            checked_in_at = None
            
        if reg_status == 'completed' and checked_in_at:
            checked_out_at = checked_in_at + timedelta(hours=random.randint(4, 8))
            
            # Đối với events đã hoàn thành, để 1-2 volunteers đầu tiên chưa được đánh giá
            if event_status == 'completed' and idx < 2:
                rating = None
                review = None
                unrated_volunteers_count += 1
                print(f"  ⭐ Event #{event_id}: Volunteer {volunteer_id} chưa được đánh giá")
            else:
                rating = random.randint(7, 10)  # Rating cao để có dữ liệu tốt cho View Rating
                review = random.choice(reviews_templates) + f" (Event #{event_id})"
        else:
            checked_out_at = None
            rating = None
            review = None

        registrations_data.append((
            event_id, volunteer_id, reg_status,
            registered_at.strftime('%Y-%m-%d %H:%M:%S'),
            checked_in_at.strftime('%Y-%m-%d %H:%M:%S') if checked_in_at else None,
            checked_out_at.strftime('%Y-%m-%d %H:%M:%S') if checked_out_at else None,
            rating, review
        ))

cur.executemany('''
INSERT INTO app_eventregistration 
(event_id, volunteer_id, status, registered_at, checked_in_at, checked_out_at, rating, review)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', registrations_data)
conn.commit()

# Đếm số volunteers pending trong events approved
conn_check = sqlite3.connect('db.sqlite3')
cur_check = conn_check.cursor()
cur_check.execute('''
    SELECT COUNT(*) FROM app_eventregistration er
    JOIN app_event e ON er.event_id = e.id 
    WHERE e.status = 'approved' AND er.status = 'pending' AND e.charity_org_id = 3
''')
pending_count = cur_check.fetchone()[0]
conn_check.close()

# ========== 9. Tạo thêm một số dữ liệu phụ ==========
print("Tạo dữ liệu bổ sung...")

# Tạo thêm một số assistance request khác (không liên quan đến charity 3)
other_requests = []
for i in range(5):
    beneficiary_id = random.choice(beneficiary_ids)
    charity_org_id = random.choice([c for c in charityorg_ids if c != 3] + [None])
    title = f'Yêu cầu hỗ trợ khác #{i+1}'
    description = f'Yêu cầu hỗ trợ thông thường #{i+1}'
    priority = random.choice(priority_choices)
    start_date = random_datetime_future(20)
    end_date = start_date + timedelta(days=random.randint(5, 15))
    status = random.choice(['pending', 'approved', 'rejected'])
    receiving_status = random.choice(['waiting', 'received']) if status == 'approved' else 'waiting'
    created_at = random_datetime_past(10)
    update_by = random.choice([uid for uid, role in user_roles.items() if role == 'admin']) if status != 'pending' else None
    update_status_at = created_at + timedelta(hours=24) if update_by else None
    place = f'Địa chỉ #{i+1}'
    proof_url = f'https://proof{i+1}.test'
    admin_remark = 'No admin remark'

    other_requests.append((
        beneficiary_id, charity_org_id, title, description, priority,
        start_date.strftime('%Y-%m-%d %H:%M:%S'),
        end_date.strftime('%Y-%m-%d %H:%M:%S'),
        status, receiving_status,
        created_at.strftime('%Y-%m-%d %H:%M:%S'),
        update_by,
        update_status_at.strftime('%Y-%m-%d %H:%M:%S') if update_status_at else None,
        place, proof_url, admin_remark
    ))

cur.executemany('''
INSERT INTO app_assistancerequest 
(beneficiary_id, charity_org_id, title, description, priority, start_date, end_date, status, receiving_status, created_at, update_by_id, update_status_at, place, proof_url, admin_remark)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', other_requests)
conn.commit()

conn.close()

# ========== 10. Thống kê dữ liệu đã tạo ==========
print("\n" + "="*70)
print("THỐNG KÊ DỮ LIỆU ĐÃ TẠO")
print("="*70)
print(f"✅ Tạo 30 users (ID 1-30)")
print(f"✅ User ID 3 = Charity Organization chính")
print(f"✅ {len(volunteer_ids)} volunteers")
print(f"✅ {len(beneficiary_ids)} beneficiaries")
print(f"✅ {len(charityorg_ids)} charity organizations")
print(f"✅ {len(skills)} skills")
print(f"✅ {len(assistance_types)} assistance request types")
print(f"✅ 10 assistance requests đặc biệt cho Charity ID 3")
print(f"   - Status: approved")
print(f"   - Receiving status: waiting")
print(f"   - Charity org ID: NULL (chưa được nhận)")
print(f"✅ 20 events cho Charity ID 3:")
print(f"   - 5 events: pending")
print(f"   - 5 events: approved (có đầy đủ volunteers + ratings)")
print(f"   - 5 events: rejected")
print(f"   - 5 events: completed (có volunteers + ratings + reviews)")
print(f"✅ Event registrations với {unrated_volunteers_count} tình nguyện viên chưa được đánh giá")
print(f"   📝 Các tình nguyện viên này đã tham gia sự kiện completed nhưng chưa có rating/review")
print(f"   📝 Bạn có thể test chức năng đánh giá với những tình nguyện viên này")
print(f"✅ 5 assistance requests khác (không liên quan Charity ID 3)")

print("\n" + "="*70)
print("THÔNG TIN ĐĂNG NHẬP TEST")
print("="*70)
print("🔑 Charity Organization chính:")
print("   Username: testuser3")
print("   Password: Test3123")
print("   Role: charity")
print("   User ID: 3")

print("\n🔑 Một số volunteer để test:")
for i, vid in enumerate(volunteer_ids[:3]):
    print(f"   Username: testuser{vid}")
    print(f"   Password: Test{vid}123")
    print(f"   Role: volunteer")

print("\n🔑 Admin để test:")
admin_users = [uid for uid, role in user_roles.items() if role == 'admin']
for aid in admin_users[:2]:
    print(f"   Username: testuser{aid}")
    print(f"   Password: Test{aid}123")
    print(f"   Role: admin")

print("\n" + "="*70)
print("🎯 ĐIỂM NHẤN QUAN TRỌNG")
print("="*70)
print(f"⭐ Có {unrated_volunteers_count} tình nguyện viên trong các sự kiện đã hoàn thành")
print("   chưa được đánh giá để bạn có thể test chức năng đánh giá!")
print("⭐ Các tình nguyện viên này có status 'completed' nhưng rating = NULL")
print("⭐ Bạn có thể đăng nhập bằng tài khoản testuser3 và thực hiện đánh giá")

print("\n" + "="*70)
print("DỮ LIỆU ĐÃ TẠO THÀNH CÔNG!")
print("Có thể bắt đầu test với Charity Organization ID 3")
print("="*70)