import mysql.connector
from werkzeug.security import generate_password_hash

try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='barang_skincare'
    )
    cursor = conn.cursor()
    
    hashed_password = generate_password_hash('karyawan1')
    
    cursor.execute(
        "UPDATE users SET role = 'Karyawan', password = %s WHERE username = 'karyawan1'",
        (hashed_password,)
    )
    conn.commit()
    print("User karyawan1 has been updated with hashed password and role 'Karyawan'.")
except Exception as e:
    print("Error:", e)
finally:
    if 'conn' in locals() and conn.is_connected():
        conn.close()
