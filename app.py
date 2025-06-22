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

if st.button("Hitung EOQ"):
    EOQ = np.sqrt((2 * D * S) / H)
    st.success(f"EOQ: {EOQ:.2f} unit")

    # Hitung biaya total untuk berbagai Q
    Q_range = np.arange(100, 2*int(EOQ)+200, 100)
    TC = (D / Q_range) * S + (Q_range / 2) * H

    # Buat grafik
    fig, ax = plt.subplots()
    ax.plot(Q_range, TC, marker='o')
    ax.axvline(EOQ, color='red', linestyle='--', label=f'EOQ: {EOQ:.0f}')
    ax.set_title('Total Cost vs Order Quantity')
    ax.set_xlabel('Order Quantity (Q)')
    ax.set_ylabel('Total Cost')
    ax.legend()
    st.pyplot(fig)


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
