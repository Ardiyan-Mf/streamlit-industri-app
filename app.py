import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("📊 Aplikasi Matematika Industri")

menu = st.sidebar.radio("Pilih Menu", [
    "Optimasi Produksi",
    "Model Persediaan",
    "Model Antrian",
    "Prediksi Permintaan"
])

if menu == "Optimasi Produksi":
    st.header("Optimasi Produksi (Linear Programming)")
    st.write("Contoh sederhana optimasi produksi dua produk...")

if menu == "Model Persediaan":
    st.header("Model EOQ (Economic Order Quantity)")
    D = st.number_input("Permintaan tahunan (unit)", value=1000)
    S = st.number_input("Biaya pemesanan per pesanan", value=100)
    H = st.number_input("Biaya penyimpanan per unit per tahun", value=5)
    if st.button("Hitung EOQ"):
        EOQ = np.sqrt((2 * D * S) / H)
        st.success(f"EOQ: {EOQ:.2f} unit")

if menu == "Model Antrian":
    st.header("Model Antrian (M/M/1)")
    lam = st.number_input("Tingkat kedatangan (λ)", value=2.0)
    mu = st.number_input("Tingkat layanan (μ)", value=3.0)
    if st.button("Hitung Model"):
        if lam < mu:
            rho = lam / mu
            L = rho / (1 - rho)
            st.success(f"Rata-rata pelanggan dalam sistem: {L:.2f}")
        else:
            st.error("μ harus lebih besar dari λ")

if menu == "Prediksi Permintaan":
    st.header("Prediksi Permintaan")
