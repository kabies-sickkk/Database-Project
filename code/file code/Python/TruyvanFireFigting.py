import mysql.connector

# Kết nối tới cơ sở dữ liệu MySQL
conn = mysql.connector.connect(
    host="127.0.0.1",          # Địa chỉ máy chủ MySQL
    user="root",               # Tên đăng nhập MySQL
    password="SQLdat1502:3",   # Mật khẩu MySQL
    database="fire_fighting"    # Tên cơ sở dữ liệu
)

cursor = conn.cursor()

# Định nghĩa các câu truy vấn
queries = {
    "sensors": "SELECT * FROM Fire_Fighting.sensors",
    "sensor_values": "SELECT * FROM Fire_Fighting.sensor_values",
    "timestamps": "SELECT * FROM Fire_Fighting.timestamps",
    "status": "SELECT * FROM Fire_Fighting.status"
}

# Thực hiện và hiển thị kết quả của từng truy vấn
for table_name, query in queries.items():
    print(f"\nDữ liệu từ bảng {table_name}:")

    # Thực hiện truy vấn
    cursor.execute(query)

    # Lấy tiêu đề của bảng (tên các cột)
    column_names = [i[0] for i in cursor.description]

    # Hiển thị tiêu đề của bảng
    print(f"| {' | '.join(column_names)} |")
    print("-" * 50)

    # Lấy và hiển thị các dòng dữ liệu
    rows = cursor.fetchall()
    for row in rows:
        print(f"| {' | '.join(str(value) for value in row)} |")

# Đóng cursor và kết nối sau khi hoàn thành
cursor.close()
conn.close()
