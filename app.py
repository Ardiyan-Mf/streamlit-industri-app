import streamlit as st
import numpy as np
import pandas as pd
from scipy.optimize import linprog
import matplotlib.pyplot as plt
import math

st.set_page_config(page_title="Model Industri Cerdas", layout="wide")

st.markdown("""
# 🤖 Aplikasi Model Matematika Industri
Selamat datang di aplikasi interaktif untuk mempelajari dan menerapkan model matematika dalam konteks industri.
""")

st.sidebar.image("https://img.icons8.com/fluency/96/robot.png", width=80)
st.sidebar.markdown("""
## 🧭 Navigasi Menu
Silakan pilih salah satu model:
""")
menu = st.sidebar.radio("Model yang ingin dipelajari", [
    "📈 Optimasi Produksi",
    "📦 Model EOQ",
    "⏳ Model Antrian (M/M/1)",
    "🌱 Pertumbuhan Eksponensial"
])

# 1. Optimasi Produksi
if menu == "📈 Optimasi Produksi":
    st.markdown("## 📈 Optimasi Produksi - Linear Programming")
    st.info("Studi kasus: PT Sinar Terang memproduksi Blender (A) dan Pemanggang Roti (B)")

    col1, col2 = st.columns(2)
    with col1:
        profit_a = st.number_input("💰 Profit/unit Blender (A)", value=40000)
        waktu_a = st.number_input("⏱ Waktu Mesin untuk A (jam)", value=2)
    with col2:
        profit_b = st.number_input("💰 Profit/unit Roti (B)", value=60000)
        waktu_b = st.number_input("⏱ Waktu Mesin untuk B (jam)", value=3)

    waktu_total = st.slider("🔧 Total Waktu Mesin Tersedia (jam/minggu)", 10, 200, 100)

    if st.button("🔍 Hitung Optimasi"):
        res = linprog(c=[-profit_a, -profit_b], A_ub=[[waktu_a, waktu_b]], b_ub=[waktu_total], bounds=[(0, None), (0, None)], method='highs')
        if res.success:
            x, y = res.x
            st.success(f"🔹 Produksi Blender (A): {x:.0f} unit")
            st.success(f"🔹 Produksi Roti (B): {y:.0f} unit")
            st.info(f"💸 Keuntungan Maksimal: Rp {int(-res.fun):,}")
            fig, ax = plt.subplots()
            ax.bar(['Blender A', 'Roti B'], [x, y], color=['skyblue', 'lightgreen'])
            ax.set_title("Hasil Produksi Optimal")
            st.pyplot(fig)
        else:
            st.error("Model tidak dapat diselesaikan.")

# 2. EOQ
elif menu == "📦 Model EOQ":
    st.markdown("## 📦 Economic Order Quantity (EOQ)")
    st.info("Model EOQ digunakan untuk menentukan jumlah pesanan optimal.")

    col1, col2 = st.columns(2)
    with col1:
        D = st.number_input("📦 Permintaan Tahunan (unit)", value=10000)
        S = st.number_input("🚚 Biaya Pemesanan per Order (Rp)", value=50000)
    with col2:
        H = st.number_input("🏢 Biaya Penyimpanan/unit/tahun (Rp)", value=2000)

    if st.button("🔍 Hitung EOQ"):
        EOQ = math.sqrt((2 * D * S) / H)
        st.success(f"🔹 EOQ: {EOQ:.2f} unit per pemesanan")
        Q_range = np.arange(100, 2*int(EOQ)+500, 100)
        TC = (D / Q_range) * S + (Q_range / 2) * H

        fig, ax = plt.subplots()
        ax.plot(Q_range, TC, marker='o')
        ax.axvline(EOQ, color='red', linestyle='--', label=f'EOQ: {EOQ:.0f}')
        ax.set_title("Total Cost vs Order Quantity")
        ax.set_xlabel("Order Quantity")
        ax.set_ylabel("Total Cost")
        ax.legend()
        st.pyplot(fig)

# 3. Antrian M/M/1
elif menu == "⏳ Model Antrian (M/M/1)":
    st.markdown("## ⏳ Model Antrian M/M/1")
    st.info("Analisis sistem pelayanan dengan 1 server.")

    col1, col2 = st.columns(2)
    with col1:
        lam = st.number_input("📥 Tingkat Kedatangan (λ)", value=10.0)
    with col2:
        mu = st.number_input("📤 Tingkat Layanan (μ)", value=12.0)

    if st.button("🔍 Hitung Model Antrian"):
        if lam < mu:
            rho = lam / mu
            L = rho / (1 - rho)
            W = 1 / (mu - lam)
            Wq = lam / (mu * (mu - lam))
            st.success(f"🔹 Utilisasi Sistem: {rho:.2%}")
            st.info(f"📊 Pelanggan rata-rata dalam sistem: {L:.2f}")
            st.info(f"⏱ Waktu dalam sistem: {W:.2f} jam")
            fig, ax = plt.subplots()
            ax.bar(['Pelanggan (L)', 'Waktu (W)'], [L, W], color=['coral', 'lightblue'])
            ax.set_title("Visualisasi Antrian")
            st.pyplot(fig)
        else:
            st.error("μ harus lebih besar dari λ agar sistem stabil")

# 4. Pertumbuhan Eksponensial
elif menu == "🌱 Pertumbuhan Eksponensial":
    st.markdown("## 🌱 Model Pertumbuhan Eksponensial")
    st.info("Model ini digunakan untuk memodelkan pertumbuhan populasi, investasi, dll.")

    P0 = st.number_input("📈 Nilai awal (P₀)", value=1000)
    r = st.number_input("📈 Laju pertumbuhan (r)", value=0.1)
    t = st.slider("🕒 Periode waktu (tahun)", 1, 50, 10)

    P = P0 * np.exp(r * t)
    st.success(f"📊 Hasil setelah {t} tahun: {P:,.2f}")

    t_vals = np.linspace(0, 50, 100)
    P_vals = P0 * np.exp(r * t_vals)
    fig, ax = plt.subplots()
    ax.plot(t_vals, P_vals, color='green')
    ax.set_title("Kurva Pertumbuhan Eksponensial")
    ax.set_xlabel("Tahun")
    ax.set_ylabel("Jumlah")
    st.pyplot(fig)
