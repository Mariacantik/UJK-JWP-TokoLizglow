import mysql.connector

try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='barang_skincare'
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users;")
    users = cursor.fetchall()
    print("Users in database:")
    for u in users:
        print(u)
except Exception as e:
    print("Error:", e)
finally:
    if 'conn' in locals() and conn.is_connected():
        conn.close()
