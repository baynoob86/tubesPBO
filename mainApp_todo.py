import streamlit as st
import datetime
import pandas as pd

try:
    from model import Tugas
    from manajer_tugas import ManajerTugas
    from konfigurasi import Matkul, STATUS_TUGAS
except ImportError as e:
    st.error(f"Gagal mengimpor modul: {e}. Pastikan semua file .py ada di folder yang sama.")
    st.stop()

# Konfigurasi halaman
st.set_page_config(
    page_title="Aplikasi To-Do List",
    page_icon="🤦‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cache resource untuk pengelola tugas
@st.cache_resource
def get_tugas_manager():
    return ManajerTugas()

manajer = get_tugas_manager()

# === Halaman Input ===
def halaman_tambah(manajer: ManajerTugas):
    st.header("➕ Tambah Tugas Baru")
    with st.form("form_tugas_baru", clear_on_submit=True):
        nama_tugas = st.text_area("Nama Tugas*", placeholder="Contoh: Belajar Streamlit...")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            matkul = st.selectbox("Mata Kuliah:", Matkul, index=0)
        with col2:
            prioritas = st.slider("Prioritas (1=Rendah, 5=Tinggi):", 1, 5, 3)
        with col3:
            tenggat_waktu = st.date_input("Tenggat Waktu:", value=datetime.date.today())

        status = st.selectbox("Status:", STATUS_TUGAS, index=0)

        submitted = st.form_submit_button("Simpan Tugas")
        if submitted:
            if not nama_tugas:
                st.warning("Nama tugas tidak boleh kosong!")
            else:
                with st.spinner("Menyimpan..."):
                    tugas_baru = Tugas(nama_tugas, matkul, prioritas, tenggat_waktu, status)
                    if manajer.tambah_tugas(tugas_baru):
                        st.success("Tugas berhasil disimpan!")
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.error("Gagal menyimpan tugas.")

# === Halaman Daftar Tugas ===
def halaman_daftar(manajer: ManajerTugas):
    st.header("📋 Daftar Semua Tugas 😭")
    button= st.button("🔄 Refresh Daftar Tugas")

    if button:
        st.cache_data.clear()
        st.rerun()

    with st.spinner("Memuat daftar tugas..."):
        df_tugas = manajer.get_dataframe_tugas()

    if df_tugas.empty:
        st.info("Belum ada tugas. Silakan tambahkan tugas baru!")
    else:
        st.dataframe(df_tugas, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.subheader("🗑️ Hapus Tugas")
        
        semua_tugas = manajer.get_semua_tugas_obj()
        pilihan_dict = {f"{t.tugas[:50]}": t.id for t in semua_tugas}
        
        pilihan_hapus = st.selectbox("Pilih tugas untuk dihapus:", options=pilihan_dict.keys(), index=None, placeholder="Pilih tugas...")

        if pilihan_hapus and st.button("Hapus Tugas", type="primary"):
            id_to_delete = pilihan_dict[pilihan_hapus]
            with st.spinner("Menghapus..."):
                if manajer.hapus_tugas(id_to_delete):
                    st.success("Tugas berhasil dihapus.")
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.error("Gagal menghapus tugas.")

# === Halaman Ringkasan ===
def halaman_ringkasan(manajer: ManajerTugas):
    st.header("📊 Ringkasan Tugas")
    
    stats = manajer.hitung_statistik_tugas()
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Tugas", stats['total'])
    col2.metric("✅ Selesai", stats['selesai'])
    col3.metric("⏳ Belum Selesai", stats['belum_selesai'])
    
    st.divider()
    
    st.subheader("Tugas per Matkul")
    data_per_matkul = manajer.get_tugas_per_matkul()
    
    if not data_per_matkul:
        st.info("Tidak ada data mata kuliah untuk ditampilkan.")
    else:
        df_matkul = pd.DataFrame(list(data_per_matkul.items()), columns=['Mata Kuliah', 'Jumlah Tugas'])
        st.bar_chart(df_matkul.set_index('Mata Kuliah'))

# === Fungsi Utama ===
def main():
    st.sidebar.title("✅ To-Do List App")
    menu_pilihan = st.sidebar.radio("Pilih Menu:", ["Tambah Tugas", "Daftar Tugas", "Ringkasan"], key="menu_utama")
    st.sidebar.markdown("---")
    # st.sidebar.info("Aplikasi sederhana dengan Python & Streamlit.")

    if menu_pilihan == "Tambah Tugas":
        halaman_tambah(manajer)
    elif menu_pilihan == "Daftar Tugas":
        halaman_daftar(manajer)
    elif menu_pilihan == "Ringkasan":
        halaman_ringkasan(manajer)

if __name__ == "__main__":
    main()