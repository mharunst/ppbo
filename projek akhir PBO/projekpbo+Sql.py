import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import mysql.connector

# ===== DATABASE CONFIGURATION =====
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # ganti sesuai dengan config lokalmu
    database="tes"
)
cursor = conn.cursor(dictionary=True)


root = None

# ===== MODEL =====
class User(ABC):
    def __init__(self, username, password, nama):
        self.username = username
        self.password = password
        self.nama = nama

    @abstractmethod
    def get_role(self):
        pass

class Mahasiswa(User):
    def __init__(self, username, password, nama, nim, semester, hasil_studi):
        super().__init__(username, password, nama)
        self.nim = nim
        self.semester = semester
        self.hasil_studi = hasil_studi

    def get_role(self):
        return "mahasiswa"

class Dosen(User):
    def __init__(self, username, password, nama, mata_kuliah):
        super().__init__(username, password, nama)
        self.mata_kuliah = mata_kuliah

    def get_role(self):
        return "dosen"

# ===== LOAD & SAVE DATA =====
def load_data_mahasiswa():
    cursor.execute("SELECT * FROM mahasiswa")
    mahasiswa_rows = cursor.fetchall()

    mahasiswa_list = []
    for row in mahasiswa_rows:
        cursor.execute("""
            SELECT h.*, mk.kode, mk.nama AS nama_mk
            FROM hasil_studi h
            JOIN mata_kuliah mk ON h.kode_mk = mk.kode
            WHERE h.nim = %s
        """, (row['nim'],))
        nilai_rows = cursor.fetchall()

        hasil_studi = []
        for nilai in nilai_rows:
            hasil_studi.append({
                'mata_kuliah': {
                    'kode': nilai['kode'],
                    'nama': nilai['nama_mk']
                },
                'nilai': {
                    'tugas': nilai['tugas'],
                    'uts': nilai['uts'],
                    'uas': nilai['uas'],
                    'akhir': nilai['akhir'],
                    'huruf': nilai['huruf']
                }
            })

        mhs = Mahasiswa(row['username'], row['password'], row['nama'], row['nim'], row['semester'], hasil_studi)
        mahasiswa_list.append(mhs)

    return mahasiswa_list

def load_data_dosen():
    cursor.execute("SELECT * FROM dosen")
    dosen_rows = cursor.fetchall()

    dosen_list = []
    for row in dosen_rows:
        cursor.execute("SELECT kode_mk FROM dosen_mengajar WHERE username_dosen = %s", (row['username'],))
        mk_rows = cursor.fetchall()
        mata_kuliah = [mk['kode_mk'] for mk in mk_rows]
        dosen = Dosen(row['username'], row['password'], row['nama'], mata_kuliah)
        dosen_list.append(dosen)

    return dosen_list

def load_jadwal():
    cursor.execute("""
        SELECT j.semester_id, j.hari, j.kode_mk, j.waktu, mk.nama
        FROM jadwal_kuliah j
        JOIN mata_kuliah mk ON j.kode_mk = mk.kode
    """)
    rows = cursor.fetchall()

    jadwal_dict = {}
    for r in rows:
        jadwal_dict.setdefault(str(r['semester_id']), {}).setdefault(r['hari'], []).append({
            'mata_kuliah': {
                'kode': r['kode_mk'],
                'nama': r['nama']
            },
            'waktu': r['waktu']
        })

    return jadwal_dict

def load_jadwal_ujian():
    cursor.execute("""
        SELECT j.id, j.semester_id, s.id AS semester, j.kode_mk, mk.nama AS nama_mk, j.tanggal, j.waktu, j.ruangan
        FROM jadwal_ujian j
        JOIN semester s ON j.semester_id = s.id
        JOIN mata_kuliah mk ON j.kode_mk = mk.kode
    """)
    rows = cursor.fetchall()

    jadwal_ujian_list = []
    for row in rows:
        jadwal_ujian_list.append({
            'id': row['id'],
            'semester_id': row['semester_id'],
            'kode_mk': row['kode_mk'],
            'nama_mk': row['nama_mk'],
            'tanggal': row['tanggal'],
            'waktu': row['waktu'],
            'ruangan': row['ruangan']
        })

    return jadwal_ujian_list

def load_paket_semester():
    cursor.execute("""
        SELECT p.id, p.semester_id, s.id AS semester, p.kode_mk, mk.nama AS nama_mk
        FROM paket_semester p
        JOIN semester s ON p.semester_id = s.id
        JOIN mata_kuliah mk ON p.kode_mk = mk.kode
    """)
    rows = cursor.fetchall()

    paket_list = []
    for row in rows:
        paket_list.append({
            'id': row['id'],
            'semester_id': row['semester_id'],
            'kode_mk': row['kode_mk'],
            'nama_mk': row['nama_mk']
        })

    return paket_list

def load_krs():
    cursor.execute("""
        SELECT k.id, k.username, m.nama AS nama_mhs, k.kode_mk, mk.nama AS nama_mk, k.semester, k.status
        FROM krs k
        JOIN mahasiswa m ON k.username = m.username
        JOIN mata_kuliah mk ON k.kode_mk = mk.kode
    """)
    rows = cursor.fetchall()

    krs_list = []
    for row in rows:
        krs_list.append({
            'id': row['id'],
            'username': row['username'],
            'nama_mhs': row['nama_mhs'],
            'kode_mk': row['kode_mk'],
            'nama_mk': row['nama_mk'],
            'semester': row['semester'],
            'status': row['status']
        })

    return krs_list

def load_feedback_matkul(username, semester):
    cursor.execute("""
        SELECT mk.kode AS kode_mk, mk.nama
        FROM paket_semester p
        JOIN mata_kuliah mk ON p.kode_mk = mk.kode
        WHERE p.semester_id = %s
    """, (semester,))
    rows = cursor.fetchall()
    return rows

def simpan_data_mahasiswa(mahasiswa_list):
    for mhs in mahasiswa_list:
        for hasil in mhs.hasil_studi:
            kode = hasil['mata_kuliah']['kode']
            nilai = hasil['nilai']

            # Cek apakah sudah ada nilai untuk nim & matkul ini
            cursor.execute("SELECT * FROM hasil_studi WHERE nim = %s AND kode_mk = %s", (mhs.nim, kode))
            existing = cursor.fetchone()

            if existing:
                # Update data jika sudah ada
                cursor.execute("""
                    UPDATE hasil_studi
                    SET tugas = %s, uts = %s, uas = %s, akhir = %s, huruf = %s
                    WHERE nim = %s AND kode_mk = %s
                """, (
                    nilai['tugas'], nilai['uts'], nilai['uas'],
                    nilai['akhir'], nilai['huruf'],
                    mhs.nim, kode
                ))
                conn.commit()

            else:
                # Insert data jika belum ada
                cursor.execute("""
                    INSERT INTO hasil_studi (nim, kode_mk, tugas, uts, uas, akhir, huruf)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    mhs.nim, kode,
                    nilai['tugas'], nilai['uts'], nilai['uas'],
                    nilai['akhir'], nilai['huruf']
                ))
                conn.commit()

# ===== CONTROLLER GUI =====
class MahasiswaControllerGUI:
    def __init__(self, mahasiswa, jadwal,  jadwal_ujian_list, paket_semester_list):
        self.mahasiswa = mahasiswa
        self.jadwal = jadwal 
        self.jadwal_ujian_list = jadwal_ujian_list
        self.paket_semester_list = paket_semester_list 

        self.window = tk.Toplevel()
        self.window.title(f"Dashboard ReGima Mahasiswa - {mahasiswa.nama}")
        self.window.geometry("700x450")

        main_frame = tk.Frame(self.window)
        main_frame.pack(fill="both", expand=True)

        self.left_frame = tk.Frame(main_frame, width=150, bg="#0050d9")
        self.left_frame.pack(side="left", fill="y")

        separator = ttk.Separator(main_frame, orient="vertical")
        separator.pack(side="left", fill="y", padx=5)

        self.right_frame = tk.Frame(main_frame)
        self.right_frame.pack(side="right", fill="both", expand=True)

        button_style = {
            "bg": "#0050d9",              # warna dasar tombol
            "fg": "#FFFFFF",              # warna teks
            "activebackground": "#0c0051",# warna saat hover
            "activeforeground": "#FFFFFF",# warna teks saat hover
            "relief": "flat",             # model border datar
            "bd": 0,                      # border width 0
            "font": ("Arial", 10),
            "anchor": 'w'
            
        }
        tk.Button(self.left_frame, text="📋 Lihat Profil", command=self.lihat_profil, **button_style).pack(fill='x', padx=10, pady=5)
        tk.Button(self.left_frame, text="📅 Lihat Jadwal", command=self.lihat_jadwal, **button_style).pack(fill='x', padx=10, pady=5)
        tk.Button(self.left_frame, text="📖 Lihat Hasil Studi", command=self.lihat_hasil_studi, **button_style).pack(fill='x', padx=10, pady=5)
        tk.Button(self.left_frame, text="📖 Lihat Jadwal Ujian", command=self.jadwal_ujian, **button_style).pack(fill='x', padx=10, pady=5)
        tk.Button(self.left_frame, text="📝 Pengajuan KRS", command=self.pengajuan_krs, **button_style).pack(fill='x', padx=10, pady=5)
        tk.Button(self.left_frame, text="🗣️ Feedback Dosen", command=self.feedback_dosen, **button_style).pack(fill='x', padx=10, pady=5)
        tk.Button(self.left_frame, text="🔙 Logout", command=self.logout,fg="white", bg="#f9623d" ).pack(fill='x', padx=10, pady=100)

        self.content = tk.Label(self.right_frame, text="Selamat datang di ReGima, " + mahasiswa.nama, justify="center", font=('Arial', 12, 'bold'), anchor="nw")
        self.content.pack(fill="both", expand=True)

    def clear_content(self): 
        for widget in self.right_frame.winfo_children():
            widget.destroy()

    def tampilkan_konten(self, text):
        self.clear_content()
        label = tk.Label(self.right_frame, text=text, justify="left", anchor="nw")
        label.pack(fill="both", expand=True)

    def lihat_profil(self):
        self.clear_content()
        profil_frame = tk.Frame(self.right_frame, padx=20, pady=20)
        profil_frame.pack(fill="both", expand=True, anchor="n")

        tk.Label(profil_frame, text="📋 Profil Mahasiswa", font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=(0, 10))

        tk.Label(profil_frame, text="Nama:", anchor="w", width=15).grid(row=1, column=0, sticky="w")
        tk.Label(profil_frame, text=self.mahasiswa.nama, anchor="w").grid(row=1, column=1, sticky="w")

        tk.Label(profil_frame, text="NIM:", anchor="w", width=15).grid(row=2, column=0, sticky="w")
        tk.Label(profil_frame, text=self.mahasiswa.nim, anchor="w").grid(row=2, column=1, sticky="w")

        tk.Label(profil_frame, text="Semester:", anchor="w", width=15).grid(row=3, column=0, sticky="w")
        tk.Label(profil_frame, text=self.mahasiswa.semester, anchor="w").grid(row=3, column=1, sticky="w")

    def lihat_jadwal(self):
        self.clear_content()
        jadwal_frame = tk.Frame(self.right_frame, padx=20, pady=20)
        jadwal_frame.pack(fill="both", expand=True, anchor="n")

        tk.Label(jadwal_frame, text="📅 Jadwal Kuliah", font=('Arial', 12, 'bold')).pack(anchor="w", pady=(0, 10))

        jadwal = self.jadwal.get(str(self.mahasiswa.semester), {})

        if not jadwal:
            tk.Label(jadwal_frame, text="Jadwal kosong.", anchor="w").pack(anchor="w")
            return

        for hari, matkul in jadwal.items():
            tk.Label(jadwal_frame, text=f"{hari}:", font=('Arial', 10, 'bold')).pack(anchor="w", pady=(5, 0))
            for m in matkul:
                matkul_text = f"  {m['mata_kuliah']['kode']} - {m['mata_kuliah']['nama']} ({m['waktu']})"
                tk.Label(jadwal_frame, text=matkul_text, anchor="w").pack(anchor="w")

    def lihat_hasil_studi(self):
        self.clear_content()
        hasil_frame = tk.Frame(self.right_frame, padx=20, pady=20)
        hasil_frame.pack(fill="both", expand=True, anchor="n")

        tk.Label(hasil_frame, text="📖 Hasil Studi Mahasiswa", font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=6, sticky="w", pady=(0, 10))

        headers = ["Kode", "Mata Kuliah", "UTS", "UAS", "Tugas", "Akhir", "Grade"]
        for col, header in enumerate(headers):
            tk.Label(hasil_frame, text=header, font=('Arial', 10, 'bold'), borderwidth=1, relief="solid", padx=5, pady=2).grid(row=1, column=col, sticky="nsew")

        hasil_list = self.mahasiswa.hasil_studi or []

        if not hasil_list:
            tk.Label(hasil_frame, text="Belum ada nilai.", anchor="w").grid(row=2, column=0, columnspan=6, sticky="w", pady=10)
            return

        for row_idx, hasil in enumerate(hasil_list, start=2):
            mk = hasil['mata_kuliah']
            n = hasil['nilai']

            data = [mk['kode'], mk['nama'], n['uts'], n['uas'], n['tugas'], n['akhir'], n['huruf']]

            for col_idx, val in enumerate(data):
                tk.Label(hasil_frame, text=val, borderwidth=1, relief="solid", padx=5, pady=2).grid(row=row_idx, column=col_idx, sticky="nsew")

    def jadwal_ujian(self):
        self.clear_content()
        ujian_frame = tk.Frame(self.right_frame, padx=20, pady=20)
        ujian_frame.pack(fill="both", expand=True, anchor="n")

        tk.Label(ujian_frame, text="📖 Jadwal Ujian Mahasiswa", font=('Arial', 12, 'bold')).pack(anchor="w", pady=(0, 10))

        semester = self.mahasiswa.semester
        ujian_semester = [ujian for ujian in self.jadwal_ujian_list if ujian['semester_id'] == semester]

        if not ujian_semester:
            tk.Label(ujian_frame, text="Belum ada jadwal ujian.", anchor="w").pack(anchor="w")
        else:
            for idx, row in enumerate(ujian_semester):
                info = f"{idx+1}. {row['kode_mk']} - {row['nama_mk']}\n   Tanggal : {row['tanggal']}\n   Waktu   : {row['waktu']}\n   Ruangan : {row['ruangan']}\n"
                tk.Label(ujian_frame, text=info, justify="left", anchor="w").pack(anchor="w", pady=5)

    def pengajuan_krs(self):
        self.clear_content()

        tk.Label(self.right_frame, text="📄 Pengajuan & Status KRS", font=('Arial', 12, 'bold')).pack(anchor="w", pady=(10, 10))

        # Ambil semua mata kuliah dari database
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="tes")
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT kode, nama FROM mata_kuliah")
        all_matkul = cursor.fetchall()

        # Cek KRS yang pernah diajukan mahasiswa ini
        cursor.execute("SELECT kode_mk, status FROM krs WHERE username = %s", (self.mahasiswa.username,))
        existing_krs = cursor.fetchall()
        existing_kode = [e['kode_mk'] for e in existing_krs]

        krs_status_dict = {e['kode_mk']: e['status'] for e in existing_krs}

        # Jika semua matkul sudah diajukan, tampilkan pesan
        if len(existing_krs) == len(all_matkul):
            tk.Label(self.right_frame, text="📌 Kamu sudah mengajukan semua mata kuliah yang tersedia.", fg="green").pack(anchor="w", pady=5)
        else:
            tk.Label(self.right_frame, text="✅ Pilih mata kuliah yang ingin diajukan:", font=('Arial', 10)).pack(anchor="w")

            var_dict = {}
            for mk in all_matkul:
                if mk['kode'] not in existing_kode:
                    var = tk.IntVar()
                    chk = tk.Checkbutton(self.right_frame, text=f"{mk['kode']} - {mk['nama']}", variable=var)
                    chk.pack(anchor='w')
                    var_dict[mk['kode']] = var

            def simpan_krs():
                conn = mysql.connector.connect(host="localhost", user="root", password="", database="tes")
                cursor = conn.cursor(dictionary=True)
                
                selected = [kode for kode, var in var_dict.items() if var.get() == 1]
                if not selected:
                    notif_label.config(text="⚠️ Pilih minimal satu mata kuliah.", fg="orange")
                    return

                try:
                    for kode in selected:
                        cursor.execute(
                            "INSERT INTO krs (username, kode_mk, semester, status) VALUES (%s, %s, %s, 'Diajukan')",
                            (self.mahasiswa.username, kode, self.mahasiswa.semester)
                        )
                    conn.commit()
                    notif_label.config(text="✅ Pengajuan KRS berhasil dikirim.", fg="green")
                    self.right_frame.after(500, self.pengajuan_krs)  # Tunggu 0.5 detik sebelum refresh

                except mysql.connector.Error as err:
                    notif_label.config(text=f"❌ Gagal menyimpan KRS: {err}", fg="red")

            if var_dict:
                notif_label = tk.Label(self.right_frame, text="", font=('Arial', 10, 'bold'))
                notif_label.pack(pady=(5, 5))
                tk.Button(self.right_frame, text="Ajukan KRS", command=simpan_krs).pack(pady=10)

        # Tampilkan daftar status KRS yang pernah diajukan
        tk.Label(self.right_frame, text="📊 Status Pengajuan KRS:", font=('Arial', 10, 'bold')).pack(anchor="w", pady=(10, 5))

        if not existing_krs:
            tk.Label(self.right_frame, text="Belum ada KRS yang diajukan.", anchor="w").pack(anchor="w")
        else:
            for e in existing_krs:
                status_color = {"Diajukan": "#2980b9", "Diterima": "#27ae60", "Ditolak": "#c0392b"}.get(e['status'], "black")
                status_text = f"{e['kode_mk']} - Status: {e['status']}"
                tk.Label(self.right_frame, text=status_text, fg=status_color).pack(anchor="w")

        conn.close()

    def feedback_dosen(self):
        self.clear_content()

        # Ambil daftar matkul sesuai semester dan status diterima
        matkul = load_feedback_matkul(self.mahasiswa.username, self.mahasiswa.semester)

        if not matkul:
            tk.Label(
                self.right_frame,
                text="📌 Tidak ada mata kuliah yang dapat diberi feedback di semester ini.",
                fg="red",
                font=('Arial', 10)
            ).pack(pady=10)
            return

        tk.Label(self.right_frame, text="🗣️ Feedback Dosen", font=('Arial', 12, 'bold')).pack(pady=(10, 10))

        mk_var = tk.StringVar()
        ttk.Label(self.right_frame, text="Pilih Mata Kuliah:").pack(anchor="w", padx=10)
        ttk.Combobox(
            self.right_frame,
            textvariable=mk_var,
            values=[f"{m['kode_mk']} - {m['nama']}" for m in matkul],
            state="readonly"
        ).pack(pady=5)

        nilai_var = tk.IntVar()
        ttk.Label(self.right_frame, text="Nilai (1-5):").pack(anchor="w", padx=10, pady=(10, 0))
        ttk.Combobox(
            self.right_frame,
            textvariable=nilai_var,
            values=[1, 2, 3, 4, 5],
            state="readonly"
        ).pack(pady=5)

        ttk.Label(self.right_frame, text="Komentar:").pack(anchor="w", padx=10, pady=(10, 0))
        komentar_text = tk.Text(self.right_frame, height=5, width=50)
        komentar_text.pack(pady=5)

        # Label notifikasi
        notif_label = tk.Label(self.right_frame, text="", font=('Arial', 10, 'bold'))
        notif_label.pack(pady=(5, 5))

        def kirim_feedback():
            if not mk_var.get() or not nilai_var.get():
                notif_label.config(text="⚠️ Lengkapi data feedback.", fg="orange")
                return

            kode_mk = mk_var.get().split(' - ')[0]
            komentar = komentar_text.get("1.0", tk.END).strip()

            try:
                conn = mysql.connector.connect(host="localhost", user="root", password="", database="tes")
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO feedback (username, kode_mk, nilai, komentar) VALUES (%s, %s, %s, %s)",
                    (self.mahasiswa.username, kode_mk, nilai_var.get(), komentar)
                )
                conn.commit()
                conn.close()
                notif_label.config(text="✅ Feedback berhasil dikirim.", fg="green")
                self.right_frame.after(500, self.feedback_dosen)
                # Reset form
                mk_var.set("")
                nilai_var.set("")
                komentar_text.delete("1.0", tk.END)
            except mysql.connector.Error as err:
                notif_label.config(text=f"❌ Gagal mengirim feedback: {err}", fg="red")

        tk.Button(self.right_frame, text="Kirim Feedback", command=kirim_feedback).pack(pady=10)

    def logout(self):
        self.window.destroy()
        root.deiconify()
        
class DosenControllerGUI:
    def __init__(self, dosen, mahasiswa_list, jadwal):
        self.dosen = dosen
        self.mahasiswa_list = mahasiswa_list
        self.jadwal = jadwal

        self.window = tk.Toplevel()
        self.window.title(f"Dashboard ReGima Dosen - {dosen.nama}")
        self.window.geometry("700x450")

        # Frame utama pembungkus kiri-kanan
        main_frame = tk.Frame(self.window)
        main_frame.pack(fill="both", expand=True)

        # Navigasi (kiri)
        nav_frame = tk.Frame(main_frame, width=150, bg="#0050d9")
        nav_frame.pack(side="left", fill="y")

        # Separator vertikal
        separator = ttk.Separator(main_frame, orient="vertical")
        separator.pack(side="left", fill="y", padx=5)

        # Area Konten (kanan)
        self.content_frame = tk.Frame(main_frame)
        self.content_frame.pack(side="right", fill="both", expand=True)

        button_style = {
            "bg": "#0050d9",              # warna dasar tombol
            "fg": "#FFFFFF",              # warna teks
            "activebackground": "#0c0051",# warna saat hover
            "activeforeground": "#FFFFFF",# warna teks saat hover
            "relief": "flat",             # model border datar
            "bd": 0,                      # border width 0
            "font": ("Arial", 10),
            "anchor": 'w'
        }
        # Tombol menu
        tk.Button(nav_frame, text="📋 Daftar Mahasiswa", command=self.daftar_mahasiswa, **button_style).pack(fill='x', padx=10, pady=5)
        tk.Button(nav_frame, text="📅 Jadwal Dosen", command=self.jadwal_dosen, **button_style).pack(fill='x', padx=10, pady=5)
        tk.Button(nav_frame, text="📊 Tabel Nilai", command=self.tabel_nilai, **button_style).pack(fill='x', padx=10, pady=5)
        tk.Button(nav_frame, text="📈 Grafik Nilai", command=self.grafik_nilai, **button_style).pack(fill='x', padx=10, pady=5)
        tk.Button(nav_frame, text="📄 Validasi KRS", command=self.validasi_krs, **button_style).pack(fill='x', padx=10, pady=5)
        tk.Button(nav_frame, text="🔙 Logout", command=self.logout,fg="white", bg="#f9623d").pack(fill='x', padx=10, pady=120)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def daftar_mahasiswa(self):
        self.clear_content()

        # === Judul ===
        tk.Label(
            self.content_frame,
            text="📋 Daftar Mahasiswa Bimbingan",
            font=('Arial', 14, 'bold'),
            anchor="w"
        ).pack(anchor="w", padx=10, pady=(10, 5))

        # === Frame Filter ===
        filter_frame = tk.Frame(self.content_frame)
        filter_frame.pack(fill="x", padx=10)

        tk.Label(filter_frame, text="Cari Nama:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        search_entry = tk.Entry(filter_frame)
        search_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(filter_frame, text="Semester:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        semester_var = tk.StringVar()
        semester_cb = ttk.Combobox(filter_frame, textvariable=semester_var, state="readonly")
        semester_cb['values'] = [''] + sorted(set(str(m.semester) for m in self.mahasiswa_list))
        semester_cb.grid(row=0, column=3, padx=5, pady=5)

        # === Tabel Daftar Mahasiswa ===
        table_frame = tk.Frame(self.content_frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        def tampilkan_tabel():
            for widget in table_frame.winfo_children():
                widget.destroy()

            keyword = search_entry.get().lower()
            selected_semester = semester_var.get()

            filtered = [
                m for m in self.mahasiswa_list
                if (keyword in m.nama.lower()) and (str(m.semester) == selected_semester or not selected_semester)
            ]

            # Header
            headers = ["Nama", "NIM", "Semester"]
            for i, h in enumerate(headers):
                tk.Label(
                    table_frame, text=h,
                    font=('Arial', 10, 'bold'),
                    borderwidth=1,
                    relief="solid",
                    width=20,
                    bg="#dfe6e9"
                ).grid(row=0, column=i, sticky="nsew")

            # Data
            for row, m in enumerate(filtered, start=1):
                bg = "#ffffff" if row % 2 == 0 else "#f9f9f9"
                tk.Label(table_frame, text=m.nama, font=('Arial', 10), bg=bg, borderwidth=1, relief="solid").grid(row=row, column=0, sticky="nsew")
                tk.Label(table_frame, text=m.nim, font=('Arial', 10), bg=bg, borderwidth=1, relief="solid").grid(row=row, column=1, sticky="nsew")
                tk.Label(table_frame, text=m.semester, font=('Arial', 10), bg=bg, borderwidth=1, relief="solid").grid(row=row, column=2, sticky="nsew")

        def reset_filter():
            search_entry.delete(0, tk.END)
            semester_var.set('')
            tampilkan_tabel()

        # Tombol Aksi
        tk.Button(filter_frame, text="🔍 Cari", command=tampilkan_tabel).grid(row=0, column=4, padx=5, pady=5)
        tk.Button(filter_frame, text="🔄 Reset", command=reset_filter).grid(row=0, column=5, padx=5, pady=5)

        tampilkan_tabel()  # Tampilkan semua saat awal

    def jadwal_dosen(self):
        self.clear_content()

        jadwal_frame = tk.Frame(self.content_frame, padx=20, pady=20)
        jadwal_frame.pack(fill="both", expand=True, anchor="n")

        tk.Label(jadwal_frame, text="📅 Jadwal Dosen", font=('Arial', 12, 'bold')).pack(anchor="w", pady=(0, 10))

        jadwal_dosen = {}
        for semester, hari_dict in self.jadwal.items():
            for hari, daftar in hari_dict.items():
                for m in daftar:
                    mk = m['mata_kuliah']
                    if mk['kode'] in self.dosen.mata_kuliah:
                        jadwal_dosen.setdefault(hari, []).append((semester, mk['kode'], mk['nama'], m['waktu']))

        if not jadwal_dosen:
            tk.Label(jadwal_frame, text="Tidak ada jadwal.", anchor="w").pack(anchor="w")
            return

        for hari in sorted(jadwal_dosen.keys()):
            tk.Label(jadwal_frame, text=f"{hari}:", font=('Arial', 10, 'bold')).pack(anchor="w", pady=(5, 0))
            for semester, kode, nama, waktu in jadwal_dosen[hari]:
                teks = f"  Semester {semester} - {kode} - {nama} ({waktu})"
                tk.Label(jadwal_frame, text=teks, anchor="w").pack(anchor="w", padx=10)

    def tabel_nilai(self):
        self.clear_content()

        container = tk.Frame(self.content_frame, padx=20, pady=20)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="📊 Tabel Nilai Mahasiswa", font=('Arial', 12, 'bold')).pack(anchor="w", pady=(0, 10))

        matkul_var = tk.StringVar()
        matkul_list = list(set(
            (hasil['mata_kuliah']['kode'], hasil['mata_kuliah']['nama'])
            for mhs in self.mahasiswa_list
            for hasil in mhs.hasil_studi
            if hasil['mata_kuliah']['kode'] in self.dosen.mata_kuliah
        ))

        dropdown_frame = tk.Frame(container)
        dropdown_frame.pack(anchor="w", pady=(0, 10))

        tk.Label(dropdown_frame, text="Pilih Mata Kuliah:", font=('Arial', 10)).pack(side="left")
        cb = ttk.Combobox(dropdown_frame, textvariable=matkul_var,
                        values=[f"{k} - {n}" for k, n in matkul_list], state="readonly", width=40)
        cb.pack(side="left", padx=10)

        table_wrapper = tk.Frame(container)
        table_wrapper.pack(fill="both", expand=True)

        def tampil_tabel():
            for widget in table_wrapper.winfo_children():
                widget.destroy()

            selected_kode = matkul_var.get().split(' - ')[0] if matkul_var.get() else ""
            if not selected_kode:
                return

            headers = ["Nama", "NIM", "UTS", "UAS", "Tugas", "Akhir", "Huruf"]
            for col, header in enumerate(headers):
                lbl = tk.Label(table_wrapper, text=header, font=('Arial', 10, 'bold'), borderwidth=1, relief="ridge", padx=5, pady=2, bg="#e0e0e0")
                lbl.grid(row=0, column=col, sticky="nsew")

            for row_idx, m in enumerate(self.mahasiswa_list, start=1):
                for h in m.hasil_studi:
                    if h['mata_kuliah']['kode'] != selected_kode:
                        continue
                    nilai = h['nilai']

                    tk.Label(table_wrapper, text=m.nama, borderwidth=1, relief="ridge", padx=5).grid(row=row_idx, column=0, sticky="nsew")
                    tk.Label(table_wrapper, text=m.nim, borderwidth=1, relief="ridge", padx=5).grid(row=row_idx, column=1, sticky="nsew")

                    def make_editable_label(value, col_idx, jenis):
                        lbl = tk.Label(table_wrapper, text=value, borderwidth=1, relief="ridge", width=6, bg="white", cursor="hand2")
                        lbl.grid(row=row_idx, column=col_idx, sticky="nsew", padx=1)
                        lbl.bind("<Button-1>", lambda e, mhs=m, hasil=h: edit_nilai(mhs, hasil, jenis))
                        lbl.bind("<Enter>", lambda e: e.widget.config(bg="#f0f0f0"))
                        lbl.bind("<Leave>", lambda e: e.widget.config(bg="white"))

                    make_editable_label(nilai['uts'], 2, 'uts')
                    make_editable_label(nilai['uas'], 3, 'uas')
                    make_editable_label(nilai['tugas'], 4, 'tugas')

                    tk.Label(table_wrapper, text=nilai['akhir'], borderwidth=1, relief="ridge", padx=5).grid(row=row_idx, column=5, sticky="nsew")
                    tk.Label(table_wrapper, text=nilai['huruf'], borderwidth=1, relief="ridge", padx=5).grid(row=row_idx, column=6, sticky="nsew")

        def edit_nilai(mhs, hasil, jenis):
            nilai_lama = hasil['nilai'][jenis]
            nilai_baru = simpledialog.askinteger(
                f"Edit Nilai {jenis.upper()}",
                f"Masukkan nilai {jenis.upper()} untuk {mhs.nama}:",
                initialvalue=nilai_lama,
                minvalue=0,
                maxvalue=100
            )
            if nilai_baru is None:
                return

            hasil['nilai'][jenis] = nilai_baru
            uts = hasil['nilai']['uts']
            uas = hasil['nilai']['uas']
            tugas = hasil['nilai']['tugas']
            akhir = round((uts + uas + tugas) / 3, 2)
            if akhir >= 90:
                huruf = 'A'
            elif akhir >= 80:
                huruf = 'B'
            elif akhir >= 70:
                huruf = 'C'
            elif akhir >= 60:
                huruf = 'D'
            else:
                huruf = 'E'

            hasil['nilai']['akhir'] = akhir
            hasil['nilai']['huruf'] = huruf

            simpan_data_mahasiswa(self.mahasiswa_list)
            tampil_tabel()

        # Tombol tampilkan
        tk.Button(dropdown_frame, text="Tampilkan", command=tampil_tabel).pack(side="left", padx=10)

    def grafik_nilai(self):
        self.clear_content()

        container = tk.Frame(self.content_frame, padx=20, pady=20)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="📈 Grafik Distribusi Nilai", font=('Arial', 12, 'bold')).pack(anchor="w", pady=(0, 10))

        input_frame = tk.Frame(container)
        input_frame.pack(anchor="w", pady=(0, 10))

        tk.Label(input_frame, text="Pilih kode mata kuliah:", font=('Arial', 10)).pack(side="left")

        # Dropdown berisi daftar kode matkul yang diajar dosen
        kode_var = tk.StringVar()
        kode_dropdown = ttk.Combobox(input_frame, textvariable=kode_var, state="readonly", width=20)
        kode_dropdown['values'] = self.dosen.mata_kuliah
        kode_dropdown.pack(side="left", padx=5)

        chart_frame = tk.Frame(container)
        chart_frame.pack(fill="both", expand=True)

        def tampilkan_grafik():
            for widget in chart_frame.winfo_children():
                widget.destroy()

            kode_matkul = kode_var.get().strip()
            rentang = {'90-100':0, '80-89':0, '70-79':0, '60-69':0, '<60':0}
            for m in self.mahasiswa_list:
                for h in m.hasil_studi:
                    if h['mata_kuliah']['kode'] == kode_matkul:
                        try:
                            nilai = float(h['nilai']['akhir'])
                            if nilai >= 90: rentang['90-100'] += 1
                            elif nilai >= 80: rentang['80-89'] += 1
                            elif nilai >= 70: rentang['70-79'] += 1
                            elif nilai >= 60: rentang['60-69'] += 1
                            else: rentang['<60'] += 1
                        except: continue

            if sum(rentang.values()) == 0:
                tk.Label(chart_frame, text="Belum ada data nilai untuk mata kuliah ini.", fg="red").pack(pady=10)
                return

            fig = Figure(figsize=(6, 4), dpi=100)
            ax = fig.add_subplot(111)
            bars = ax.bar(rentang.keys(), rentang.values(), color='#4faaff', edgecolor='black')
            ax.set_title(f"Distribusi Nilai untuk {kode_matkul}", fontsize=11)
            ax.set_ylabel("Jumlah Mahasiswa")
            ax.set_xlabel("Rentang Nilai")

            # Menambahkan label jumlah di atas tiap bar
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2, height + 0.2, str(height), ha='center', fontsize=9)

            canvas = FigureCanvasTkAgg(fig, master=chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        # Tombol tampilkan grafik
        tk.Button(input_frame, text="Tampilkan Grafik", command=tampilkan_grafik).pack(side="left", padx=10)

    def validasi_krs(self):
        self.clear_content()

        tk.Label(self.content_frame, text="📄 Validasi Pengajuan KRS", font=('Arial', 14, 'bold')).pack(anchor="w", padx=10, pady=(10, 5))

        # === SCROLLABLE CANVAS ===
        canvas = tk.Canvas(self.content_frame)
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # === LOAD DATA KRS YANG PERLU DIVALIDASI SAJA ===
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="tes")
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT k.id, m.nama AS nama_mhs, k.kode_mk, mk.nama AS nama_mk, k.semester, k.status
            FROM krs k
            JOIN mahasiswa m ON k.username = m.username
            JOIN mata_kuliah mk ON k.kode_mk = mk.kode
            WHERE k.status = 'Diajukan'
            ORDER BY m.nama
        """)
        data_krs = cursor.fetchall()
        conn.close()

        # === HEADER ===
        headers = ["Mahasiswa", "Kode MK", "Nama MK", "Semester", "Status", "Aksi"]
        for col, h in enumerate(headers):
            tk.Label(scrollable_frame, text=h, font=('Arial', 10, 'bold'),
                    borderwidth=1, relief="ridge", padx=5, pady=2, bg="#e0e0e0").grid(row=0, column=col, sticky="nsew")

        for row_idx, krs in enumerate(data_krs, start=1):
            bg = "#ffffff" if row_idx % 2 == 0 else "#f9f9f9"
            tk.Label(scrollable_frame, text=krs['nama_mhs'], bg=bg, borderwidth=1, relief="ridge", padx=5).grid(row=row_idx, column=0, sticky="nsew")
            tk.Label(scrollable_frame, text=krs['kode_mk'], bg=bg, borderwidth=1, relief="ridge", padx=5).grid(row=row_idx, column=1, sticky="nsew")
            tk.Label(scrollable_frame, text=krs['nama_mk'], bg=bg, borderwidth=1, relief="ridge", padx=5).grid(row=row_idx, column=2, sticky="nsew")
            tk.Label(scrollable_frame, text=krs['semester'], bg=bg, borderwidth=1, relief="ridge", padx=5).grid(row=row_idx, column=3, sticky="nsew")
            tk.Label(scrollable_frame, text=krs['status'], bg=bg, borderwidth=1, relief="ridge", padx=5).grid(row=row_idx, column=4, sticky="nsew")

            # Tombol Aksi
            aksi_frame = tk.Frame(scrollable_frame, bg=bg)
            aksi_frame.grid(row=row_idx, column=5, sticky="nsew", padx=2, pady=2)

            def make_action_button(krs_id, new_status):
                return lambda: self.update_status_krs(krs_id, new_status)

            tk.Button(aksi_frame, text="Terima", font=("Arial", 8), bg="#27ae60", fg="white",
                    command=make_action_button(krs['id'], "Diterima")).pack(side="left", padx=2)
            tk.Button(aksi_frame, text="Tolak", font=("Arial", 8), bg="#c0392b", fg="white",
                    command=make_action_button(krs['id'], "Ditolak")).pack(side="left", padx=2)

    def update_status_krs(self, krs_id, new_status):
        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="", database="tes")
            cursor = conn.cursor()
            cursor.execute("UPDATE krs SET status = %s WHERE id = %s", (new_status, krs_id))
            conn.commit()
            conn.close()
            self.validasi_krs()  # Refresh tampilan agar baris hilang
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Gagal update status:\n{err}")

    def logout(self):
        self.window.destroy()
        root.deiconify()

        
# ===== LOGIN GUI =====
# ===== LOGIN GUI =====
def login_gui():
    def do_login():
        u, p = username.get(), password.get()
        role = role_var.get()

        if role == "Mahasiswa":
            for m in mahasiswa_list:
                if m.username == u and m.password == p:
                    root.withdraw()  # sembunyikan login window
                    MahasiswaControllerGUI(m, jadwal, jadwal_ujian_list, paket_semester_list)

                    return
        elif role == "Dosen":
            for d in dosen_list:
                if d.username == u and d.password == p:
                    root.withdraw()  # sembunyikan login window
                    DosenControllerGUI(d, mahasiswa_list, jadwal)
                    return
        messagebox.showerror("Error", "Login gagal.")

    global root
    root = tk.Tk()
    root.title("Login ReGIMA")
    root.geometry("700x450")
    root.resizable(False, False)

    # Frame kiri (logo)
    left_frame = tk.Frame(root, bg="#0050d9", width=400)
    left_frame.pack(side="left", fill="y")

    logo_label = tk.Label(left_frame, text="ReGIMA", fg="#f4f422", bg="#0050d9",
                          font=("Poppins", 36, "bold"))
    logo_label.place(relx=0.5, rely=0.5, anchor="center")

    # Frame kanan (form login)
    right_frame = tk.Frame(root, bg="white")
    right_frame.pack(side="right", expand=True, fill="both")

    welcome_label = tk.Label(right_frame, text="Selamat datang di ReGima",
                             font=("Poppins", 14, "bold"), bg="white", fg="#333")
    welcome_label.pack(pady=(50, 20))

    username = tk.Entry(right_frame, font=("Poppins", 12), relief="solid", bd=1)
    username.insert(0, "Username")
    username.pack(pady=10, ipadx=10, ipady=5)

    password = tk.Entry(right_frame, show="*", font=("Poppins", 12), relief="solid", bd=1)
    password.insert(0, "Password")
    password.pack(pady=10, ipadx=10, ipady=5)

    role_var = tk.StringVar()
    role_dropdown = ttk.Combobox(right_frame, textvariable=role_var,
                                 values=["Mahasiswa", "Dosen"], state="readonly", font=("Poppins", 12))
    role_dropdown.set("Login Sebagai")
    role_dropdown.pack(pady=10, ipadx=1, ipady=5)

    login_button = tk.Button(right_frame, text="Login", command=do_login,
                             font=("Poppins", 12), bg="white", relief="solid", bd=1)
    login_button.pack(pady=30, ipadx=10, ipady=5)

    root.mainloop()

# ===== MAIN =====
mahasiswa_list = load_data_mahasiswa()
dosen_list = load_data_dosen()
jadwal = load_jadwal()
jadwal_ujian_list = load_jadwal_ujian()
paket_semester_list = load_paket_semester()
login_gui()
