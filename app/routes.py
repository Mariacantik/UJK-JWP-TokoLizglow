from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, render_template, redirect, url_for, flash, request, session, Response
from reportlab.pdfgen import canvas
from io import BytesIO
from .db import db_connection

main = Blueprint('main', __name__)

# Halaman utama
@main.route('/')
def home():
    return render_template('home.html')

# Login untuk Admin/Karyawan/Supplier
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        conn = db_connection()
        cursor = conn.cursor(dictionary=True)

        if role == 'Supplier':
            cursor.execute("SELECT * FROM supplier WHERE username = %s", (username,))
        else:
            cursor.execute("SELECT * FROM users WHERE username = %s AND role = %s", (username, role))

        user = cursor.fetchone()
        
        # PERUBAHAN ENKRIPSI ADA DI BARIS INI:
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['role'] = role
            session['username'] = user['username']
            flash('Login successful!', 'success')
            
            if role == 'Admin':
                return redirect(url_for('main.admin_dashboard'))
            elif role == 'Karyawan':
                return redirect(url_for('main.karyawan_dashboard'))
            elif role == 'Supplier':
                return redirect(url_for('main.supplier_dashboard'))
        else:
            flash('Invalid credentials', 'danger')

    return render_template('login.html')
# Dashboard Admin
@main.route('/admin/dashboard')
def admin_dashboard():
    if session.get('role') != 'Admin':
        return redirect(url_for('main.home'))

    conn = db_connection()
    cursor = conn.cursor(dictionary=True)

    # Hitung jumlah barang
    cursor.execute("SELECT COUNT(*) AS jumlah_barang FROM barang")
    jumlah_barang = cursor.fetchone()['jumlah_barang']

    # Hitung jumlah supplier
    cursor.execute("SELECT COUNT(*) AS jumlah_supplier FROM supplier")
    jumlah_supplier = cursor.fetchone()['jumlah_supplier']

    return render_template('admin/dashboard.html', jumlah_barang=jumlah_barang, jumlah_supplier=jumlah_supplier)