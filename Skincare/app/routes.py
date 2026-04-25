from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint, render_template, redirect, url_for, flash, request, session, Response
from .db import db_connection
from reportlab.pdfgen import canvas
from io import BytesIO
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

# logout
@main.route('/logout')
def logout():
    # Hapus sesi pengguna
    session.clear()
    flash('Anda telah logout.', 'success')
    return redirect(url_for('main.login'))

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

# Dashboard Supplier
@main.route('/supplier/dashboard')
def supplier_dashboard():
    if session.get('role') != 'Supplier':
        return redirect(url_for('main.home'))

    supplier_id = session.get('user_id')  # Ambil ID supplier dari sesi login
    conn = db_connection()
    cursor = conn.cursor(dictionary=True)

    # Ambil data barang yang ditugaskan ke supplier
    cursor.execute("""
        SELECT b.nama AS nama_barang, b.stok, k.nama AS kategori
        FROM transaksi_masuk tm
        JOIN barang b ON tm.barang_id = b.id
        JOIN kategori_barang k ON b.kategori_id = k.id
        WHERE tm.supplier_id = %s
    """, (supplier_id,))
    barang_supplier = cursor.fetchall()

    return render_template('supplier/barang_supplier.html', barang_supplier=barang_supplier)

# tambah barang
@main.route('/admin/add_barang', methods=['GET', 'POST'])
def add_barang():
    if session.get('role') != 'Admin':
        return redirect(url_for('main.home'))
    
    conn = db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Ambil daftar kategori untuk dropdown
    cursor.execute("SELECT id, nama FROM kategori_barang")
    kategori = cursor.fetchall()
    
    if request.method == 'POST':
        nama = request.form['nama']
        stok = request.form['stok']
        kategori_id = request.form['kategori_id']
        
        # Simpan barang ke database
        cursor.execute(
            "INSERT INTO barang (nama, stok, kategori_id) VALUES (%s, %s, %s)",
            (nama, stok, kategori_id)
        )
        conn.commit()
        flash('Barang berhasil ditambahkan!', 'success')
        return redirect(url_for('main.admin_dashboard'))
    
    return render_template('admin/add_barang.html', kategori=kategori)

# edit barang
@main.route('/admin/edit_barang/<int:barang_id>', methods=['GET', 'POST'])
def edit_barang(barang_id):
    if session.get('role') != 'Admin':
        return redirect(url_for('main.home'))

    conn = db_connection()
    cursor = conn.cursor(dictionary=True)

    # Ambil data barang berdasarkan ID
    cursor.execute("SELECT * FROM barang WHERE id = %s", (barang_id,))
    barang = cursor.fetchone()

    # Ambil data kategori untuk dropdown
    cursor.execute("SELECT id, nama FROM kategori_barang")
    kategori = cursor.fetchall()

    if request.method == 'POST':
        nama = request.form['nama']
        stok = request.form['stok']
        kategori_id = request.form['kategori_id']

        # Update data barang
        cursor.execute(
            "UPDATE barang SET nama = %s, stok = %s, kategori_id = %s WHERE id = %s",
            (nama, stok, kategori_id, barang_id)
        )
        conn.commit()
        flash('Barang berhasil diperbarui!', 'success')
        return redirect(url_for('main.admin_dashboard'))

    return render_template('admin/edit_barang.html', barang=barang, kategori=kategori)

#  hapus barang
@main.route('/admin/delete_barang/<int:barang_id>', methods=['GET'])
def delete_barang(barang_id):
    if session.get('role') != 'Admin':
        return redirect(url_for('main.home'))

    conn = db_connection()
    cursor = conn.cursor()

    # Hapus barang berdasarkan ID
    cursor.execute("DELETE FROM barang WHERE id = %s", (barang_id,))
    conn.commit()
    flash('Barang berhasil dihapus!', 'success')
    return redirect(url_for('main.admin_dashboard'))

# daftar kategori
@main.route('/admin/manage_kategori')
def manage_kategori():
    if session.get('role') != 'Admin':
        return redirect(url_for('main.home'))

    conn = db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM kategori_barang")
    kategori = cursor.fetchall()
    return render_template('admin/manage_kategori.html', kategori=kategori)

# tambah kategori 
@main.route('/admin/add_kategori', methods=['GET', 'POST'])
def add_kategori():
    if session.get('role') != 'Admin':
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        nama = request.form['nama']

        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO kategori_barang (nama) VALUES (%s)", (nama,))
        conn.commit()
        flash('Kategori berhasil ditambahkan!', 'success')
        return redirect(url_for('main.manage_kategori'))

    return render_template('admin/add_kategori.html')

# edit kategori
@main.route('/admin/edit_kategori/<int:kategori_id>', methods=['GET', 'POST'])
def edit_kategori(kategori_id):
    if session.get('role') != 'Admin':
        return redirect(url_for('main.home'))

    conn = db_connection()
    cursor = conn.cursor(dictionary=True)

    # Ambil data kategori berdasarkan ID
    cursor.execute("SELECT * FROM kategori_barang WHERE id = %s", (kategori_id,))
    kategori = cursor.fetchone()

    if request.method == 'POST':
        nama = request.form['nama']

        # Update data kategori
        cursor.execute("UPDATE kategori_barang SET nama = %s WHERE id = %s", (nama, kategori_id))
        conn.commit()
        flash('Kategori berhasil diperbarui!', 'success')
        return redirect(url_for('main.manage_kategori'))

    return render_template('admin/edit_kategori.html', kategori=kategori)

# hapus kategori
@main.route('/admin/delete_kategori/<int:kategori_id>', methods=['GET'])
def delete_kategori(kategori_id):
    if session.get('role') != 'Admin':
        return redirect(url_for('main.home'))

    conn = db_connection()
    cursor = conn.cursor()

    # Hapus kategori berdasarkan ID
    cursor.execute("DELETE FROM kategori_barang WHERE id = %s", (kategori_id,))
    conn.commit()
    flash('Kategori berhasil dihapus!', 'success')
    return redirect(url_for('main.manage_kategori'))


#  daftar transaksi masuk 
@main.route('/admin/manage_transaksi_masuk')
def manage_transaksi_masuk():
    if session.get('role') != 'Admin':
        return redirect(url_for('main.home'))

    conn = db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT tm.id, b.nama AS nama_barang, tm.jumlah, tm.tanggal, s.nama_pt AS nama_supplier 
        FROM transaksi_masuk tm
        JOIN barang b ON tm.barang_id = b.id
        JOIN supplier s ON tm.supplier_id = s.id
    """)
    transaksi_masuk = cursor.fetchall()
    return render_template('admin/manage_transaksi_masuk.html', transaksi_masuk=transaksi_masuk)


# tambah transaksi masuk 
@main.route('/admin/add_transaksi_masuk', methods=['GET', 'POST'])
def add_transaksi_masuk():
    if session.get('role') != 'Admin':
        return redirect(url_for('main.home'))

    conn = db_connection()
    cursor = conn.cursor(dictionary=True)

    # Ambil daftar barang untuk dropdown
    cursor.execute("SELECT id, nama FROM barang")
    barang = cursor.fetchall()

    # Ambil daftar supplier untuk dropdown
    cursor.execute("SELECT id, nama_pt FROM supplier")
    suppliers = cursor.fetchall()

    if request.method == 'POST':
        barang_id = request.form['barang_id']
        jumlah = request.form['jumlah']
        supplier_id = request.form['supplier_id']

        # Simpan transaksi masuk ke database
        cursor.execute(
            "INSERT INTO transaksi_masuk (barang_id, jumlah, supplier_id) VALUES (%s, %s, %s)",
            (barang_id, jumlah, supplier_id)
        )
        conn.commit()

        # Update stok barang
        cursor.execute(
            "UPDATE barang SET stok = stok + %s WHERE id = %s",
            (jumlah, barang_id)
        )
        conn.commit()

        flash('Transaksi masuk berhasil ditambahkan!', 'success')
        return redirect(url_for('main.manage_transaksi_masuk'))

    return render_template('admin/add_transaksi_masuk.html', barang=barang, suppliers=suppliers)

# hapus transaksi masuk 
@main.route('/admin/delete_transaksi_masuk/<int:transaksi_id>', methods=['GET'])
def delete_transaksi_masuk(transaksi_id):
    if session.get('role') != 'Admin':
        return redirect(url_for('main.home'))

    conn = db_connection()
    cursor = conn.cursor(dictionary=True)

    # Ambil data transaksi masuk untuk mengurangi stok barang
    cursor.execute("SELECT barang_id, jumlah FROM transaksi_masuk WHERE id = %s", (transaksi_id,))
    transaksi = cursor.fetchone()

    if transaksi:
        # Hapus transaksi masuk
        cursor.execute("DELETE FROM transaksi_masuk WHERE id = %s", (transaksi_id,))
        conn.commit()

        # Kurangi stok barang
        cursor.execute(
            "UPDATE barang SET stok = stok - %s WHERE id = %s",
            (transaksi['jumlah'], transaksi['barang_id'])
        )
        conn.commit()

        flash('Transaksi masuk berhasil dihapus!', 'success')

    return redirect(url_for('main.manage_transaksi_masuk'))

# daftar transaksi keluar
@main.route('/admin/manage_transaksi_keluar')
def manage_transaksi_keluar():
    if session.get('role') != 'Admin':
        return redirect(url_for('main.home'))

    conn = db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT tk.id, b.nama AS nama_barang, tk.jumlah, tk.tanggal 
        FROM transaksi_keluar tk
        JOIN barang b ON tk.barang_id = b.id
    """)
    transaksi_keluar = cursor.fetchall()
    return render_template('admin/manage_transaksi_keluar.html', transaksi_keluar=transaksi_keluar)


# tambah transaksi keluar
@main.route('/admin/add_transaksi_keluar', methods=['GET', 'POST'])
def add_transaksi_keluar():
    if session.get('role') != 'Admin':
        return redirect(url_for('main.home'))

    conn = db_connection()
    cursor = conn.cursor(dictionary=True)

    # Ambil daftar barang untuk dropdown
    cursor.execute("SELECT id, nama FROM barang")
    barang = cursor.fetchall()

    if request.method == 'POST':
        barang_id = request.form['barang_id']
        jumlah = request.form['jumlah']

        # Simpan transaksi keluar ke database
        cursor.execute(
            "INSERT INTO transaksi_keluar (barang_id, jumlah) VALUES (%s, %s)",
            (barang_id, jumlah)
        )
        conn.commit()

        # Kurangi stok barang
        cursor.execute(
            "UPDATE barang SET stok = stok - %s WHERE id = %s AND stok >= %s",
            (jumlah, barang_id, jumlah)
        )
        if cursor.rowcount == 0:
            flash('Stok barang tidak mencukupi!', 'danger')
            conn.rollback()
        else:
            conn.commit()
            flash('Transaksi keluar berhasil ditambahkan!', 'success')

        return redirect(url_for('main.manage_transaksi_keluar'))

    return render_template('admin/add_transaksi_keluar.html', barang=barang)


# hapus transaksi keluar 
@main.route('/admin/delete_transaksi_keluar/<int:transaksi_id>', methods=['GET'])
def delete_transaksi_keluar(transaksi_id):
    if session.get('role') != 'Admin':
        return redirect(url_for('main.home'))

    conn = db_connection()
    cursor = conn.cursor(dictionary=True)

    # Ambil data transaksi keluar untuk menambah stok barang
    cursor.execute("SELECT barang_id, jumlah FROM transaksi_keluar WHERE id = %s", (transaksi_id,))
    transaksi = cursor.fetchone()

    if transaksi:
        # Hapus transaksi keluar
        cursor.execute("DELETE FROM transaksi_keluar WHERE id = %s", (transaksi_id,))
        conn.commit()

        # Tambah stok barang
        cursor.execute(
            "UPDATE barang SET stok = stok + %s WHERE id = %s",
            (transaksi['jumlah'], transaksi['barang_id'])
        )
        conn.commit()

        flash('Transaksi keluar berhasil dihapus!', 'success')

    return redirect(url_for('main.manage_transaksi_keluar'))

# daftar barang karyawan
@main.route('/karyawan/dashboard')
def karyawan_dashboard():
    if session.get('role') != 'Karyawan':
        return redirect(url_for('main.home'))

    conn = db_connection()
    cursor = conn.cursor(dictionary=True)

    # Ambil daftar barang
    cursor.execute("""
        SELECT b.nama AS nama_barang, b.stok, k.nama AS kategori
        FROM barang b
        JOIN kategori_barang k ON b.kategori_id = k.id
    """)
    barang = cursor.fetchall()

    return render_template('karyawan/dashboard.html', barang=barang)
# admin manage barang
@main.route('/admin/manage_barang', methods=['GET', 'POST'])
def manage_barang():
    if session.get('role') != 'Admin':
        return redirect(url_for('main.home'))

    conn = db_connection()
    cursor = conn.cursor(dictionary=True)

    # Ambil semua data barang
    cursor.execute("""
        SELECT b.id, b.nama AS nama_barang, b.stok, k.nama AS kategori
        FROM barang b
        JOIN kategori_barang k ON b.kategori_id = k.id
    """)
    barang = cursor.fetchall()

    return render_template('admin/manage_barang.html', barang=barang)

# manage supplier
@main.route('/admin/manage_supplier')
def manage_supplier():
    if session.get('role') != 'Admin':
        return redirect(url_for('main.home'))

    conn = db_connection()
    cursor = conn.cursor(dictionary=True)

    # Ambil semua data supplier
    cursor.execute("SELECT * FROM supplier")
    suppliers = cursor.fetchall()

    return render_template('admin/manage_supplier.html', suppliers=suppliers)

# tambah supplier 
@main.route('/admin/add_supplier', methods=['GET', 'POST'])
def add_supplier():
    if session.get('role') != 'Admin':
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        nama_pt = request.form['nama_pt']
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        conn = db_connection()
        cursor = conn.cursor()

        # Simpan supplier ke database
        cursor.execute(
            "INSERT INTO supplier (nama_pt, username, password) VALUES (%s, %s, %s)",
            (nama_pt, username, hashed_password)
        )
        conn.commit()

        flash('Supplier berhasil ditambahkan!', 'success')
        return redirect(url_for('main.manage_supplier'))

    return render_template('admin/add_supplier.html')

# edit supplier
@main.route('/admin/edit_supplier/<int:supplier_id>', methods=['GET', 'POST'])
def edit_supplier(supplier_id):
    if session.get('role') != 'Admin':
        return redirect(url_for('main.home'))

    conn = db_connection()
    cursor = conn.cursor(dictionary=True)

    # Ambil data supplier berdasarkan ID
    cursor.execute("SELECT * FROM supplier WHERE id = %s", (supplier_id,))
    supplier = cursor.fetchone()

    if request.method == 'POST':
        nama_pt = request.form['nama_pt']
        username = request.form['username']
        password = request.form['password']
        
        # In case the password is provided or updated, we should hash it
        if password:
            hashed_password = generate_password_hash(password)
        else:
            # Note: Depending on form validation, password might be required.
            hashed_password = ""

        # Update data supplier
        cursor.execute(
            "UPDATE supplier SET nama_pt = %s, username = %s, password = %s WHERE id = %s",
            (nama_pt, username, hashed_password, supplier_id)
        )
        conn.commit()

        flash('Supplier berhasil diperbarui!', 'success')
        return redirect(url_for('main.manage_supplier'))

    return render_template('admin/edit_supplier.html', supplier=supplier)

# hapus supplier 
@main.route('/admin/delete_supplier/<int:supplier_id>', methods=['GET'])
def delete_supplier(supplier_id):
    if session.get('role') != 'Admin':
        return redirect(url_for('main.home'))

    conn = db_connection()
    cursor = conn.cursor()

    # Hapus supplier dari database
    cursor.execute("DELETE FROM supplier WHERE id = %s", (supplier_id,))
    conn.commit()

    flash('Supplier berhasil dihapus!', 'success')
    return redirect(url_for('main.manage_supplier'))

# cetak barang
@main.route('/admin/cetak_laporan_barang_reportlab')
def cetak_laporan_barang_reportlab():
    if session.get('role') != 'Admin':
        return redirect(url_for('main.home'))

    conn = db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT b.nama AS nama_barang, b.stok, k.nama AS kategori
        FROM barang b
        JOIN kategori_barang k ON b.kategori_id = k.id
    """)
    barang = cursor.fetchall()

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.setTitle("Laporan Barang")

    # Header PDF
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, 800, "Laporan Barang")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 780, "Nama Barang")
    pdf.drawString(300, 780, "Stok")
    pdf.drawString(400, 780, "Kategori")
    pdf.line(100, 770, 500, 770)

    # Data Barang
    y = 750
    for item in barang:
        pdf.drawString(100, y, item['nama_barang'])
        pdf.drawString(300, y, str(item['stok']))
        pdf.drawString(400, y, item['kategori'])
        y -= 20

    pdf.save()
    buffer.seek(0)
    return Response(buffer, content_type='application/pdf')

# cetak transaksi keluar
@main.route('/admin/cetak_laporan_transaksi_keluar_reportlab')
def cetak_laporan_transaksi_keluar_reportlab():
    if session.get('role') != 'Admin':
        return redirect(url_for('main.home'))

    conn = db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT tk.id, b.nama AS nama_barang, tk.jumlah, tk.tanggal
        FROM transaksi_keluar tk
        JOIN barang b ON tk.barang_id = b.id
    """)
    transaksi_keluar = cursor.fetchall()

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.setTitle("Laporan Transaksi Keluar")

    # Header PDF
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, 800, "Laporan Transaksi Keluar")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 780, "Nama Barang")
    pdf.drawString(300, 780, "Jumlah")
    pdf.drawString(400, 780, "Tanggal")
    pdf.line(100, 770, 500, 770)

    # Data Transaksi Keluar
    y = 750
    for item in transaksi_keluar:
        pdf.drawString(100, y, item['nama_barang'])
        pdf.drawString(300, y, str(item['jumlah']))
        pdf.drawString(400, y, item['tanggal'].strftime('%Y-%m-%d'))
        y -= 20

    pdf.save()
    buffer.seek(0)
    return Response(buffer, content_type='application/pdf')

# cetak transaksi masuk
@main.route('/admin/cetak_laporan_transaksi_masuk_reportlab')
def cetak_laporan_transaksi_masuk_reportlab():
    if session.get('role') != 'Admin':
        return redirect(url_for('main.home'))

    conn = db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT tm.id, b.nama AS nama_barang, tm.jumlah, tm.tanggal
        FROM transaksi_masuk tm
        JOIN barang b ON tm.barang_id = b.id
    """)
    transaksi_masuk = cursor.fetchall()

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.setTitle("Laporan Transaksi Masuk")

    # Header PDF
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, 800, "Laporan Transaksi Masuk")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 780, "Nama Barang")
    pdf.drawString(300, 780, "Jumlah")
    pdf.drawString(400, 780, "Tanggal")
    pdf.line(100, 770, 500, 770)

    # Data Transaksi Masuk
    y = 750
    for item in transaksi_masuk:
        pdf.drawString(100, y, item['nama_barang'])
        pdf.drawString(300, y, str(item['jumlah']))
        pdf.drawString(400, y, item['tanggal'].strftime('%Y-%m-%d'))
        y -= 20

    pdf.save()
    buffer.seek(0)
    return Response(buffer, content_type='application/pdf')

# ==========================================
# CRUD PELANGGAN (Tugas Tambahan UJK)
# ==========================================

# 1. READ (Tampil Data)
@main.route('/admin/manage_pelanggan')
def manage_pelanggan():
    if session.get('role') != 'Admin': return redirect(url_for('main.home'))
    conn = db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pelanggan")
    daftar_pelanggan = cursor.fetchall()
    return render_template('manage_pelanggan.html', pelanggan=daftar_pelanggan)

# 2. CREATE (Tambah Data)
@main.route('/admin/tambah_pelanggan', methods=['POST'])
def tambah_pelanggan():
    if session.get('role') != 'Admin': return redirect(url_for('main.home'))
    nama = request.form['nama_pelanggan']
    no_hp = request.form['no_hp']
    alamat = request.form['alamat']
    
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pelanggan (nama_pelanggan, no_hp, alamat) VALUES (%s, %s, %s)", (nama, no_hp, alamat))
    conn.commit()
    flash('Data Pelanggan berhasil ditambahkan!', 'success')
    return redirect(url_for('main.manage_pelanggan'))

# 3. DELETE (Hapus Data)
@main.route('/admin/hapus_pelanggan/<int:id>')
def hapus_pelanggan(id):
    if session.get('role') != 'Admin': return redirect(url_for('main.home'))
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pelanggan WHERE id_pelanggan=%s", (id,))
    conn.commit()
    flash('Data Pelanggan berhasil dihapus!', 'success')
    return redirect(url_for('main.manage_pelanggan'))