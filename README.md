# README.md untuk Aplikasi Streamlit Industri

## 📌 Deskripsi
Aplikasi ini dibuat untuk mata kuliah **Matematika Terapan** dengan tujuan mensimulasikan berbagai model matematika yang digunakan dalam industri.

Aplikasi dibuat menggunakan **Python** dan **Streamlit**, serta terdiri dari 4 menu utama yang interaktif.

## 📂 Menu Utama
1. **Optimasi Produksi (Linear Programming)**
   - Studi kasus: Produksi blender dan pemanggang roti
   - Dilengkapi grafik batang hasil produksi optimal

2. **Model Persediaan (EOQ)**
   - Studi kasus: Bengkel memesan oli
   - Dilengkapi grafik biaya total terhadap kuantitas pesanan

3. **Model Antrian (M/M/1)**
   - Studi kasus: Loket layanan pelanggan
   - Dilengkapi grafik batang pelanggan dan waktu tunggu

4. **Model Pertumbuhan Eksponensial**
   - Digunakan untuk simulasi pertumbuhan populasi/investasi
   - Interaktif dengan slider waktu dan input tingkat pertumbuhan

## 🚀 Cara Menjalankan Aplikasi

### 🔹 Lokal (di komputer sendiri)
```bash
pip install -r requirements.txt
streamlit run app.py
```

### 🔹 Online (Streamlit Cloud)
1. Deploy ke: [https://streamlit.io/cloud](https://streamlit.io/cloud)
2. Pastikan file `app.py` dan `requirements.txt` sudah ada di repo GitHub
3. Klik **New app** → Pilih repo → Isi `main file path: app.py` → Deploy

## 🧾 requirements.txt
```txt
streamlit
numpy
pandas
scipy
matplotlib
```

## 🧠 Refleksi
Model matematika mampu:
- Meningkatkan efisiensi produksi
- Mengoptimalkan inventori
- Meminimalkan waktu tunggu
- Menyediakan simulasi tanpa eksperimen fisik

---

> Dibuat oleh: **Ardiyan-Mf**  
> Untuk: Matematika Terapan - Pertemuan 13
