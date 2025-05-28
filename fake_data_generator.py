import sqlite3
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'donenv.settings')
from django.contrib.auth.hashers import make_password
from datetime import datetime

def insert_auth_user(cursor, id, username, raw_password, email, is_staff=False, is_superuser=False, is_active=True):
    try:
        hashed_pw = make_password(raw_password)
        cursor.execute("""
            INSERT INTO auth_user (
                id, password, last_login, is_superuser, username, first_name, last_name,
                email, is_staff, is_active, date_joined
            ) VALUES (?, ?, NULL, ?, ?, '', '', ?, ?, ?, datetime('now'))
        """, (id, hashed_pw, int(is_superuser), username, email, int(is_staff), int(is_active)))
    except sqlite3.IntegrityError as e:
        print(f"[auth_user] Lỗi khi thêm user ID {id}: {e}")

def insert_nguoidung(cursor, user_id, role, dob, phone, address, description, status, avatar_url):
    try:
        cursor.execute("""
            INSERT INTO app_nguoidung (
                user_id, role, dob, phone, address, description, status, created_at, avatar_url
            ) VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'), ?)
        """, (user_id, role, dob, phone, address, description, status, avatar_url))
    except sqlite3.IntegrityError as e:
        print(f"[app_nguoidung] Lỗi khi thêm user_id {user_id}: {e}")

def insert_users_and_nguoidung():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    with open("vv_data_source/app_nguoidung.txt", "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) != 11:
                print(f"Dòng không hợp lệ: {line.strip()}")
                continue

            id = int(parts[0])
            username = parts[1]
            raw_password = parts[2]  # Nên là hashed (nếu chưa hash, dùng mật khẩu đơn giản tạm)
            email = parts[3]
            role = parts[4]
            dob = parts[5]
            phone = parts[6]
            address = parts[7]
            description = parts[8]
            status = parts[9]
            avatar_url = parts[10]

            # Xác định quyền
            is_staff = role == "admin"
            is_superuser = role == "admin"

            # Insert auth_user
            insert_auth_user(cursor, id, username, raw_password, email, is_staff, is_superuser)

            # Insert app_nguoidung
            insert_nguoidung(cursor, id, role, dob, phone, address, description, status, avatar_url)

    conn.commit()
    conn.close()
    print("Đã chèn xong dữ liệu người dùng.")

def insert_volunteer(cursor, user_id, gender):
    try:
        cursor.execute("INSERT INTO app_volunteer (user_id, gender) VALUES (?, ?)", (user_id, gender))
    except sqlite3.IntegrityError as e:
        print(f"[app_volunteer] Lỗi khi thêm {user_id}: {e}")

def insert_beneficiary(cursor, user_id, gender):
    try:
        cursor.execute("INSERT INTO app_beneficiary (user_id, gender) VALUES (?, ?)", (user_id, gender))
    except sqlite3.IntegrityError as e:
        print(f"[app_beneficiary] Lỗi khi thêm {user_id}: {e}")

def insert_charityorg(cursor, user_id, org_type, website):
    try:
        cursor.execute("INSERT INTO app_charityorg (user_id, type, website) VALUES (?, ?, ?)", (user_id, org_type, website))
    except sqlite3.IntegrityError as e:
        print(f"[app_charityorg] Lỗi khi thêm {user_id}: {e}")

def insert_skill(cursor):
    with open("vv_data_source/app_skill.txt", "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) == 2:
                try:
                    cursor.execute("INSERT INTO app_skill (id, name) VALUES (?, ?)", (int(parts[0]), parts[1]))
                except sqlite3.IntegrityError as e:
                    print(f"[app_skill] Lỗi khi thêm ({parts[0]}, {parts[1]}): {e}")

def insert_assistance_types(cursor):
    with open("vv_data_source/app_assistancerequesttype.txt", "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) == 2:
                try:
                    cursor.execute("INSERT INTO app_assistancerequesttype (id, name) VALUES (?, ?)", (int(parts[0]), parts[1]))
                except sqlite3.IntegrityError as e:
                    print(f"[app_assistancerequesttype] Lỗi khi thêm ({parts[0]}, {parts[1]}): {e}")
def insert_volunteerskill_from_txt(cursor, file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            user_id, skill_id = map(int, line.strip().split("|"))
            try:
                cursor.execute("INSERT INTO app_volunteerskill (volunteer_id, skill_id) VALUES (?, ?)", (user_id, skill_id))
            except sqlite3.IntegrityError as e:
                print(f"[app_volunteerskill] Lỗi khi thêm ({user_id}, {skill_id}): {e}")
def insert_skillassistancerequesttype_from_txt(cursor, file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            skill_id, type_id = map(int, line.strip().split("|"))
            try:
                cursor.execute("INSERT INTO app_skillassistancerequesttype (skill_id, assistance_request_type_id) VALUES (?, ?)", (skill_id, type_id))
            except sqlite3.IntegrityError as e:
                print(f"[app_skillassistancerequesttype] Lỗi khi thêm ({skill_id}, {type_id}): {e}")
def insert_charityorgassistancerequesttype_from_txt(cursor, file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            charityorg_id, type_id = map(int, line.strip().split("|"))
            try:
                cursor.execute("INSERT INTO app_charityorgassistancerequesttype (charity_org_id, assistance_request_type_id) VALUES (?, ?)", (charityorg_id, type_id))
            except sqlite3.IntegrityError as e:
                print(f"[app_charityorgassistancerequesttype] Lỗi khi thêm ({charityorg_id}, {type_id}): {e}")
def insert_assistancerequest(cursor, id, beneficiary_id, charity_org_id, title, description, priority,
                              start_date, end_date, status, receiving_status,
                              update_by_id, update_status_at, place, proof_url, admin_remark):
    try:
        cursor.execute("""
            INSERT INTO app_assistancerequest (
                id, beneficiary_id, charity_org_id, title, description, priority,
                start_date, end_date, status, receiving_status,
                update_by_id, update_status_at, place, proof_url, admin_remark,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
        """, (
            id,
            beneficiary_id,
            charity_org_id if charity_org_id else None,
            title,
            description,
            priority,
            start_date,
            end_date,
            status,
            receiving_status,
            update_by_id if update_by_id else None,
            update_status_at if update_status_at else None,
            place,
            proof_url,
            admin_remark
        ))
    except Exception as e:
        print(f"[app_assistancerequest] Lỗi khi thêm ID {id}: {e}")

def insert_assistancerequesttypemap(cursor, assistancerequest_id, assistancerequesttype_id):
    try:
        cursor.execute("""
            INSERT INTO app_assistancerequesttypemap (assistance_request_id, type_id)
            VALUES (?, ?)
        """, (assistancerequest_id, assistancerequesttype_id))
    except sqlite3.IntegrityError as e:
        print(f"[app_assistancerequesttypemap] Lỗi khi thêm ({assistancerequest_id}, {assistancerequesttype_id}): {e}")

def insert_assistancerequestimage(cursor, id, assistancerequest_id, image_path):
    try:
        cursor.execute("""
            INSERT INTO app_assistancerequestimage (id, assistance_request_id, image_url)
            VALUES (?, ?, ?)
        """, (id, assistancerequest_id, image_path))
    except sqlite3.IntegrityError as e:
        print(f"[app_assistancerequestimage] Lỗi khi thêm ảnh {id}: {e}")

def insert_event(cursor, id, charity_org_id, assistance_request_id, title, description, start_time, end_time,
                 status, approved_by, approved_at, report_url, confirmed_by, volunteers_number, reason):
    try:
        cursor.execute(
            """
            INSERT INTO app_event (
                id, charity_org_id, assistance_request_id, title, description, start_time, end_time,
                status, approved_by_id, approved_at, report_url, confirmed_by, volunteers_number, reason, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
            """,
            (id, charity_org_id, assistance_request_id, title, description, start_time, end_time,
             status, approved_by, approved_at, report_url, confirmed_by, volunteers_number, reason)
        )
    except sqlite3.IntegrityError as e:
        print(f"[app_event] Lỗi khi thêm ID {id}: {e}")

def insert_eventregistration(cursor, id, event_id, volunteer_id, status, registered_at,
                             checked_in_at, checked_out_at, rating, review):
    try:
        cursor.execute(
            """
            INSERT INTO app_eventregistration (
                id, event_id, volunteer_id, status, registered_at, checked_in_at,
                checked_out_at, rating, review
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (id, event_id, volunteer_id, status, registered_at, checked_in_at,
             checked_out_at, rating, review)
        )
    except sqlite3.IntegrityError as e:
        print(f"[app_eventregistration] Lỗi khi thêm ID {id}: {e}")

def main():
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()

    # Insert NguoiDung
    with open("vv_data_source/app_nguoidung.txt", "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) == 8:
                insert_nguoidung(cursor, int(parts[0]), parts[1], parts[2], parts[3], parts[4], parts[5], parts[6], parts[7])

    insert_users_and_nguoidung()
    # Insert Volunteer
    with open("vv_data_source/app_volunteer.txt", "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) == 2:
                insert_volunteer(cursor, int(parts[0]), parts[1])

    # Insert Beneficiary
    with open("vv_data_source/app_beneficiary.txt", "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) == 2:
                insert_beneficiary(cursor, int(parts[0]), parts[1])

    # Insert CharityOrg
    with open("vv_data_source/app_charityorg.txt", "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) == 3:
                insert_charityorg(cursor, int(parts[0]), parts[1], parts[2])
    insert_skill(cursor)
    insert_assistance_types(cursor)
    insert_volunteerskill_from_txt(cursor, "vv_data_source/app_volunteerskill.txt")
    insert_skillassistancerequesttype_from_txt(cursor, "vv_data_source/app_skillassistancerequesttype.txt")
    insert_charityorgassistancerequesttype_from_txt(cursor, "vv_data_source/app_charityorgassistancerequesttype.txt")
        # Insert app_assistancerequest
    with open("vv_data_source/app_assistancerequest.txt", "r", encoding="utf-8") as f:
        for line in f:
            fields = line.strip().split("|")
            if len(fields) != 15:
                print(f"[SKIP] Dòng sai định dạng: {line}")
                continue

            id = int(fields[0])
            beneficiary_id = int(fields[1])
            charity_org_id = int(fields[2]) if fields[2] else None
            title = fields[3]
            description = fields[4]
            priority = fields[5]
            start_date = fields[6]
            end_date = fields[7]
            status = fields[8]
            receiving_status = fields[9]
            update_by_id = int(fields[10]) if fields[10] else None
            update_status_at = fields[11] if fields[11] else None
            place = fields[12]
            proof_url = fields[13]
            admin_remark = fields[14]

            insert_assistancerequest(
                cursor, id, beneficiary_id, charity_org_id, title, description,
                priority, start_date, end_date, status, receiving_status,
                update_by_id, update_status_at, place, proof_url, admin_remark
            )

    # Insert app_assistancerequesttypemap
    with open("vv_data_source/app_assistancerequesttypemap.txt", "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) == 2:
                assistancerequest_id = int(parts[0])
                assistancerequesttype_id = int(parts[1])
                insert_assistancerequesttypemap(cursor, assistancerequest_id, assistancerequesttype_id)

    # Insert app_assistancerequestimage
    with open("vv_data_source/app_assistancerequestimage.txt", "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) == 3:
                id = int(parts[0])
                assistancerequest_id = int(parts[1])
                image_path = parts[2]
                insert_assistancerequestimage(cursor, id, assistancerequest_id, image_path)
    # ===== Insert app_event =====
    with open('vv_data_source/app_event.txt', 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) == 14:
                id = int(parts[0])
                charity_org_id = int(parts[1])
                assistance_request_id = int(parts[2]) if parts[2] else None
                title = parts[3]
                description = parts[4]
                start_time = parts[5]
                end_time = parts[6]
                status = parts[7]
                approved_by = int(parts[8]) if parts[8] else None
                approved_at = parts[9] if parts[9] else None
                report_url = parts[10] if parts[10] else None
                confirmed_by = parts[11].lower() == 'true'
                volunteers_number = int(parts[12])
                reason = parts[13] if parts[13] else None

                insert_event(cursor, id, charity_org_id, assistance_request_id, title, description,
                             start_time, end_time, status, approved_by, approved_at, report_url,
                             confirmed_by, volunteers_number, reason)

    # ===== Insert app_eventregistration =====
    with open('vv_data_source/app_eventregistration.txt', 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) == 9:
                id = int(parts[0])
                event_id = int(parts[1])
                volunteer_id = int(parts[2])
                status = parts[3]
                registered_at = parts[4]
                checked_in_at = parts[5] if parts[5] else None
                checked_out_at = parts[6] if parts[6] else None
                rating = int(parts[7]) if parts[7] else None
                review = parts[8] if parts[8] else None

                insert_eventregistration(cursor, id, event_id, volunteer_id, status,
                                         registered_at, checked_in_at, checked_out_at,
                                         rating, review)
    conn.commit()
    conn.close()
    print("✅ Đã chèn dữ liệu thành công vào các bảng")

if __name__ == "__main__":
    main()
