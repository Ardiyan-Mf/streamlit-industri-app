import streamlit as st
import numpy as np
import pandas as pd
from scipy.optimize import linprog
import matplotlib.pyplot as plt
import math
import seaborn as sns

# Atur tema dan judul
st.set_page_config(page_title="Model Industri Cerdas", layout="wide")

# Sidebar
st.sidebar.markdown("## 🔍 Pilih Model")
menu = st.sidebar.radio("Menu", [
    "📈 Optimasi Produksi",
    "📦 Model EOQ",
    "⏳ Model Antrian (M/M/1)",
    "🌱 Pertumbuhan Eksponensial"
])

# 1. Optimasi Produksi - Linear Programming
if menu == "📈 Optimasi Produksi":
    st.markdown("## 📈 Optimasi Produksi - Linear Programming")
    st.markdown("""
    **Studi Kasus:**
    PT Sinar Terang memproduksi dua produk unggulan: Blender (A) dan Pemanggang Roti (B). 
    Masing-masing produk memerlukan waktu mesin untuk proses produksinya, yaitu 2 jam untuk Blender dan 3 jam untuk Pemanggang Roti. 
    Dalam satu minggu, perusahaan hanya memiliki 100 jam mesin yang tersedia.

    Keuntungan yang dihasilkan dari setiap unit Blender adalah Rp40.000, dan dari Pemanggang Roti adalah Rp60.000. 
    Manajemen ingin mengetahui berapa unit masing-masing produk yang sebaiknya diproduksi agar **keuntungan maksimal** tercapai, tanpa melebihi waktu mesin yang tersedia.
    """)

    col1, col2 = st.columns(2)
    with col1:
        profit_a = st.number_input("💰 Profit/unit Blender (A)", value=40000, min_value=0)
        waktu_a = st.number_input("⏱ Waktu Mesin A (jam)", value=2, min_value=0)
    with col2:
        profit_b = st.number_input("💰 Profit/unit Roti (B)", value=60000, min_value=0)
        waktu_b = st.number_input("⏱ Waktu Mesin B (jam)", value=3, min_value=0)

    waktu_total = st.slider("🛠️ Total Jam Mesin Tersedia", 10, 200, 100)

    if st.button("🔍 Hitung Optimasi"):
        res = linprog(
            c=[-profit_a, -profit_b],
            A_ub=[[waktu_a, waktu_b]],
            b_ub=[waktu_total],
            bounds=[(0, None), (0, None)],
            method='highs'
        )
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
            st.error("❌ Gagal menyelesaikan model LP.")

# 2. Model EOQ - Economic Order Quantity
elif menu == "📦 Model EOQ":
    st.markdown("## 📦 Model Persediaan - EOQ")
    st.markdown("""
    **Studi Kasus:**
    PT Sinar Terang mengelola gudang suku cadang blender dan pemanggang roti. 
    Setiap tahun, permintaan suku cadang mencapai 10.000 unit. 
    Biaya pemesanan sebesar Rp50.000 per kali pesan dan biaya penyimpanan per unit per tahun adalah Rp2.000. 

    Berapa unit yang sebaiknya dipesan agar **biaya total persediaan minimum**?
    """)

    col1, col2 = st.columns(2)
    with col1:
        D = st.number_input("📦 Permintaan Tahunan (D)", value=10000, min_value=1)
        S = st.number_input("🛒 Biaya Pemesanan (S)", value=50000, min_value=1)
    with col2:
        H = st.number_input("🏢 Biaya Penyimpanan (H)", value=2000, min_value=1)

    if st.button("🔍 Hitung EOQ"):
        EOQ = math.sqrt((2 * D * S) / H)
        st.success(f"📦 EOQ: {EOQ:.2f} unit")

        Q_range = np.arange(100, 2 * int(EOQ) + 500, 100)
        TC = (D / Q_range) * S + (Q_range / 2) * H

        fig, ax = plt.subplots()
        ax.plot(Q_range, TC, marker='o', color='#003366')
        ax.axvline(EOQ, color='red', linestyle='--', label=f'EOQ: {EOQ:.0f}')
        ax.set_title("Total Cost vs Order Quantity")
        ax.set_xlabel("Kuantitas Order")
        ax.set_ylabel("Total Cost")
        ax.legend()
        st.pyplot(fig)

        st.markdown("### 📊 Korelasi Kuantitas & Total Cost")
        df = pd.DataFrame({"Q": Q_range, "Total_Cost": TC})
        fig3, ax3 = plt.subplots()
        sns.regplot(data=df, x="Q", y="Total_Cost", ax=ax3, scatter_kws={"color": "#0055a5"}, line_kws={"color": "orange"})
        ax3.set_title("Regresi Total Cost terhadap Order Quantity")
        st.pyplot(fig3)

# 3. Model Antrian (M/M/1)
elif menu == "⏳ Model Antrian (M/M/1)":
    st.markdown("## ⏳ Model Antrian M/M/1")
    st.markdown("""
    **Studi Kasus:**
    PT Sinar Terang memiliki pusat layanan pelanggan. 
    Rata-rata terdapat 10 pelanggan datang setiap jam, dan seorang petugas mampu melayani 12 pelanggan per jam. 
    Manajemen ingin mengetahui seberapa padat sistem antrian, rata-rata jumlah pelanggan dalam sistem, serta waktu tunggu pelanggan.
    """)

    col1, col2 = st.columns(2)
    with col1:
        lam = st.number_input("📥 Tingkat Kedatangan (λ)", value=10.0, min_value=0.0)
    with col2:
        mu = st.number_input("📤 Tingkat Layanan (μ)", value=12.0, min_value=0.1)

    if st.button("🔍 Hitung Model"):
        if lam < mu:
            rho = lam / mu
            L = rho / (1 - rho)
            W = 1 / (mu - lam)
            Wq = lam / (mu * (mu - lam))

            st.success(f"📌 Utilisasi Sistem: {rho:.2%}")
            st.info(f"👥 Pelanggan dalam sistem (L): {L:.2f}")
            st.info(f"⏱️ Waktu rata-rata dalam sistem (W): {W:.2f} jam")
            st.info(f"⌛ Waktu tunggu dalam antrian (Wq): {Wq:.2f} jam")

            fig, ax = plt.subplots()
            ax.bar(['Pelanggan (L)', 'Waktu (W)', 'Antrian (Wq)'], [L, W, Wq], color=['#99ccff', '#ffcc99', '#cc9999'])
            ax.set_title("Visualisasi Antrian")
            st.pyplot(fig)
        else:
            st.error("❌ μ harus lebih besar dari λ agar sistem stabil.")

# 4. Pertumbuhan Eksponensial
elif menu == "🌱 Pertumbuhan Eksponensial":
    st.markdown("## 🌱 Pertumbuhan Eksponensial")
    st.markdown("""
    **Studi Kasus:**
    PT Sinar Terang meluncurkan produk blender pintar yang terhubung ke internet. 
    Awalnya terdapat 1.000 pengguna aktif. Diperkirakan pelanggan tumbuh dengan laju 10% per tahun.
    Berapa jumlah pengguna setelah beberapa tahun?
    """)

    P0 = st.number_input("📍 Nilai Awal (P₀)", value=1000, min_value=1)
    r = st.number_input("📈 Laju Pertumbuhan (r)", value=0.1, min_value=0.0)
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
