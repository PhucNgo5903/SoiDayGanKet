import os
import django
import sqlite3
from django.contrib.auth.hashers import make_password

# Cấu hình Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Gr18_QLTPChungCu.settings')
django.setup()

# Kết nối hoặc tạo mới file cơ sở dữ liệu
con = sqlite3.connect('db.sqlite3')
cur = con.cursor()

# Chèn dữ liệu vào bảng User (mã hóa mật khẩu)
password1 = make_password('ABC123')  # Mã hóa mật khẩu
password2 = make_password('XYZ123')  # Mã hóa mật khẩu
password3 = make_password('LMN123')  # Mã hóa mật khẩu

# Chèn 3 user với các mật khẩu khác nhau
cur.execute('''
    INSERT INTO auth_user (password, username, is_superuser, is_staff, is_active, last_name, email, date_joined, first_name) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', (password1, 'admin1', 1, 1, 1, 'Huyen', 'admin1@gmail.com', '2025-05-08 14:54:11', 'Admin1'))
cur.execute('''
    INSERT INTO auth_user (password, username, is_superuser, is_staff, is_active, last_name, email, date_joined, first_name) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', (password2, 'admin2', 0, 1, 1, 'Linh', 'admin2@gmail.com', '2025-05-08 14:54:11', 'Admin2'))
cur.execute('''
    INSERT INTO auth_user (password, username, is_superuser, is_staff, is_active, last_name, email, date_joined, first_name) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', (password3, 'admin3', 0, 1, 1, 'Nam', 'admin3@gmail.com', '2025-05-08 14:54:11', 'Admin3'))

# Chèn dữ liệu vào bảng NguoiDung cho 3 vai trò
user_ids = [4, 5, 6]  # giả sử user_id là 1, 2, 3
roles = ['Quản trị hệ thống', 'BQL Chung cư', 'Kế toán']
for user_id, role in zip(user_ids, roles):
    cur.execute('''
        INSERT INTO apartment_management_nguoidung (user_id, vai_tro, so_dien_thoai, trang_thai) 
        VALUES (?, ?, ?, ?)
    ''', (user_id, role, f'012345678{user_id}', 'Đang hoạt động'))

# Chèn dữ liệu vào bảng HoGiaDinh
for i in range(1, 4):
    cur.execute('''
        INSERT INTO apartment_management_hogiadinh (id_chu_ho_id, so_can_ho, dien_tich, ghi_chu, thoi_gian_bat_dau_o, thoi_gian_ket_thuc_o, trang_thai) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (i, 101 + i, 50.0 + i, f'Ghi chú căn hộ {101 + i}', '2025-01-01', '2025-12-31', 'Đang ở'))

# Chèn dữ liệu vào bảng DanCu
for i in range(1, 4):
    cur.execute('''
        INSERT INTO apartment_management_dancu (ho_gia_dinh_id, ho_ten, ngay_sinh, gioi_tinh, ma_can_cuoc, so_dien_thoai, trang_thai, thoi_gian_chuyen_den, thoi_gian_chuyen_di) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (i, f'Nguyen Thi Lan {i}', '1990-05-05', 'Nữ', f'12345678{i}', f'0123456789{i}', 'Đang sinh sống', '2025-01-01', '2025-12-31'))

# Chèn dữ liệu vào bảng KhoanThu
for i in range(1, 4):
    cur.execute('''
        INSERT INTO apartment_management_khoanthu (ten_khoan_thu, loai_khoan_thu, ghi_chu) 
        VALUES (?, ?, ?)
    ''', (f'Phí quản lý {i}', 'Bắt buộc', f'Phí quản lý hàng tháng {i}'))

# Chèn dữ liệu vào bảng DotThu
for i in range(1, 4):
    cur.execute('''
        INSERT INTO apartment_management_dotthu (khoan_thu_id, ten_dot_thu, noi_dung, thoi_gian_bat_dau, thoi_gian_ket_thuc, trang_thai) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (i, f'Đợt thu tháng {i}', f'Thu phí quản lý tháng {i}', f'2025-05-01', f'2025-05-31', 'Đang tiến hành'))

# Chèn dữ liệu vào bảng ChiTietThu
for i in range(1, 4):
    cur.execute('''
        INSERT INTO apartment_management_chitietthu (dot_thu_id, ho_gia_dinh_id, so_tien_can_nop, trang_thai_nop, ngay_nop) 
        VALUES (?, ?, ?, ?, ?)
    ''', (i, i, 500000 + (i * 100000), 'chưa nộp', None))

# Chèn dữ liệu vào bảng TamTruTamVang
for i in range(1, 4):
    cur.execute('''
        INSERT INTO apartment_management_tamtrutamvang (dan_cu_id, loai_tttv, thoi_gian_bat_dau, thoi_gian_ket_thuc, ly_do) 
        VALUES (?, ?, ?, ?, ?)
    ''', (i, 'Tạm trú', '2025-05-01', '2025-05-10', f'Công tác công ty {i}'))

# Chèn dữ liệu vào bảng PhuongTien
for i in range(1, 4):
    cur.execute('''
        INSERT INTO apartment_management_phuongtien (ho_gia_dinh_id, loai_phuong_tien, bien_so, mau, mo_ta) 
        VALUES (?, ?, ?, ?, ?)
    ''', (i, 'Ô tô', f'29A-1234{i}', 'Đen', f'Xe ô tô gia đình {i}'))

# Lưu thay đổi và đóng kết nối
con.commit()
con.close()

print("Dữ liệu đã được thêm vào!")
