from flask import Flask, render_template, request, send_from_directory
import mysql.connector
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'  # Specify your upload folder
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create the folder if it doesn't exist

def create_connection(database_name):
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="2223333",
            database=database_name
        )
        if connection.is_connected():
            print(f"Kết nối thành công với cơ sở dữ liệu {database_name}")
        return connection
    except mysql.connector.Error as e:
        print(f"Lỗi khi kết nối MySQL: {e}")
        return None

def get_media_list(connection, table_name):
    try:
        cursor = connection.cursor()
        sql_query = f"SELECT id, name_music, name_singer, name_album FROM {table_name}" if table_name == "music_table" else f"SELECT id, name_video, name_singer, name_album FROM {table_name}"
        cursor.execute(sql_query)
        return cursor.fetchall()
    except mysql.connector.Error as e:
        print(f"Lỗi khi truy xuất danh sách từ {table_name}: {e}")
        return []

def get_file_path_from_db(connection, table_name, media_id):
    try:
        cursor = connection.cursor()
        sql_query = f"SELECT file_path FROM {table_name} WHERE id = %s"
        cursor.execute(sql_query, (media_id,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    except mysql.connector.Error as e:
        print(f"Lỗi khi truy xuất file_path từ {table_name}: {e}")
        return None

@app.route('/')
def home():
    video_connection = create_connection("video_database")
    music_connection = create_connection("music_database")

    videos = get_media_list(video_connection, "video_table") if video_connection else []
    music = get_media_list(music_connection, "music_table") if music_connection else []
    
    if video_connection:
        video_connection.close()
    if music_connection:
        music_connection.close()
    
    return render_template('home.html', videos=videos, music=music)

@app.route('/play_media', methods=['POST'])
def play_media():
    media_type = request.form.get('media_type')
    media_id = request.form.get('media_id')

    if media_type == 'video':
        connection = create_connection("video_database")
        file_path = get_file_path_from_db(connection, "video_table", media_id)
        if connection:
            connection.close()
    elif media_type == 'music':
        connection = create_connection("music_database")
        file_path = get_file_path_from_db(connection, "music_table", media_id)
        if connection:
            connection.close()

    if file_path and os.path.exists(file_path):
        return render_template('play.html', media_type=media_type, file_path=file_path)
    else:
        return "Không tìm thấy file hoặc đường dẫn không hợp lệ", 404

@app.route('/add_media', methods=['POST'])
def add_media():
    media_type = request.form.get('media_type')
    file = request.files['file']
    name = request.form.get('name')
    singer = request.form.get('singer')
    album = request.form.get('album')

    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)  # Save the file

        if media_type == 'video':
            connection = create_connection("video_database")
            table_name = "video_table"
        else:
            connection = create_connection("music_database")
            table_name = "music_table"

        # Insert into the database
        try:
            cursor = connection.cursor()
            sql_insert = f"INSERT INTO {table_name} (name_video, name_singer, name_album, file_path) VALUES (%s, %s, %s, %s)" if media_type == 'video' else f"INSERT INTO {table_name} (name_music, name_singer, name_album, file_path) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql_insert, (name, singer, album, file_path))
            connection.commit()
        except mysql.connector.Error as e:
            print(f"Lỗi khi thêm vào {table_name}: {e}")
        finally:
            if connection:
                connection.close()

    return "Media added successfully", 200

@app.route('/delete_media', methods=['POST'])
def delete_media():
    media_type = request.form.get('media_type')
    media_id = request.form.get('media_id')

    if media_type == 'video':
        connection = create_connection("video_database")
        table_name = "video_table"
    else:
        connection = create_connection("music_database")
        table_name = "music_table"

    try:
        cursor = connection.cursor()
        sql_delete = f"DELETE FROM {table_name} WHERE id = %s"
        cursor.execute(sql_delete, (media_id,))
        connection.commit()
    except mysql.connector.Error as e:
        print(f"Lỗi khi xóa từ {table_name}: {e}")
    finally:
        if connection:
            connection.close()

    return "Media deleted successfully", 200

@app.route('/media/<path:filename>')
def media(filename):
    return send_from_directory(os.path.dirname(filename), os.path.basename(filename))

if __name__ == '__main__':
    app.run(debug=True)
