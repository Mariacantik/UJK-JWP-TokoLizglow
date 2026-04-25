import mysql.connector
from werkzeug.security import generate_password_hash

try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='barang_skincare'
    )
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT id, password FROM supplier;")
    suppliers = cursor.fetchall()
    
    for supp in suppliers:
        # Check if it's already hashed (starts with 'scrypt:' or 'pbkdf2:')
        if not str(supp['password']).startswith(('scrypt:', 'pbkdf2:')):
            hashed_pwd = generate_password_hash(supp['password'])
            cursor.execute(
                "UPDATE supplier SET password = %s WHERE id = %s",
                (hashed_pwd, supp['id'])
            )
            print(f"Updated supplier id {supp['id']} with hashed password.")
    
    conn.commit()
    print("Database update complete.")
except Exception as e:
    print("Error:", e)
finally:
    if 'conn' in locals() and conn.is_connected():
        conn.close()
