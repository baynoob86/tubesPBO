import datetime
import pandas as pd
from model import Tugas 
import database

class ManajerTugas:
    _db_setup_done = False
    
    def __init__(self):
        # Logika setup database bisa disederhanakan karena kita akan menjalankannya manual
        pass

    def tambah_tugas(self, tugas: Tugas) -> bool: 
        sql = "INSERT INTO tugas (nama_tugas, matkul, prioritas, tenggat_waktu, status) VALUES (?, ?, ?, ?, ?)"
        params = (tugas.tugas, tugas.matkul, tugas.prioritas, tugas.tenggat_waktu, tugas.status)
        last_id = database.execute_query(sql, params)
        if last_id is not None:
            tugas.id = last_id
            return True
        return False

    def hapus_tugas(self, id_tugas: int) -> bool:
        sql = "DELETE FROM tugas WHERE id = ?"
        params = (id_tugas,)
        hasil = database.execute_query(sql, params)
        return hasil is not None
        
    def get_semua_tugas_obj(self) -> list[Tugas]: 
        sql = "SELECT id, nama_tugas, matkul, prioritas, tenggat_waktu, status FROM tugas ORDER BY tenggat_waktu ASC, prioritas DESC"
        rows = database.fetch_query(sql, fetch_all=True)
        tugas_list = []
        if rows:
            for row in rows:
                tugas_list.append(
                    Tugas(
                        id_tugas=row['id'],
                        nama_tugas=row['nama_tugas'],
                        matkul=row['matkul'],
                        prioritas=row['prioritas'],
                        tenggat_waktu=row['tenggat_waktu'],
                        status=row['status']
                    )
                )
        return tugas_list

    def get_dataframe_tugas(self) -> pd.DataFrame: 
        query = "SELECT nama_tugas as 'Nama Tugas', matkul as 'Mata Kuliah', " \
                "prioritas as 'Prioritas', tenggat_waktu as 'Tenggat Waktu', " \
                "status as 'Status' FROM tugas ORDER BY tenggat_waktu ASC, id DESC"
        df = database.get_dataframe(query)
        return df

    def hitung_statistik_tugas(self) -> dict: 
        total_tugas = database.fetch_query("SELECT COUNT(*) FROM tugas", fetch_all=False)[0]
        tugas_selesai = database.fetch_query("SELECT COUNT(*) FROM tugas WHERE status = 'Selesai'", fetch_all=False)[0]
        
        return {
            "total": total_tugas or 0,
            "selesai": tugas_selesai or 0,
            "belum_selesai": (total_tugas or 0) - (tugas_selesai or 0)
        }

    def get_tugas_per_matkul(self) -> dict: 
        sql = "SELECT matkul, COUNT(*) FROM tugas GROUP BY matkul ORDER BY COUNT(*) DESC"
        rows = database.fetch_query(sql, fetch_all=True)
        hasil = {}
        if rows:
            for row in rows:
                hasil[row['matkul']] = row[1]
        return hasil
