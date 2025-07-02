import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NAMA_DB = 'todo_list.db'
DB_PATH = os.path.join(BASE_DIR, NAMA_DB)

Matkul = ["Sistem Tertananm", "Bahasa Inggris", "Kewarganegaraan","Basis Data II", "Kecerdasan Buatan", "PBO" ,"Lainnya"]
STATUS_TUGAS = ["Belum Dikerjakan", "Sedang Dikerjakan", "Selesai"]