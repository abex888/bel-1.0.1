import tkinter as tk
import sqlite3
from tkinter import ttk
from datetime import datetime, timedelta

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

        # Buat tabel jadwal jika belum ada
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS jadwal (
                hari text PRIMARY KEY,
                jam_upacara text,
                jam_masuk text,
                jam_istirahat text,
                jam_masuk_setelah_istirahat text,
                jam_pulang text
            )
        """)

    def insert_jadwal(self, hari, jam_upacara, jam_masuk, jam_istirahat, jam_masuk_setelah_istirahat, jam_pulang):
        self.cursor.execute("""
            INSERT INTO jadwal (hari, jam_upacara, jam_masuk, jam_istirahat, jam_masuk_setelah_istirahat, jam_pulang)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (hari, jam_upacara, jam_masuk, jam_istirahat, jam_masuk_setelah_istirahat, jam_pulang))
        self.connection.commit()

    def get_jadwal(self, hari):
        self.cursor.execute("""
            SELECT * FROM jadwal WHERE hari = ?
        """, (hari,))
        return self.cursor.fetchone()

    def update_jadwal(self, hari, jam_upacara, jam_masuk, jam_istirahat, jam_masuk_setelah_istirahat, jam_pulang):
        self.cursor.execute("""
            UPDATE jadwal
            SET jam_upacara = ?, jam_masuk = ?, jam_istirahat = ?, jam_masuk_setelah_istirahat = ?, jam_pulang = ?
            WHERE hari = ?
        """, (jam_upacara, jam_masuk, jam_istirahat, jam_masuk_setelah_istirahat, jam_pulang, hari))
        self.connection.commit()

    def delete_jadwal(self, hari):
        self.cursor.execute("""
            DELETE FROM jadwal WHERE hari = ?
        """, (hari,))
        self.connection.commit()

class JadwalApp:
    def __init__(self):
        self.db = Database('jadwal.db')

        # Buat jendela utama
        self.window = tk.Tk()
        self.window.title("Jadwal Kelas")
        self.window.geometry("300x220")
        self.window.resizable(False, False)

        # Buat frame untuk input data
        self.input_frame = tk.Frame(self.window)
        self.input_frame.pack(pady=10)

        # Hari dropdown options
        hari_options = ["Pilih hari", "Senin", "Selasa", "Rabu", "Kamis", "Jumat"]

        # Hari dropdown
        self.hari_var = tk.StringVar(self.window)
        self.hari_var.set(hari_options[0])  # Set default value
        self.hari_dropdown = ttk.OptionMenu(self.input_frame, self.hari_var, *hari_options, command=self.display_jadwal)
        self.hari_dropdown.grid(row=0, column=1, sticky=tk.W)

        # Label dan entri untuk jam upacara
        self.jam_upacara_label = tk.Label(self.input_frame, text="Jam Upacara/Kumpul:")
        self.jam_upacara_label.grid(row=1, column=0, sticky=tk.W)
        self.jam_upacara_entry = tk.Entry(self.input_frame)
        self.jam_upacara_entry.grid(row=1, column=1, sticky=tk.W)

        # Label dan entri untuk jam masuk
        self.jam_masuk_label = tk.Label(self.input_frame, text="Jam Masuk:")
        self.jam_masuk_label.grid(row=2, column=0, sticky=tk.W)
        self.jam_masuk_entry = tk.Entry(self.input_frame)
        self.jam_masuk_entry.grid(row=2, column=1, sticky=tk.W)

        # Label dan entri untuk jam istirahat
        self.jam_istirahat_label = tk.Label(self.input_frame, text="Jam Istirahat:")
        self.jam_istirahat_label.grid(row=3, column=0, sticky=tk.W)
        self.jam_istirahat_entry = tk.Entry(self.input_frame)
        self.jam_istirahat_entry.grid(row=3, column=1, sticky=tk.W)

        # Label dan entri untuk jam masuk setelah istirahat
        self.jam_masuk_setelah_istirahat_label = tk.Label(self.input_frame, text="Jam Masuk Setelah Istirahat:")
        self.jam_masuk_setelah_istirahat_label.grid(row=4, column=0, sticky=tk.W)
        self.jam_masuk_setelah_istirahat_entry = tk.Entry(self.input_frame)
        self.jam_masuk_setelah_istirahat_entry.grid(row=4, column=1, sticky=tk.W)

        # Label dan entri untuk jam pulang
        self.jam_pulang_label = tk.Label(self.input_frame, text="Jam Pulang:")
        self.jam_pulang_label.grid(row=5, column=0, sticky=tk.W)
        self.jam_pulang_entry = tk.Entry(self.input_frame)
        self.jam_pulang_entry.grid(row=5, column=1, sticky=tk.W)

        # Create frame for displaying data
        self.data_frame = tk.Frame(self.window)
        self.data_frame.pack()

        # Create the data label
        self.data_label = tk.Label(self.data_frame, text="")
        self.data_label.pack()

        # Tombol simpan
        self.simpan_button = tk.Button(self.window, text="Simpan", command=self.simpan_jadwal)
        self.simpan_button.pack(pady=10)

    def display_jadwal(self, selected_hari):
        jadwal = self.db.get_jadwal(selected_hari)
        if jadwal:
            # Insert the schedule data into the entry fields
            self.jam_upacara_entry.delete(0, tk.END)
            self.jam_upacara_entry.insert(0, jadwal[1])
            self.jam_masuk_entry.delete(0, tk.END)
            self.jam_masuk_entry.insert(0, jadwal[2])
            self.jam_istirahat_entry.delete(0, tk.END)
            self.jam_istirahat_entry.insert(0, jadwal[3])
            self.jam_masuk_setelah_istirahat_entry.delete(0, tk.END)
            self.jam_masuk_setelah_istirahat_entry.insert(0, jadwal[4])
            self.jam_pulang_entry.delete(0, tk.END)
            self.jam_pulang_entry.insert(0, jadwal[5])

        else:
            self.data_label.config(text="Jadwal tidak ditemukan untuk hari {}".format(selected_hari))
            self.jam_upacara_entry.delete(0, tk.END)
            self.jam_masuk_entry.delete(0, tk.END)
            self.jam_istirahat_entry.delete(0, tk.END)
            self.jam_masuk_setelah_istirahat_entry.delete(0, tk.END)
            self.jam_pulang_entry.delete(0, tk.END)

    def simpan_jadwal(self):
        hari = self.hari_var.get()
        jam_upacara = self.jam_upacara_entry.get()
        jam_masuk = self.jam_masuk_entry.get()
        jam_istirahat = self.jam_istirahat_entry.get()
        jam_masuk_setelah_istirahat = self.jam_masuk_setelah_istirahat_entry.get()
        jam_pulang = self.jam_pulang_entry.get()

        if self.db.get_jadwal(hari):
            # If schedule exists, update it
            self.db.update_jadwal(hari, jam_upacara, jam_masuk, jam_istirahat, jam_masuk_setelah_istirahat, jam_pulang)
            self.data_label.config(text="Jadwal berhasil diperbarui")
        else:
            # If schedule doesn't exist, insert it
            try:
                self.db.insert_jadwal(hari, jam_upacara, jam_masuk, jam_istirahat, jam_masuk_setelah_istirahat,
                                      jam_pulang)
                self.data_label.config(text="Jadwal berhasil disimpan")
            except sqlite3.IntegrityError:
                self.data_label.config(text="Jadwal untuk hari ini sudah ada")

        self.data_label.config(text="Jadwal berhasil disimpan")

    def ubah_jadwal(self):
        hari = self.hari_var.get()
        jadwal = self.db.get_jadwal(hari)

        if jadwal:
            self.jam_upacara_entry.delete(0, tk.END)
            self.jam_upacara_entry.insert(0, jadwal[1])
            self.jam_masuk_entry.delete(0, tk.END)
            self.jam_masuk_entry.insert(0, jadwal[2])
            self.jam_istirahat_entry.delete(0, tk.END)
            self.jam_istirahat_entry.insert(0, jadwal[3])
            self.jam_masuk_setelah_istirahat_entry.delete(0, tk.END)
            self.jam_masuk_setelah_istirahat_entry.insert(0, jadwal[4])
            self.jam_pulang_entry.delete(0, tk.END)
            self.jam_pulang_entry.insert(0, jadwal[5])
        else:
            self.data_label.config(text="Jadwal tidak ditemukan")


    def hapus_jadwal(self):
        hari = self.hari_entry.get()
        self.db.delete_jadwal(hari)

        self.data_label.config(text="Jadwal berhasil dihapus")

if __name__ == "__main__":
    app = JadwalApp()
    app.window.mainloop()
