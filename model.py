import datetime

class Tugas:
    def __init__(self,nama_tugas:str,matkul:str,prioritas:int,tenggat_waktu:datetime.date,status="Belum Dikerjakan",id_tugas: int |None=None):
        self.id=id_tugas
        self.matkul=matkul
        self.tugas=nama_tugas
        self.prioritas=prioritas
        self.tenggat_waktu=tenggat_waktu
        self.status=status

    def __repr__(self):
        return f"Tugas(id={self.id}, nama='{self.tugas}', status='{self.status}')"
    

