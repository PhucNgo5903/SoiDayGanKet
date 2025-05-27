import sqlite3

def insert_with_id(cursor, table, id_value, name):
    try:
        cursor.execute(f"INSERT INTO {table} (id, name) VALUES (?, ?)", (id_value, name))
    except sqlite3.IntegrityError as e:
        print(f"[{table}] Không thể thêm ({id_value}, {name}): {e}")

def insert_relationship(cursor, table, skill_id, area_id ):
    try:
        cursor.execute(f"INSERT INTO {table} (skill_id, support_area_id) VALUES (?, ?)", (skill_id, area_id))
    except sqlite3.IntegrityError as e:
        print(f"[{table}] Không thể thêm ({skill_id},{area_id}): {e}")

def main():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    # Insert app_supportarea
    with open("vv_data_source/app_supportarea.txt", "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) == 2:
                insert_with_id(cursor, "app_supportarea", int(parts[0]), parts[1])

    # Insert app_skill
    with open("vv_data_source/app_skill.txt", "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) == 2:
                insert_with_id(cursor, "app_skill", int(parts[0]), parts[1])

    # Insert relationships into app_skillssupportarea
    with open("vv_data_source/app_skillssupportarea.txt", "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) == 2:
                insert_relationship(cursor, "app_skillssupportarea", int(parts[0]), int(parts[1]))

    conn.commit()
    conn.close()
    print("Đã chèn dữ liệu thành công vào tất cả các bảng.")

if __name__ == "__main__":
    main()

# import sqlite3

# conn = sqlite3.connect('db.sqlite3')
# cursor = conn.cursor()

# cursor.execute("""

# DELETE FROM support_areas_volunteer_skills;


# """)
# conn.commit()
# conn.close()