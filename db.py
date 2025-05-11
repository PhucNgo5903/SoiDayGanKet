import sqlite3
from django.contrib.auth.hashers import make_password
from datetime import datetime
import os
import django
# Cấu hình Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'donenv.settings')
django.setup()

# Kết nối cơ sở dữ liệu
con = sqlite3.connect('db.sqlite3')
cur = con.cursor()

# Tạo mật khẩu mã hóa
password = make_password('123456')

# === Bảng auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) ===
users = [
    (1, password, None, 1, 'adminuser', 'Admin', 'User', 'admin@example.com', 1, 1, datetime.now()),
    (2, password, None, 0, 'voluser', 'Vol', 'User', 'vol@example.com', 0, 1, datetime.now()),
    (3, password, None, 0, 'charityuser', 'Charity', 'User', 'charity@example.com', 0, 1, datetime.now()),
    (4, password, None, 0, 'beneficiaryuser', 'Beneficiary', 'User', 'bene@example.com', 0, 1, datetime.now()),
    (5, password, None, 0, 'extrauser', 'Extra', 'User', 'extra@example.com', 0, 1, datetime.now()),
]

cur.executemany('''
INSERT INTO auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', users)

# === Bảng app_nguoidung ===
nguoidungs = [
    (1, password, 'admin', 'admin@example.com', '1990-01-01', '0123456789', 'Address 1', 'Admin user', 'active', datetime.now()),
    (2, password, 'volunteer', 'vol@example.com', '1992-02-02', '0123456790', 'Address 2', 'Volunteer user', 'active', datetime.now()),
    (3, password, 'charity', 'charity@example.com', '1993-03-03', '0123456791', 'Address 3', 'Charity user', 'active', datetime.now()),
    (4, password, 'beneficiary', 'bene@example.com', '1994-04-04', '0123456792', 'Address 4', 'Beneficiary user', 'active', datetime.now()),
    (5, password, 'volunteer', 'extra@example.com', '1995-05-05', '0123456793', 'Address 5', 'Extra user', 'inactive', datetime.now()),
]

cur.executemany('''
INSERT INTO app_nguoidung (id, password, role, email, dob, phone, address, description, status, created_at, user_id)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', [(i+1, *nguoidungs[i][1:], i+1) for i in range(5)])

# === Volunteer ===
cur.executemany('''
INSERT INTO app_volunteer (user_id, gender) VALUES (?, ?)
''', [(2, 'male'), (5, 'female')])

# === Beneficiary ===
cur.execute('INSERT INTO app_beneficiary (user_id, gender) VALUES (?, ?)', (4, 'female'))

# === CharityOrg ===
cur.execute('INSERT INTO app_charityorg (user_id, type, website) VALUES (?, ?, ?)', (3, 'local', 'https://charity.org'))

# === Skill ===
skills = [('Cooking',), ('Teaching',), ('Driving',), ('Cleaning',), ('Designing',)]
cur.executemany('INSERT INTO app_skill (name) VALUES (?)', skills)

# === VolunteerSkill ===
cur.executemany('INSERT INTO app_volunteerskill (volunteer_id, skill_id) VALUES (?, ?)', [
    (2, 1), (2, 2), (5, 3), (5, 4), (5, 5)
])

# === SupportArea ===
areas = [
    ('Food Supply',),
    ('Medical Support',),
    ('Education',),
    ('Legal Assistance',),
    ('Housing Support',)
]
cur.executemany('INSERT INTO app_supportarea (name) VALUES (?)', areas)


# === SkillsSupportArea ===
cur.executemany('INSERT INTO app_skillssupportarea (skill_id, support_area_id) VALUES (?, ?)', [
    (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)
])

# === CharityOrgSupportArea ===
cur.executemany('INSERT INTO app_charityorgsupportarea (charity_org_id, support_area_id) VALUES (?, ?)', [
    (3, 1), (3, 2), (3, 3), (3, 4), (3, 5)
])

# === AssistanceRequestType ===
types = [('Food',), ('Medical',), ('Shelter',), ('Education',), ('Transport',)]
cur.executemany('INSERT INTO app_assistancerequesttype (name) VALUES (?)', types)

# === AssistanceRequest ===
requests = [
    (4, 3, 'Need food', 'Requesting rice and noodles', 'high', 1715417600, 1715504000, 'pending', 'waiting', datetime.now(), 1, datetime.now(), 'Hanoi', 'http://proof.com/1', 'http://img.com/1'),
    (4, 3, 'Need medicine', 'Urgent medical supplies', 'medium', 1715417600, 1715504000, 'approved', 'received', datetime.now(), 1, datetime.now(), 'Danang', 'http://proof.com/2', 'http://img.com/2'),
    (4, 3, 'Need shelter', 'Temporary housing needed', 'low', 1715417600, 1715504000, 'approved', 'waiting', datetime.now(), 1, datetime.now(), 'Hue', 'http://proof.com/3', 'http://img.com/3'),
    (4, 3, 'Need education', 'School support', 'medium', 1715417600, 1715504000, 'pending', 'waiting', datetime.now(), 1, datetime.now(), 'HCM', 'http://proof.com/4', 'http://img.com/4'),
    (4, 3, 'Need transport', 'Bus tickets', 'low', 1715417600, 1715504000, 'pending', 'received', datetime.now(), 1, datetime.now(), 'Can Tho', 'http://proof.com/5', 'http://img.com/5'),
]
cur.executemany('''
INSERT INTO app_assistancerequest (
    beneficiary_id, charity_org_id, title, description, priority, start_date, end_date, status, receive, created_at,
    approved_by_id, approved_at, place, proof_url, image
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', requests)

# === AssistanceRequestTypeMap ===
cur.executemany('''
INSERT INTO app_assistancerequesttypemap (assistance_request_id, type_id) VALUES (?, ?)
''', [(1,1), (2,2), (3,3), (4,4), (5,5)])

# === Event ===
events = [
    (3, 1, 'Food Distribution', 'Distribute food packages', '2025-05-20 10:00:00', '2025-05-20 15:00:00', 'pending', datetime.now(), 1, datetime.now(), None, 10),
    (3, 2, 'Medical Camp', 'Provide medical aid', '2025-05-21 09:00:00', '2025-05-21 14:00:00', 'approved', datetime.now(), 1, datetime.now(), 'http://report.com/1', 8),
    (3, 3, 'Shelter Setup', 'Set up tents', '2025-05-22 08:00:00', '2025-05-22 12:00:00', 'completed', datetime.now(), 1, datetime.now(), 'http://report.com/2', 6),
    (3, 4, 'Teaching Session', 'Teach children', '2025-05-23 13:00:00', '2025-05-23 17:00:00', 'pending', datetime.now(), 1, datetime.now(), '', 5),
    (3, 5, 'Transport Help', 'Drive people to safe place', '2025-05-24 10:00:00', '2025-05-24 12:00:00', 'approved', datetime.now(), 1, datetime.now(), '', 7),
]
cur.executemany('''
INSERT INTO app_event (
    charity_org_id, assistance_request_id, title, description, start_time, end_time, status, created_at,
    approved_by_id, approved_at, report_url, volunteers_number
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', events)

# === EventRegistration ===
registrations = [
    (1, 2, 'pending', datetime.now(), None, None, None, None),
    (2, 2, 'approved', datetime.now(), datetime.now(), None, 5, 'Great job!'),
    (3, 5, 'completed', datetime.now(), datetime.now(), datetime.now(), 4, 'Good'),
    (4, 2, 'pending', datetime.now(), None, None, None, None),
    (5, 5, 'approved', datetime.now(), datetime.now(), None, 5, 'Nice'),
]
cur.executemany('''
INSERT INTO app_eventregistration (
    event_id, volunteer_id, status, registered_at, checked_in_at, checked_out_at, rating, review
) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', registrations)

# Lưu thay đổi và đóng kết nối
con.commit()
con.close()
