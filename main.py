import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Importing Pillow for image handling
from datetime import datetime
import sqlite3
import suara  # Pastikan modul suara ada dan diimport
from jadwal import JadwalApp  # Pastikan modul jadwal ada dan diimport

deskripsi = '''
BEL SEKOLAH SMP NEGERI 2 BOJONGPICUNG
Penulis		: Aries Aprilian (abex888@gmail.com)
Versi		: 1.0.1
Lisensi		: GNU GPL versi 3

========================================
PENJELASAN:
Program ini akan membunyikan bel sesuai dengan jadwal per hari. Jadwal diambil dari database jadwal yang dapat diatur menggunakan tombol atur jadwal.
'''

keterangan = '''
F1 menampilkan pesan program
F2 membunyikan bel masuk
F3 membunyikan bel pulang
F4 membunyikan bel istirahat
F5 membunyikan bel kumpul
'''

# Fungsi Tentang Program
def tentang_program():
    messagebox.showinfo("Tentang Program", deskripsi + keterangan)

# Fungsi untuk memperbarui waktu
def update_time():
    now = datetime.now()
    time_str = now.strftime("%H:%M:%S")
    day_str = days_id[now.strftime("%A")]
    date_str = now.strftime("%d")
    month_str = months_id[now.strftime("%B")]
    year_str = now.strftime("%Y")
    full_date_str = f"{day_str}, {date_str} {month_str} {year_str}"
    time_label.config(text=time_str)
    date_label.config(text=full_date_str)
    check_schedule(now)
    root.after(1000, update_time)

# Fungsi untuk menampilkan jadwal hari ini
def show_schedule():
    # Map English day names to Bahasa Indonesia
    english_to_indonesian_days = {
        "Monday": "Senin",
        "Tuesday": "Selasa",
        "Wednesday": "Rabu",
        "Thursday": "Kamis",
        "Friday": "Jumat",
        "Saturday": "Sabtu",
        "Sunday": "Minggu"
    }

    # Get the current day in English and convert to Bahasa Indonesia
    current_day_english = datetime.now().strftime("%A")
    day = english_to_indonesian_days.get(current_day_english, "")

    print(f"Current day: {day}")  # Debug: Print the current day in Bahasa Indonesia

    with sqlite3.connect("jadwal.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM jadwal WHERE hari=?", (day,))
        schedules = cursor.fetchall()

        print(f"Schedules fetched: {schedules}")  # Debug: Print the fetched schedules

        if schedules:
            # Initialize an empty string to accumulate all schedule entries
            schedule_text = ""
            for schedule in schedules:
                # Format each schedule entry
                schedule_text += (f"Upacara: {schedule[1]}\n"
                                  f"Masuk: {schedule[2]}\n"
                                  f"Istirahat: {schedule[3]}\n"
                                  f"Masuk Setelah Istirahat: {schedule[4]}\n"
                                  f"Pulang: {schedule[5]}\n\n")
            # Remove trailing newlines
            schedule_text = schedule_text.strip()
        else:
            schedule_text = "Tidak ada jadwal"

        schedule_label.config(text=schedule_text)


# Fungsi untuk mengatur jadwal
def set_schedule():
    JadwalApp()

# Fungsi untuk membunyikan bel
def ring_bell(bell_type):
    if bell_type == "masuk":
        suara.suara_masuk()
    elif bell_type == "pulang":
        suara.suara_pulang()
    elif bell_type == "istirahat":
        suara.suara_istirahat()
    elif bell_type == "kumpul":
        suara.suara_kumpul()
    print(f"Bel {bell_type} dibunyikan!")

# Fungsi untuk memeriksa jadwal dan membunyikan bel
def check_schedule(now):
    day = days_id[now.strftime("%A")]
    current_time = now.strftime("%H:%M")
    with sqlite3.connect("jadwal.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM jadwal WHERE hari=?", (day,))
        schedule = cursor.fetchone()
        if schedule:
            # Periksa setiap waktu dalam jadwal dan bandingkan dengan waktu saat ini
            if current_time == schedule[1]:
                ring_bell("kumpul")
            elif current_time == schedule[2]:
                ring_bell("masuk")
            elif current_time == schedule[3]:
                ring_bell("istirahat")
            elif current_time == schedule[4]:
                ring_bell("masuk")
            elif current_time == schedule[5]:
                ring_bell("pulang")

# Fungsi untuk menghentikan suara
def stop_sound():
    import pygame
    pygame.mixer.music.stop()


# Konversi nama hari ke dalam bahasa Indonesia
days_id = {
    "Monday": "Senin",
    "Tuesday": "Selasa",
    "Wednesday": "Rabu",
    "Thursday": "Kamis",
    "Friday": "Jumat",
    "Saturday": "Sabtu",
    "Sunday": "Minggu"
}

# Konversi nama bulan ke dalam bahasa Indonesia
months_id = {
    "January": "Januari",
    "February": "Februari",
    "March": "Maret",
    "April": "April",
    "May": "Mei",
    "June": "Juni",
    "July": "Juli",
    "August": "Agustus",
    "September": "September",
    "October": "Oktober",
    "November": "November",
    "December": "Desember"
}

# Membuat GUI utama
root = tk.Tk()
root.title("Bel Sekolah SMPN 2 Bojongpicung")
root.geometry("400x350")
root.resizable(False, False)
root.iconbitmap("smp2.ico")  # Use .ico format for Windows

# Membuat frame untuk judul
judul_frame = tk.Frame(root)
judul_frame.grid(row=0, column=0, columnspan=2, pady=10)

# Menambahkan logo
logo_image = Image.open("smp2.png")  # Replace with your image path
logo_photo = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(judul_frame, image=logo_photo)
logo_label.grid(row=0, column=0, rowspan=2)

# Judul
judul_label1 = tk.Label(judul_frame, font=("Helvetica", 12), text="Bel Sekolah")
judul_label1.grid(row=0, column=1)
judul_label2 = tk.Label(judul_frame, font=("Helvetica", 12), text="SMPN 2 Bojongpicung")
judul_label2.grid(row=1, column=1)

# Frame Jam dan Tanggal
jam_frame = tk.Frame(root)
jam_frame.grid(row=1, column=0)

# Menampilkan jam dan tanggal
time_label = tk.Label(jam_frame, font=("Arial", 14))
time_label.grid(row=0, column=0, pady=5)
date_label = tk.Label(jam_frame, font=("Courier", 10))
date_label.grid(row=1, column=0, pady=5)

# Menampilkan jadwal hari ini
schedule_label = tk.Label(jam_frame, font=("Courier", 8), justify=tk.LEFT)
schedule_label.grid(row=2, column=0, pady=20)

# Membuat frame untuk kontrol di bawah informasi jadwal
control_frame = tk.Frame(root)
control_frame.grid(row=1, column=1, pady=20)

# Radio button untuk memilih jenis bel
bell_var = tk.StringVar()
bell_var.set("masuk")  # Nilai default

bell_options = [
    ("Bel Masuk", "masuk"),
    ("Bel Pulang", "pulang"),
    ("Bel Istirahat", "istirahat"),
    ("Bel Kumpul/Upacara", "kumpul")
]

radio_frame = tk.Frame(control_frame)
radio_frame.grid(row=0, column=0, padx=10)

for text, mode in bell_options:
    radio_button = tk.Radiobutton(radio_frame, text=text, variable=bell_var, value=mode)
    radio_button.pack(anchor=tk.W)

# Tombol untuk membunyikan bel
ring_bell_button = tk.Button(control_frame, text="Bunyikan Bel", height=1, width=10, command=lambda: ring_bell(bell_var.get()))
ring_bell_button.grid(row=1, column=0, padx=10, sticky=tk.W)

# Tombol untuk menghentikan suara
stop_button = tk.Button(control_frame, text="Stop", height=1, width=10, command=stop_sound)
stop_button.grid(row=2, column=0, padx=10, sticky=tk.W)

# Tombol untuk mengatur jadwal
set_schedule_button = tk.Button(control_frame, text="Atur Jadwal", height=1, width=10, command=set_schedule)
set_schedule_button.grid(row=3, column=0, padx=10, sticky=tk.W)

#label_informasi = tk.Label(root, font=("Arial", 2), text=keterangan)
#label_informasi.grid(row=2, column=0)

# binding F1 sampai F5
root.bind('<F1>', lambda event: tentang_program())
root.bind('<F2>', lambda event: suara.suara_masuk())
root.bind('<F3>', lambda event: suara.suara_pulang())
root.bind('<F4>', lambda event: suara.suara_istirahat())
root.bind('<F5>', lambda event: suara.suara_kumpul())

# Memulai pembaruan waktu
update_time()
show_schedule()

root.mainloop()
