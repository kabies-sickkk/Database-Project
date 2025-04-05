import mysql.connector
import tkinter as tk
from tkinter import ttk

# Hàm để thực hiện truy vấn JOIN và hiển thị dữ liệu trong Treeview
def show_combined_data():
    query = """
    SELECT 
        s.Sensor_id,
        s.Temperature_sensor,
        s.Smoke_sensor,
        t.Time_id,
        t.Date,
        t.Time,
        st.Status_id,
        st.Temperature_value,
        st.Smoke_value,
        st.Temperature_Warning,
        st.Smoke_Warning,
        st.Decision
    FROM 
        Fire_Fighting.sensors AS s
    JOIN 
        Fire_Fighting.timestamps AS t ON s.Sensor_id = t.Sensor_id
    JOIN 
        Fire_Fighting.status AS st ON s.Sensor_id = st.Sensor_id;
    """
    
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="SQLdat1502:3",
        database="fire_fighting"
    )
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    # Xóa dữ liệu cũ trên Treeview
    for row in tree_combined.get_children():
        tree_combined.delete(row)

    # Hiển thị dữ liệu mới
    for row in rows:
        tree_combined.insert("", "end", values=row)

    cursor.close()
    conn.close()

# Tạo giao diện tkinter
root = tk.Tk()
root.title("Dữ liệu Kết hợp từ Các Bảng Sensors, Timestamps và Status")
root.geometry("1200x400")

# Nút để tải dữ liệu
btn_show_data = tk.Button(root, text="Hiện dữ liệu cảm biến", command=show_combined_data)
btn_show_data.pack(pady=10)

# Cấu hình Treeview cho dữ liệu kết hợp
columns_combined = (
    "Sensor_id", "Temperature_sensor", "Smoke_sensor",
    "Time_id", "Date", "Time",
    "Status_id", "Temperature_value", "Smoke_value",
    "Temperature_Warning", "Smoke_Warning", "Decision"
)
tree_combined = ttk.Treeview(root, columns=columns_combined, show="headings", height=15)
tree_combined.pack(expand=True, fill="both")

# Đặt tiêu đề cho các cột
for col in columns_combined:
    tree_combined.heading(col, text=col)

# Thiết lập kích thước cho các cột
for col in columns_combined:
    tree_combined.column(col, width=100, anchor="center")

# Chạy giao diện
root.mainloop()
