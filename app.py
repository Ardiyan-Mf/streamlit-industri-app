import streamlit as st
import numpy as np
import pandas as pd
from scipy.optimize import linprog
import matplotlib.pyplot as plt
import math
import seaborn as sns

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
