import os
import django
import sqlite3
from django.contrib.auth.hashers import make_password
from datetime import datetime
import random

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'donenv.settings')  # ← sửa lại tên project nếu cần
django.setup()

# Kết nối SQLite
con = sqlite3.connect('db.sqlite3')
cur = con.cursor()

# ========== Tạo Users ==========
user_data = []
for i in range(1, 21):
    username = f'user{i}'
    password = make_password(f'Pass{i}123')
    email = f'user{i}@gmail.com'
    first_name = f'User{i}'
    last_name = 'Test'
    user_data.append((password, username, 0, 0, 1, last_name, email, '2025-05-01 00:00:00', first_name))

cur.executemany('''
    INSERT INTO auth_user (password, username, is_superuser, is_staff, is_active, last_name, email, date_joined, first_name)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', user_data)

# Lấy ID vừa thêm
cur.execute('SELECT id FROM auth_user ORDER BY id DESC LIMIT 20')
user_ids = [row[0] for row in cur.fetchall()][::-1]  # đảo ngược lại cho đúng thứ tự

# ========== Tạo NguoiDung ==========
roles = ['admin', 'volunteer', 'charity', 'beneficiary']
statuses = ['active', 'inactive']
nguoidung_data = []

for i, user_id in enumerate(user_ids):
    role = roles[i % len(roles)]
    status = statuses[i % len(statuses)]
    dob = f"199{i % 10}-01-01"
    nguoidung_data.append((
        user_id,
        make_password(f'Pass{i+1}123'),
        role,
        f'user{i+1}@gmail.com',
        dob,
        f'09123456{i:02}',
        f'Địa chỉ {i+1}',
        f'Mô tả user {i+1}',
        status,
        '2025-05-01 00:00:00'
    ))

cur.executemany('''
    INSERT INTO app_nguoidung (user_id, password, role, email, dob, phone, address, description, status, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', nguoidung_data)

# ========== Volunteer ==========
volunteers = []
for i in range(len(user_ids)):
    if nguoidung_data[i][2] == 'volunteer':
        gender = random.choice(['male', 'female', 'other'])
        volunteers.append((user_ids[i], gender))

cur.executemany('''
    INSERT INTO app_volunteer (user_id, gender)
    VALUES (?, ?)
''', volunteers)

# ========== Beneficiary ==========
beneficiaries = []
for i in range(len(user_ids)):
    if nguoidung_data[i][2] == 'beneficiary':
        gender = random.choice(['male', 'female', 'other'])
        beneficiaries.append((user_ids[i], gender))

cur.executemany('''
    INSERT INTO app_beneficiary (user_id, gender)
    VALUES (?, ?)
''', beneficiaries)

# ========== CharityOrg ==========
charities = []
org_types = ['local', 'national', 'international']
for i in range(len(user_ids)):
    if nguoidung_data[i][2] == 'charity':
        org_type = org_types[i % len(org_types)]
        charities.append((user_ids[i], org_type, f'https://charity{i+1}.org'))

cur.executemany('''
    INSERT INTO app_charityorg (user_id, type, website)
    VALUES (?, ?, ?)
''', charities)

# ========== Skill ==========
skills = [("Tổ chức"), ("Y tế"), ("Giáo dục"), ("Nấu ăn"), ("Thiết kế"), ("Lập trình")]
cur.executemany('''
    INSERT INTO app_skill (name) VALUES (?)
''', [(s,) for s in skills])

# ========== SupportArea ==========
support_areas = [("Nông thôn"), ("Thành phố"), ("Miền núi"), ("Biên giới"), ("Hải đảo")]
cur.executemany('''
    INSERT INTO app_supportarea (name) VALUES (?)
''', [(s,) for s in support_areas])

# ========== Commit và đóng ==========
con.commit()
con.close()
print("✅ Đã chèn dữ liệu mẫu vào cơ sở dữ liệu!")
Mở lại kết nối
con = sqlite3.connect('db.sqlite3')
cur = con.cursor()

# Lấy các id cần thiết
cur.execute('SELECT id FROM app_skill')
skill_ids = [row[0] for row in cur.fetchall()]

cur.execute('SELECT id FROM app_supportarea')
area_ids = [row[0] for row in cur.fetchall()]

cur.execute('SELECT user_id FROM app_volunteer')
volunteer_ids = [row[0] for row in cur.fetchall()]

cur.execute('SELECT user_id FROM app_charityorg')
charity_ids = [row[0] for row in cur.fetchall()]

cur.execute('SELECT user_id FROM app_beneficiary')
beneficiary_ids = [row[0] for row in cur.fetchall()]

# ========== VolunteerSkill ==========
volunteer_skills = []
for vid in volunteer_ids:
    chosen_skills = random.sample(skill_ids, k=random.randint(1, 3))
    for sid in chosen_skills:
        volunteer_skills.append((vid, sid))
cur.executemany('INSERT INTO app_volunteerskill (volunteer_id, skill_id) VALUES (?, ?)', volunteer_skills)

# ========== SkillsSupportArea ==========
skill_area_links = []
for sid in skill_ids:
    for aid in random.sample(area_ids, k=2):
        skill_area_links.append((sid, aid))
cur.executemany('INSERT INTO app_skillssupportarea (skill_id, support_area_id) VALUES (?, ?)', skill_area_links)

# ========== CharityOrgSupportArea ==========
charity_area_links = []
for cid in charity_ids:
    for aid in random.sample(area_ids, k=2):
        charity_area_links.append((cid, aid))
cur.executemany('INSERT INTO app_charityorgsupportarea (charity_org_id, support_area_id) VALUES (?, ?)', charity_area_links)

# ========== AssistanceRequestType ==========
types = ['Lương thực', 'Y tế', 'Giáo dục', 'Chỗ ở', 'Việc làm']
cur.executemany('INSERT INTO app_assistancerequesttype (name) VALUES (?)', [(t,) for t in types])

cur.execute('SELECT id FROM app_assistancerequesttype')
type_ids = [row[0] for row in cur.fetchall()]

# ========== AssistanceRequest ==========
requests = []
request_type_map = []
for i in range(10):
    b_id = random.choice(beneficiary_ids)
    c_id = random.choice(charity_ids)
    title = f'Hỗ trợ {i+1}'
    priority = random.choice(['low', 'medium', 'high'])
    status = random.choice(['pending', 'approved', 'rejected'])
    receive = random.choice(['waiting', 'received'])
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    place = f'Khu vực {i+1}'
    proof_url = f'https://example.com/proof{i+1}.pdf'
    image = f'https://example.com/image{i+1}.jpg'

    cur.execute('''
        INSERT INTO app_assistancerequest (
            beneficiary_id, charity_org_id, title, description, priority,
            start_date, end_date, status, receive, created_at, place, proof_url, image
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        b_id, c_id, title, f'Mô tả yêu cầu {i+1}', priority,
        '2025-05-20', '2025-06-20', status, receive, created_at,
        place, proof_url, image
    ))

    request_id = cur.lastrowid
    for tid in random.sample(type_ids, k=2):
        request_type_map.append((request_id, tid))

cur.executemany('INSERT INTO app_assistancerequesttypemap (assistance_request_id, type_id) VALUES (?, ?)', request_type_map)

# ========== Event ==========
events = []
for i in range(5):
    c_id = random.choice(charity_ids)
    title = f'Sự kiện {i+1}'
    status = random.choice(['pending', 'approved', 'completed'])
    confirmed = True
    volunteers_number = random.randint(2, 5)
    events.append((
        c_id, title, f'Mô tả sự kiện {i+1}', '2025-06-01 08:00:00',
        '2025-06-01 12:00:00', status, datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        confirmed, volunteers_number
    ))

cur.executemany('''
    INSERT INTO app_event (
        charity_org_id, title, description, start_time, end_time,
        status, created_at, confirmed_by, volunteers_number
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', events)

cur.execute('SELECT id FROM app_event')
event_ids = [row[0] for row in cur.fetchall()]

# ========== EventRegistration ==========
event_regs = []
for eid in event_ids:
    for vid in random.sample(volunteer_ids, k=3):
        status = random.choice(['pending', 'approved', 'completed'])
        event_regs.append((eid, vid, status, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

cur.executemany('''
    INSERT INTO app_eventregistration (event_id, volunteer_id, status, registered_at)
    VALUES (?, ?, ?, ?)
''', event_regs)

# ========== Commit ==========
con.commit()
con.close()
print("✅ Đã bổ sung dữ liệu cho các bảng còn thiếu!")
