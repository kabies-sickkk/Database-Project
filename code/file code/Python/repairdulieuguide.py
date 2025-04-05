import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox

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
        fire_fighting.sensors AS s
    JOIN 
        fire_fighting.timestamps AS t ON s.Sensor_id = t.Sensor_id
    JOIN 
        fire_fighting.status AS st ON s.Sensor_id = st.Sensor_id;
    """
    
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="SQLdat1502:3",
            database="fire_fighting"  # Đảm bảo tên cơ sở dữ liệu chính xác
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

    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi truy vấn", f"Không thể truy vấn dữ liệu: {err}")
    finally:
        cursor.close()
        conn.close()

# Hàm để thêm dữ liệu vào bảng
def insert_data():
    temperature_value = entry_temperature.get()
    smoke_value = entry_smoke.get()

    if not temperature_value or not smoke_value:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
        return

    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="SQLdat1502:3",
            database="fire_fighting"  # Đảm bảo tên cơ sở dữ liệu chính xác
        )
        cursor = conn.cursor()

        # Tìm Sensor_id lớn nhất để tự động tăng
        cursor.execute("SELECT MAX(Sensor_id) FROM fire_fighting.sensors")
        max_sensor_id = cursor.fetchone()[0] or 0
        new_sensor_id = max_sensor_id + 1
        temperature_sensor_name = f"Temp Sensor {new_sensor_id}"
        smoke_sensor_name = f"Smoke Sensor {new_sensor_id}"

        # Thêm vào bảng sensors
        cursor.execute(""" 
            INSERT INTO fire_fighting.sensors (Sensor_id, Temperature_sensor, Smoke_sensor) 
            VALUES (%s, %s, %s);
        """, (new_sensor_id, temperature_sensor_name, smoke_sensor_name))

        # Thêm vào bảng sensor_values
        cursor.execute(""" 
            INSERT INTO fire_fighting.sensor_values (Sensor_id, Temperature_value, Smoke_value) 
            VALUES (%s, %s, %s);
        """, (new_sensor_id, temperature_value, smoke_value))

        conn.commit()
        messagebox.showinfo("Thành công", "Dữ liệu đã được thêm thành công!")
        entry_temperature.delete(0, tk.END)
        entry_smoke.delete(0, tk.END)
        show_combined_data()

    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi thêm dữ liệu", f"Không thể thêm dữ liệu: {err}")
    finally:
        cursor.close()
        conn.close()

# Hàm để xóa dữ liệu dựa trên Sensor_id
def delete_data():
    selected_item = tree_combined.selection()
    if not selected_item:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn một mục để xóa!")
        return

    sensor_id = tree_combined.item(selected_item, "values")[0]  # Lấy Sensor_id từ mục đã chọn

    if messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa dữ liệu với Sensor_id: {sensor_id}?"):
        try:
            conn = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="SQLdat1502:3",
                database="fire_fighting"  # Đảm bảo tên cơ sở dữ liệu chính xác
            )
            cursor = conn.cursor()

            # Xóa dữ liệu từ bảng status trước
            cursor.execute("DELETE FROM fire_fighting.status WHERE Sensor_id = %s;", (sensor_id,))
            # Xóa dữ liệu từ bảng sensor_values
            cursor.execute("DELETE FROM fire_fighting.sensor_values WHERE Sensor_id = %s;", (sensor_id,))
            # Xóa dữ liệu từ bảng timestamps
            cursor.execute("DELETE FROM fire_fighting.timestamps WHERE Sensor_id = %s;", (sensor_id,))
            # Xóa dữ liệu từ bảng sensors
            cursor.execute("DELETE FROM fire_fighting.sensors WHERE Sensor_id = %s;", (sensor_id,))

            conn.commit()
            messagebox.showinfo("Thành công", "Dữ liệu đã được xóa thành công!")
            show_combined_data()

        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi xóa dữ liệu", f"Không thể xóa dữ liệu: {err}")
        finally:
            cursor.close()
            conn.close()

# Hàm để sửa dữ liệu dựa trên Sensor_id
def edit_data():
    selected_item = tree_combined.selection()
    if not selected_item:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn một mục để sửa!")
        return

    sensor_id = tree_combined.item(selected_item, "values")[0]  # Lấy Sensor_id từ mục đã chọn
    new_temperature_value = entry_temperature.get()
    new_smoke_value = entry_smoke.get()

    if not new_temperature_value or not new_smoke_value:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
        return

    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="SQLdat1502:3",
            database="fire_fighting"  # Đảm bảo tên cơ sở dữ liệu chính xác
        )
        cursor = conn.cursor()

        # Cập nhật dữ liệu trong bảng sensor_values
        cursor.execute("""
            UPDATE fire_fighting.sensor_values 
            SET Temperature_value = %s, Smoke_value = %s 
            WHERE Sensor_id = %s;
        """, (new_temperature_value, new_smoke_value, sensor_id))

        conn.commit()
        messagebox.showinfo("Thành công", "Dữ liệu đã được sửa thành công!")
        entry_temperature.delete(0, tk.END)
        entry_smoke.delete(0, tk.END)
        show_combined_data()  # Làm mới danh sách sau khi sửa

    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi sửa dữ liệu", f"Không thể sửa dữ liệu: {err}")
    finally:
        cursor.close()
        conn.close()

# Tạo giao diện tkinter
root = tk.Tk()
root.title("Dữ liệu Kết hợp từ Các Bảng Sensors, Timestamps và Status")
root.geometry("1200x500")

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

# Tạo khung nhập liệu cho việc thêm và sửa dữ liệu
frame_insert = tk.Frame(root)
frame_insert.pack(pady=10)

label_temperature = tk.Label(frame_insert, text="Giá trị Nhiệt độ:")
label_temperature.grid(row=0, column=0)
entry_temperature = tk.Entry(frame_insert)
entry_temperature.grid(row=0, column=1)

label_smoke = tk.Label(frame_insert, text="Giá trị Khói:")
label_smoke.grid(row=1, column=0)
entry_smoke = tk.Entry(frame_insert)
entry_smoke.grid(row=1, column=1)

# Nút thêm dữ liệu
btn_insert_data = tk.Button(root, text="Thêm dữ liệu", command=insert_data)
btn_insert_data.pack(pady=10)

# Nút sửa dữ liệu
btn_edit_data = tk.Button(root, text="Sửa dữ liệu", command=edit_data)
btn_edit_data.pack(pady=10)

# Nút xóa dữ liệu
btn_delete_data = tk.Button(root, text="Xóa dữ liệu", command=delete_data)
btn_delete_data.pack(pady=10)

# Khởi động ứng dụng
root.mainloop()
