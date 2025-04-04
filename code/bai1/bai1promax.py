import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, Frame, Label
import mysql.connector
import os
import vlc

# Kết nối với cơ sở dữ liệu
def connect_to_database(database_name):
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="2223333",
        database=database_name
    )

# Kết nối với cơ sở dữ liệu cho video và âm nhạc
video_db = connect_to_database("video_database")
music_db = connect_to_database("music_database")

# Khởi tạo trình phát VLC
media_player = vlc.MediaPlayer()

# Hàm tải danh sách video
def load_videos():
    cursor = video_db.cursor()
    cursor.execute("SELECT id, name_video FROM video_table")
    video_list.delete(0, tk.END)
    for video in cursor.fetchall():
        video_list.insert(tk.END, video[1])
    cursor.close()

# Hàm mở video
def open_video():
    selected_video = video_list.curselection()
    if selected_video:
        video_name = video_list.get(selected_video)
        cursor = video_db.cursor()
        cursor.execute("SELECT file_path FROM video_table WHERE name_video = %s", (video_name,))
        file_path = cursor.fetchone()
        cursor.close()
        
        if file_path:
            media_player.set_media(vlc.Media(file_path[0]))
            media_player.set_hwnd(video_frame.winfo_id())
            media_player.play()
            display_video_info(None)
        else:
            messagebox.showwarning("Lỗi", "Không tìm thấy video.")
    else:
        messagebox.showwarning("Chọn video", "Hãy chọn một video để mở.")

# Hàm thêm video mới
def add_video():
    file_path = filedialog.askopenfilename(title="Chọn file video", filetypes=[("Video files", "*.mp4 *.avi")])
    if file_path:
        video_name = os.path.basename(file_path)
        name_singer = simpledialog.askstring("Nhập tên ca sĩ", "Tên ca sĩ:")
        name_album = simpledialog.askstring("Nhập tên album", "Tên album:")
        cursor = video_db.cursor()
        cursor.execute("INSERT INTO video_table (name_video, name_singer, name_album, file_path) VALUES (%s, %s, %s, %s)", (video_name, name_singer, name_album, file_path))
        video_db.commit()
        cursor.close()
        load_videos()

# Hàm xóa video
def delete_video():
    selected_video = video_list.curselection()
    if selected_video:
        video_name = video_list.get(selected_video)
        cursor = video_db.cursor()
        cursor.execute("DELETE FROM video_table WHERE name_video = %s", (video_name,))
        video_db.commit()
        cursor.close()
        load_videos()
    else:
        messagebox.showwarning("Chọn video", "Hãy chọn một video để xóa")

# Hàm sửa thông tin video
def edit_video():
    selected_video = video_list.curselection()
    if selected_video:
        video_name = video_list.get(selected_video)
        new_name = simpledialog.askstring("Chỉnh sửa video", "Nhập tên mới cho video:", initialvalue=video_name)
        if new_name:
            cursor = video_db.cursor()
            cursor.execute("UPDATE video_table SET name_video = %s WHERE name_video = %s", (new_name, video_name))
            video_db.commit()
            cursor.close()
            load_videos()
    else:
        messagebox.showwarning("Chọn video", "Hãy chọn một video để chỉnh sửa")

# Hàm tải danh sách âm nhạc
def load_music():
    cursor = music_db.cursor()
    cursor.execute("SELECT id, name_music FROM music_table")
    music_list.delete(0, tk.END)
    for music in cursor.fetchall():
        music_list.insert(tk.END, music[1])
    cursor.close()

# Hàm thêm âm nhạc mới
def add_music():
    file_path = filedialog.askopenfilename(title="Chọn file âm nhạc", filetypes=[("Audio files", "*.mp3 *.wav")])
    if file_path:
        music_name = simpledialog.askstring("Thêm âm nhạc", "Nhập tên bài hát:")
        singer_name = simpledialog.askstring("Thêm âm nhạc", "Nhập tên ca sĩ:")
        album_name = simpledialog.askstring("Thêm âm nhạc", "Nhập tên album:")
        
        if music_name and singer_name and album_name:
            cursor = music_db.cursor()
            cursor.execute("INSERT INTO music_table (name_music, name_singer, name_album, file_path) VALUES (%s, %s, %s, %s)",
                           (music_name, singer_name, album_name, file_path))
            music_db.commit()
            cursor.close()
            load_music()

# Hàm xóa âm nhạc
def delete_music():
    selected_music = music_list.curselection()
    if selected_music:
        music_name = music_list.get(selected_music)
        cursor = music_db.cursor()
        cursor.execute("DELETE FROM music_table WHERE name_music = %s", (music_name,))
        music_db.commit()
        cursor.close()
        load_music()
    else:
        messagebox.showwarning("Chọn âm nhạc", "Hãy chọn một bài hát để xóa")

# Hàm sửa thông tin âm nhạc
def edit_music():
    selected_music = music_list.curselection()
    if selected_music:
        music_name = music_list.get(selected_music)
        new_name = simpledialog.askstring("Chỉnh sửa âm nhạc", "Nhập tên mới cho bài hát:", initialvalue=music_name)
        new_singer = simpledialog.askstring("Chỉnh sửa âm nhạc", "Nhập tên ca sĩ mới:")
        new_album = simpledialog.askstring("Chỉnh sửa âm nhạc", "Nhập tên album mới:")
        
        if new_name and new_singer and new_album:
            cursor = music_db.cursor()
            cursor.execute("UPDATE music_table SET name_music = %s, name_singer = %s, name_album = %s WHERE name_music = %s",
                           (new_name, new_singer, new_album, music_name))
            music_db.commit()
            cursor.close()
            load_music()
    else:
        messagebox.showwarning("Chọn âm nhạc", "Hãy chọn một bài hát để chỉnh sửa")

# Hàm phát nhạc
def play_music():
    selected_music = music_list.curselection()
    if selected_music:
        music_name = music_list.get(selected_music)
        cursor = music_db.cursor()
        cursor.execute("SELECT file_path FROM music_table WHERE name_music = %s", (music_name,))
        file_path = cursor.fetchone()
        
        if file_path:
            media_player.set_media(vlc.Media(file_path[0]))
            media_player.play()
            display_music_info(None)
        cursor.close()
    else:
        messagebox.showwarning("Chọn âm nhạc", "Hãy chọn một bài hát để phát")

# Hàm hiển thị thông tin video
def display_video_info(event):
    selected_video = video_list.curselection()
    if selected_video:
        video_name = video_list.get(selected_video)
        cursor = video_db.cursor()
        cursor.execute("SELECT name_singer, name_album, file_path FROM video_table WHERE name_video = %s", (video_name,))
        video_info = cursor.fetchone()
        cursor.close()
        
        if video_info:
            video_info_text.set(f"Tên video: {video_name}\nCa sĩ: {video_info[0]}\nAlbum: {video_info[1]}\nĐường dẫn: {video_info[2]}")
        else:
            video_info_text.set("Không tìm thấy thông tin video.")
    else:
        video_info_text.set("")

# Hàm hiển thị thông tin âm nhạc
def display_music_info(event):
    selected_music = music_list.curselection()
    if selected_music:
        music_name = music_list.get(selected_music)
        cursor = music_db.cursor()
        cursor.execute("SELECT name_singer, name_album, file_path FROM music_table WHERE name_music = %s", (music_name,))
        music_info = cursor.fetchone()
        cursor.close()
        
        if music_info:
            music_info_text.set(f"Tên bài hát: {music_name}\nCa sĩ: {music_info[0]}\nAlbum: {music_info[1]}\nĐường dẫn: {music_info[2]}")
        else:
            music_info_text.set("Không tìm thấy thông tin âm nhạc.")
    else:
        music_info_text.set("")

# Hàm dừng phát video và âm nhạc
def stop_playback():
    media_player.stop()  # Dừng phát video hoặc âm nhạc
    video_info_text.set("")  # Xóa thông tin video
    music_info_text.set("")  # Xóa thông tin âm nhạc

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Quản lý video và âm nhạc")

# Tạo các Frame
frame_left = Frame(root, padx=10, pady=10)
frame_left.grid(row=0, column=0, sticky='nsew')

frame_right = Frame(root, padx=10, pady=10)
frame_right.grid(row=0, column=1, sticky='nsew')

frame_video = Frame(frame_left, bd=2, relief=tk.RIDGE)
frame_video.pack(pady=5)

frame_music = Frame(frame_left, bd=2, relief=tk.RIDGE)
frame_music.pack(pady=5)

# Tạo danh sách video
video_list = tk.Listbox(frame_video, width=40, height=10)
video_list.pack(side=tk.LEFT)

video_scrollbar = tk.Scrollbar(frame_video)
video_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
video_list.config(yscrollcommand=video_scrollbar.set)
video_scrollbar.config(command=video_list.yview)
video_list.bind("<<ListboxSelect>>", display_video_info)

video_info_text = tk.StringVar()
video_info_label = Label(frame_video, textvariable=video_info_text, justify=tk.LEFT)
video_info_label.pack(pady=5)

# Tạo nút điều khiển video
btn_video_frame = Frame(frame_video)
btn_video_frame.pack(pady=5)

btn_add_video = tk.Button(btn_video_frame, text="Thêm video", command=add_video)
btn_add_video.grid(row=0, column=0, padx=5)

btn_delete_video = tk.Button(btn_video_frame, text="Xóa video", command=delete_video)
btn_delete_video.grid(row=0, column=1, padx=5)

btn_edit_video = tk.Button(btn_video_frame, text="Chỉnh sửa video", command=edit_video)
btn_edit_video.grid(row=0, column=2, padx=5)

btn_open_video = tk.Button(btn_video_frame, text="Mở video", command=open_video)
btn_open_video.grid(row=0, column=3, padx=5)

# Tạo danh sách âm nhạc
music_list = tk.Listbox(frame_music, width=40, height=10)
music_list.pack(side=tk.LEFT)

music_scrollbar = tk.Scrollbar(frame_music)
music_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
music_list.config(yscrollcommand=music_scrollbar.set)
music_scrollbar.config(command=music_list.yview)
music_list.bind("<<ListboxSelect>>", display_music_info)

music_info_text = tk.StringVar()
music_info_label = Label(frame_music, textvariable=music_info_text, justify=tk.LEFT)
music_info_label.pack(pady=5)

# Tạo nút điều khiển âm nhạc
btn_music_frame = Frame(frame_music)
btn_music_frame.pack(pady=5)

btn_add_music = tk.Button(btn_music_frame, text="Thêm âm nhạc", command=add_music)
btn_add_music.grid(row=0, column=0, padx=5)

btn_delete_music = tk.Button(btn_music_frame, text="Xóa âm nhạc", command=delete_music)
btn_delete_music.grid(row=0, column=1, padx=5)

btn_edit_music = tk.Button(btn_music_frame, text="Chỉnh sửa âm nhạc", command=edit_music)
btn_edit_music.grid(row=0, column=2, padx=5)

btn_play_music = tk.Button(btn_music_frame, text="Phát nhạc", command=play_music)
btn_play_music.grid(row=0, column=3, padx=5)

btn_stop_playback = tk.Button(root, text="Dừng phát", command=stop_playback)
btn_stop_playback.grid(row=1, column=0, columnspan=2, pady=10)

# Tạo Frame cho video
video_frame = Frame(frame_right, bd=2, relief=tk.RIDGE, width=400, height=300)
video_frame.pack(padx=10, pady=10)

# Thiết lập tỉ lệ kích thước
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Tải danh sách video và âm nhạc
load_videos()
load_music()

# Chạy vòng lặp chính
root.mainloop()
