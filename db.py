import os
import django
import sqlite3
from django.contrib.auth.hashers import make_password
from datetime import datetime, timedelta
import random

# Setup Django environment (thay 'donenv.settings' bằng settings project của bạn)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'donenv.settings')
django.setup()

conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()

# Giúp random ngày sinh
def random_date(start_year=1950, end_year=2010):
    start = datetime(year=start_year, month=1, day=1)
    end = datetime(year=end_year, month=12, day=31)
    delta = end - start
    return (start + timedelta(days=random.randint(0, delta.days))).date()

# ========== 1. Tạo 20 User ==========
user_data = []
for i in range(1, 21):
    username = f'user{i}'
    password = make_password(f'Pass{i}123')
    email = f'user{i}@example.com'
    first_name = f'First{i}'
    last_name = f'Last{i}'
    date_joined = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    user_data.append((password, username, 0, 0, 1, last_name, email, date_joined, first_name))

cur.executemany('''
INSERT INTO auth_user (password, username, is_superuser, is_staff, is_active, last_name, email, date_joined, first_name)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', user_data)
conn.commit()

# Lấy lại user_ids vừa tạo
cur.execute('SELECT id FROM auth_user ORDER BY id DESC LIMIT 20')
user_ids = [row[0] for row in cur.fetchall()][::-1]

# ========== 2. Tạo NguoiDung ==========
roles = ['admin', 'volunteer', 'charity', 'beneficiary']
statuses = ['active', 'inactive']
nguoidung_data = []
for i, user_id in enumerate(user_ids):
    role = roles[i % len(roles)]
    status = statuses[i % len(statuses)]
    dob = random_date()
    phone = f'09{random.randint(10000000, 99999999)}'
    address = f'123 Đường số {i+1}, Quận {random.randint(1,12)}, TP.HCM'
    description = f'Mô tả cho người dùng {user_id}'
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    nguoidung_data.append((user_id, role, dob.isoformat(), phone, address, description, status, created_at))

cur.executemany('''
INSERT INTO app_nguoidung (user_id, role, dob, phone, address, description, status, created_at)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', nguoidung_data)
conn.commit()

# Lấy NguoiDung IDs
cur.execute('SELECT user_id FROM app_nguoidung')
nguoidung_ids = [row[0] for row in cur.fetchall()]

# ========== 3. Tạo Volunteer, Beneficiary, CharityOrg ==========
genders = ['male', 'female', 'other']
org_types = ['local', 'national', 'international']

volunteer_data = []
beneficiary_data = []
charityorg_data = []

for i, nguoidung_user_id in enumerate(nguoidung_ids):
    # Lấy role tương ứng
    role = roles[i % len(roles)]
    if role == 'volunteer':
        gender = random.choice(genders)
        volunteer_data.append((nguoidung_user_id, gender))
    elif role == 'beneficiary':
        gender = random.choice(genders)
        beneficiary_data.append((nguoidung_user_id, gender))
    elif role == 'charity':
        org_type = random.choice(org_types)
        website = f'https://charity{nguoidung_user_id}.org'
        charityorg_data.append((nguoidung_user_id, org_type, website))

cur.executemany('INSERT INTO app_volunteer (user_id, gender) VALUES (?, ?)', volunteer_data)
cur.executemany('INSERT INTO app_beneficiary (user_id, gender) VALUES (?, ?)', beneficiary_data)
cur.executemany('INSERT INTO app_charityorg (user_id, type, website) VALUES (?, ?, ?)', charityorg_data)
conn.commit()

# Lấy Volunteer IDs (là user_id của NguoiDung)
cur.execute('SELECT user_id FROM app_volunteer')
volunteer_ids = [row[0] for row in cur.fetchall()]

# Lấy Beneficiary IDs
cur.execute('SELECT user_id FROM app_beneficiary')
beneficiary_ids = [row[0] for row in cur.fetchall()]

# Lấy CharityOrg IDs
cur.execute('SELECT user_id FROM app_charityorg')
charityorg_ids = [row[0] for row in cur.fetchall()]

# ========== 4. Tạo Skill (15 skills) ==========
skills = ['Tổ chức', 'Y tế', 'Giáo dục', 'Nấu ăn', 'Thiết kế', 'Lập trình', 'Giao tiếp', 'Quản lý', 'Marketing', 'Hỗ trợ tâm lý', 'Vận tải', 'Phiên dịch', 'Tư vấn', 'Sửa chữa', 'Thể thao']
cur.executemany('INSERT INTO app_skill (name) VALUES (?)', [(s,) for s in skills])
conn.commit()

cur.execute('SELECT id FROM app_skill')
skill_ids = [row[0] for row in cur.fetchall()]

# ========== 5. Tạo VolunteerSkill ==========
volunteer_skill_data = []
for vid in volunteer_ids:
    # mỗi volunteer có 1-4 kỹ năng random
    chosen = random.sample(skill_ids, random.randint(1,4))
    for sid in chosen:
        volunteer_skill_data.append((vid, sid))
cur.executemany('INSERT INTO app_volunteerskill (volunteer_id, skill_id) VALUES (?, ?)', volunteer_skill_data)
conn.commit()

# ========== 6. Tạo SupportArea (8 area) ==========
support_areas = ['Nông thôn', 'Thành phố', 'Miền núi', 'Biên giới', 'Hải đảo', 'Vùng sâu vùng xa', 'Khu công nghiệp', 'Khu dân cư']
cur.executemany('INSERT INTO app_supportarea (name) VALUES (?)', [(a,) for a in support_areas])
conn.commit()

cur.execute('SELECT id FROM app_supportarea')
support_area_ids = [row[0] for row in cur.fetchall()]

# ========== 7. Tạo SkillsSupportArea (map ngẫu nhiên) ==========
skillsupportarea_data = []
for sid in skill_ids:
    chosen_areas = random.sample(support_area_ids, random.randint(1,3))
    for aid in chosen_areas:
        skillsupportarea_data.append((sid, aid))
cur.executemany('INSERT INTO app_skillssupportarea (skill_id, support_area_id) VALUES (?, ?)', skillsupportarea_data)
conn.commit()

# ========== 8. Tạo CharityOrgSupportArea ==========
charity_supportarea_data = []
for cid in charityorg_ids:
    chosen_areas = random.sample(support_area_ids, random.randint(1,3))
    for aid in chosen_areas:
        charity_supportarea_data.append((cid, aid))
cur.executemany('INSERT INTO app_charityorgsupportarea (charity_org_id, support_area_id) VALUES (?, ?)', charity_supportarea_data)
conn.commit()

# ========== 9. Tạo AssistanceRequestType (10 loại) ==========
artypes = ['Tiền bạc', 'Thực phẩm', 'Quần áo', 'Chỗ ở', 'Giáo dục', 'Y tế', 'Hỗ trợ pháp lý', 'Tư vấn tâm lý', 'Vận chuyển', 'Khác']
cur.executemany('INSERT INTO app_assistancerequesttype (name) VALUES (?)', [(t,) for t in artypes])
conn.commit()

cur.execute('SELECT id FROM app_assistancerequesttype')
artype_ids = [row[0] for row in cur.fetchall()]

# ========== 10. Tạo AssistanceRequest (20 bản ghi) ==========
priority_choices = ['low', 'medium', 'high']
status_choices = ['pending', 'approved', 'rejected']
receiving_choices = ['waiting', 'received']

assistance_requests = []
for i in range(20):
    beneficiary_id = random.choice(beneficiary_ids)
    charity_org_id = random.choice(charityorg_ids + [None])
    title = f'Yêu cầu hỗ trợ #{i+1}'
    description = f'Mô tả yêu cầu hỗ trợ #{i+1}'
    priority = random.choice(priority_choices)
    start_date = datetime.now() - timedelta(days=random.randint(1,30))
    end_date = start_date + timedelta(days=random.randint(5,15))
    status = random.choice(status_choices)
    receiving_status = random.choice(receiving_choices)
    created_at = datetime.now()
    approved_by = random.choice(nguoidung_ids + [None])
    approved_at = created_at if approved_by else None
    place = f'Địa điểm hỗ trợ #{i+1}'
    proof_url = f'https://proof.url/{i+1}'

    assistance_requests.append((
        beneficiary_id,
        charity_org_id,
        title,
        description,
        priority,
        start_date.strftime('%Y-%m-%d %H:%M:%S'),
        end_date.strftime('%Y-%m-%d %H:%M:%S'),
        status,
        receiving_status,
        created_at.strftime('%Y-%m-%d %H:%M:%S'),
        approved_by,
        approved_at.strftime('%Y-%m-%d %H:%M:%S') if approved_at else None,
        place,
        proof_url
    ))

cur.executemany('''
INSERT INTO app_assistancerequest 
(beneficiary_id, charity_org_id, title, description, priority, start_date, end_date, status, receiving_status, created_at, approved_by_id, approved_at, place, proof_url)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', assistance_requests)
conn.commit()

# Lấy AssistanceRequest IDs
cur.execute('SELECT id FROM app_assistancerequest')
assist_request_ids = [row[0] for row in cur.fetchall()]

# ========== 11. Tạo AssistanceRequestTypeMap ==========
artype_map_data = []
for arid in assist_request_ids:
    chosen_types = random.sample(artype_ids, random.randint(1,3))
    for tid in chosen_types:
        artype_map_data.append((arid, tid))
cur.executemany('INSERT INTO app_assistancerequesttypemap (assistance_request_id, type_id) VALUES (?, ?)', artype_map_data)
conn.commit()

# ========== 12. Tạo AssistanceRequestImage ==========
ari_data = []
fixed_img_url = 'https://aashritha.org/wp-content/uploads/2024/05/Untitled-design-17-1024x576.png'
for arid in assist_request_ids:
    for _ in range(random.randint(1,3)):
        ari_data.append((arid, fixed_img_url))
cur.executemany('INSERT INTO app_assistancerequestimage (assistance_request_id, image_url) VALUES (?, ?)', ari_data)
conn.commit()

# ========== 13. Tạo Event (15 bản ghi) ==========
event_statuses = ['pending', 'approved', 'rejected', 'completed']
events = []
for i in range(15):
    charity_org_id = random.choice(charityorg_ids)
    assistance_request_id = random.choice(assist_request_ids + [None])
    title = f'Sự kiện #{i+1}'
    description = f'Mô tả sự kiện #{i+1}'
    start_time = datetime.now() + timedelta(days=random.randint(1,20))
    end_time = start_time + timedelta(hours=random.randint(2,8))
    status = random.choice(event_statuses)
    created_at = datetime.now()
    approved_by = random.choice(nguoidung_ids + [None])
    approved_at = created_at if approved_by else None
    report_url = f'https://reports.example.com/{i+1}' if random.choice([True, False]) else None
    confirmed_by = random.choice([True, False])
    volunteers_number = random.randint(5, 50)

    events.append((
        charity_org_id,
        assistance_request_id,
        title,
        description,
        start_time.strftime('%Y-%m-%d %H:%M:%S'),
        end_time.strftime('%Y-%m-%d %H:%M:%S'),
        status,
        created_at.strftime('%Y-%m-%d %H:%M:%S'),
        approved_by,
        approved_at.strftime('%Y-%m-%d %H:%M:%S') if approved_at else None,
        report_url,
        int(confirmed_by),
        volunteers_number
    ))

cur.executemany('''
INSERT INTO app_event (charity_org_id, assistance_request_id, title, description, start_time, end_time, status, created_at, approved_by_id, approved_at, report_url, confirmed_by, volunteers_number)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', events)
conn.commit()

# Lấy Event IDs
cur.execute('SELECT id FROM app_event')
event_ids = [row[0] for row in cur.fetchall()]

# ========== 14. Tạo EventRegistration ==========

event_registrations = []
status_choices_er = ['pending', 'approved', 'rejected', 'completed']

for event_id in event_ids:
    # mỗi event có 3-5 volunteer đăng ký
    volunteers_for_event = random.sample(volunteer_ids, random.randint(3, 5))
    for vid in volunteers_for_event:
        status = random.choice(status_choices_er)
        registered_at = datetime.now() - timedelta(days=random.randint(1, 10))
        checked_in_at = registered_at + timedelta(hours=1) if status in ['approved', 'completed'] else None
        checked_out_at = checked_in_at + timedelta(hours=2) if status == 'completed' else None
        rating = random.randint(1, 5) if status == 'completed' else None
        review = f'Review cho sự kiện {event_id} của volunteer {vid}' if rating else None

        event_registrations.append((
            event_id,
            vid,
            status,
            registered_at.strftime('%Y-%m-%d %H:%M:%S'),
            checked_in_at.strftime('%Y-%m-%d %H:%M:%S') if checked_in_at else None,
            checked_out_at.strftime('%Y-%m-%d %H:%M:%S') if checked_out_at else None,
            rating,
            review
        ))

cur.executemany('''
INSERT INTO app_eventregistration 
(event_id, volunteer_id, status, registered_at, checked_in_at, checked_out_at, rating, review)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', event_registrations)
conn.commit()


conn.close()
print("Mockdata đã được tạo thành công!")
