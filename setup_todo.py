import sqlite3
import os
from konfigurasi import DB_PATH

def setup_database():
    print(f"Memeriksa/membuat database di: {DB_PATH}")
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        sql_create_table = """
        CREATE TABLE IF NOT EXISTS tugas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_tugas TEXT NOT NULL,
            matkul TEXT,
            prioritas INTEGER NOT NULL DEFAULT 3,
            tenggat_waktu DATE,
            status TEXT NOT NULL DEFAULT 'Belum Dikerjakan'
        );"""
        print("Membuat tabel 'tugas' (jika belum ada)...")
        cursor.execute(sql_create_table)
        conn.commit()
        print(" -> Tabel 'tugas' siap.")
        return True
    except sqlite3.Error as e:
        print(f" -> Error SQLite saat setup: {e}")
        return False
    finally:
        if conn:
            conn.close()
            print(" -> Koneksi DB setup ditutup.")

if __name__ == "__main__":
    print("--- Memulai Setup Database To-Do List ---")
    if setup_database():
        print(f"\nSetup database '{os.path.basename(DB_PATH)}' selesai.")
    else:
        print(f"\nSetup database GAGAL.")
    print("--- Setup Database Selesai ---")