import streamlit as st
from pymongo import MongoClient

# Koneksi ke MongoDB Atlas
client = MongoClient("mongodb+srv://icaa03:Nch6LzykBuiWvyEo@cluster0.rv7ql.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["TokoOnline"] 
collectionB = db["KatalogElektronik"]
collection = db["KatalogAksesoris"]  

st.markdown("<h1 style='color: pink;'> 💍 Selamat Datang Di Katalog Aksesoris 💍 </h1>", unsafe_allow_html=True)
st.markdown("### Kelompok 4")
st.markdown("### 👥 Anggota Kelompok:")
st.write("- Anisa Cikal Virgifiani (20230040261)")
st.write("- Erin Nurfajrina (20230040320)")
st.write("- M. Rifki Rivaldi (20230040154)")
st.write("- Wardatul Jannah (20230040120)")

st.divider()

# Form Input Produk Elektronik
st.markdown("<h1 style='color: SkyBlue;'>Tambah / Update Stok Produk Elektronik</h1>", unsafe_allow_html=True)
with st.form("form_tambah_produk_elektronik"):
    nama_produk = st.text_input("Nama Produk Elektronik")
    harga = st.number_input("Harga", min_value=0)
    stok_tambah = st.number_input("Tambah Stok", min_value=0)
    
    with st.expander("Spesifikasi (Opsional)"):
        ram = st.text_input("RAM")
        processor = st.text_input("Processor")
        storage = st.text_input("Storage")
    
    submit = st.form_submit_button("Simpan")
    
    if submit:
        if nama_produk and harga > 0 and stok_tambah >= 0:
            existing_product = collectionB.find_one({"nama": nama_produk})
            spesifikasi = {"RAM": ram, "Processor": processor, "Storage": storage}
            
            if existing_product:
                new_stok = existing_product["stok"] + stok_tambah
                collectionB.update_one(
                    {"nama": nama_produk},
                    {"$set": {"stok": new_stok, "harga": harga, "spesifikasi": spesifikasi}}
                )
                st.success(f"✅ Stok produk elektronik '{nama_produk}' berhasil ditambahkan! Stok sekarang: {new_stok}")
            else:
                data_produk = {
                    "nama": nama_produk,
                    "harga": harga,
                    "stok": stok_tambah,
                    "spesifikasi": spesifikasi
                }
                collectionB.insert_one(data_produk)
                st.success(f"✅ Produk elektronik baru '{nama_produk}' berhasil ditambahkan!")
        else:
            st.error("❌ Mohon isi semua data dengan benar!")

st.divider()

# Form Input Produk Aksesoris
st.markdown("<h1 style='color: pink;'>Tambah / Update Stok Produk Aksesoris</h1>", unsafe_allow_html=True)
with st.form("form_tambah_produk_aksesoris"):
    nama_produk = st.text_input("Nama Aksesoris")
    jenis_produk = st.selectbox("Jenis Aksesoris", ["Gelang", "Cincin", "Anting", "Kalung", "Jam Tangan"])
    bahan_produk = st.text_input("Bahan")
    harga = st.number_input("Harga", min_value=0)
    stok_tambah = st.number_input("Tambah Stok", min_value=0)
    link_produk = st.text_input("Link Produk")
    
    # Tombol Simpan
    submit = st.form_submit_button("Simpan")
    
    if submit:
        if nama_produk and harga > 0 and stok_tambah >= 0 and link_produk:
            # Cek apakah produk sudah ada di database
            existing_product = collection.find_one({"nama": nama_produk})
            
            if existing_product:
                # Jika produk sudah ada, update stok
                new_stok = existing_product["stok"] + stok_tambah
                collection.update_one(
                    {"nama": nama_produk},
                    {"$set": {"stok": new_stok, "harga": harga, "link": link_produk}}
                )
                st.success(f"✅ Stok aksesoris '{nama_produk}' berhasil ditambahkan! Stok sekarang: {new_stok}")
            else:
                # Jika produk belum ada, tambahkan baru
                data_produk = {
                    "nama": nama_produk,
                    "jenis": jenis_produk,
                    "bahan": bahan_produk,
                    "harga": harga,
                    "stok": stok_tambah,
                    "link": link_produk
                }
                collection.insert_one(data_produk)
                st.success(f"✅ Aksesoris baru '{nama_produk}' berhasil ditambahkan!")
        else:
            st.error("❌ Mohon isi semua data dengan benar!")
