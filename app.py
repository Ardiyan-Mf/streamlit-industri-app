import streamlit as st
import numpy as np
import pandas as pd
from scipy.optimize import linprog
import matplotlib.pyplot as plt
import math

# Atur tema dan judul
st.set_page_config(page_title="Model Industri Cerdas", layout="wide")
st.markdown("""
<style>
    .main {
        background-color: #f0f4f8;
        padding: 2rem;
        border-radius: 1rem;
    }
    h1, h2, h3 {
        color: #003366;
    }
    .stButton > button {
        background-color: #007BFF;
        color: white;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
# 📊 Aplikasi Matematika Industri
Selamat datang di aplikasi interaktif untuk memahami dan menerapkan **model matematika dalam industri**.
""")

st.sidebar.markdown("""
## 🔍 Pilih Model
""")

menu = st.sidebar.radio("Menu", [
    "📈 Optimasi Produksi",
    "📦 Model EOQ",
    "⏳ Model Antrian (M/M/1)",
    "🌱 Pertumbuhan Eksponensial"
])

# 1. Optimasi Produksi
if menu == "📈 Optimasi Produksi":
    st.markdown("## 📈 Optimasi Produksi - Linear Programming")
    st.info("Studi kasus: PT Sinar Terang memproduksi Blender dan Pemanggang Roti")

    col1, col2 = st.columns(2)
    with col1:
        profit_a = st.number_input("💰 Profit/unit Blender (A)", value=40000)
        waktu_a = st.number_input("⏱ Waktu Mesin A (jam)", value=2)
    with col2:
        profit_b = st.number_input("💰 Profit/unit Roti (B)", value=60000)
        waktu_b = st.number_input("⏱ Waktu Mesin B (jam)", value=3)

    waktu_total = st.slider("🛠️ Total Jam Mesin Tersedia", 10, 200, 100)

    if st.button("🔍 Hitung Optimasi"):
        res = linprog(c=[-profit_a, -profit_b], A_ub=[[waktu_a, waktu_b]], b_ub=[waktu_total], bounds=[(0, None), (0, None)], method='highs')
        if res.success:
            x, y = res.x
            st.success(f"✅ Produksi Blender A: {x:.0f} unit")
            st.success(f"✅ Produksi Roti B: {y:.0f} unit")
            st.info(f"💸 Total Keuntungan: Rp {int(-res.fun):,}")
            fig, ax = plt.subplots()
            ax.bar(['Blender A', 'Roti B'], [x, y], color=['#3399ff', '#66cc99'])
            ax.set_title("Produksi Optimal")
            st.pyplot(fig)
        else:
            st.error("Gagal menyelesaikan model LP.")

# 2. EOQ
elif menu == "📦 Model EOQ":
    st.markdown("## 📦 Model Persediaan - EOQ")
    st.info("Model EOQ digunakan untuk menentukan jumlah pemesanan optimal.")

    col1, col2 = st.columns(2)
    with col1:
        D = st.number_input("📦 Permintaan Tahunan (D)", value=10000)
        S = st.number_input("🛒 Biaya Pemesanan (S)", value=50000)
    with col2:
        H = st.number_input("🏢 Biaya Penyimpanan (H)", value=2000)

    if st.button("🔍 Hitung EOQ"):
        EOQ = math.sqrt((2 * D * S) / H)
        st.success(f"📦 EOQ: {EOQ:.2f} unit")

        Q_range = np.arange(100, 2*int(EOQ)+500, 100)
        TC = (D / Q_range) * S + (Q_range / 2) * H

        fig, ax = plt.subplots()
        ax.plot(Q_range, TC, marker='o', color='#003366')
        ax.axvline(EOQ, color='red', linestyle='--', label=f'EOQ: {EOQ:.0f}')
        ax.set_title("Total Cost vs Order Quantity")
        ax.set_xlabel("Kuantitas Order")
        ax.set_ylabel("Total Cost")
        ax.legend()
        st.pyplot(fig)

# 3. Antrian M/M/1
elif menu == "⏳ Model Antrian (M/M/1)":
    st.markdown("## ⏳ Model Antrian M/M/1")
    st.info("Digunakan untuk menganalisis sistem pelayanan satu server.")

    col1, col2 = st.columns(2)
    with col1:
        lam = st.number_input("📥 Tingkat Kedatangan (λ)", value=10.0)
    with col2:
        mu = st.number_input("📤 Tingkat Layanan (μ)", value=12.0)

    if st.button("🔍 Hitung Model"):
        if lam < mu:
            rho = lam / mu
            L = rho / (1 - rho)
            W = 1 / (mu - lam)
            Wq = lam / (mu * (mu - lam))

            st.success(f"📌 Utilisasi Sistem: {rho:.2%}")
            st.info(f"👥 Pelanggan dalam sistem: {L:.2f}")
            st.info(f"⏱️ Waktu rata-rata dalam sistem: {W:.2f} jam")

            fig, ax = plt.subplots()
            ax.bar(['Pelanggan (L)', 'Waktu (W)'], [L, W], color=['#99ccff', '#ffcc99'])
            ax.set_title("Visualisasi Antrian")
            st.pyplot(fig)
        else:
            st.error("μ harus lebih besar dari λ agar sistem stabil")

# 4. Pertumbuhan Eksponensial
elif menu == "🌱 Pertumbuhan Eksponensial":
    st.markdown("## 🌱 Pertumbuhan Eksponensial")
    st.info("Model pertumbuhan untuk populasi atau investasi")

    P0 = st.number_input("📍 Nilai Awal (P₀)", value=1000)
    r = st.number_input("📈 Laju Pertumbuhan (r)", value=0.1)
    t = st.slider("⏳ Waktu (tahun)", 1, 50, 10)

    P = P0 * np.exp(r * t)
    st.success(f"📈 Nilai pada tahun ke-{t}: {P:,.2f}")

    t_vals = np.linspace(0, 50, 100)
    P_vals = P0 * np.exp(r * t_vals)
    fig, ax = plt.subplots()
    ax.plot(t_vals, P_vals, color='#006600')
    ax.set_title("Kurva Pertumbuhan Eksponensial")
    ax.set_xlabel("Tahun")
    ax.set_ylabel("Jumlah")
    st.pyplot(fig)
