import streamlit as st
import random
import math

# ===============================
# 1. Hàm tính chi phí lộ trình
# ===============================
def tinh_chi_phi(lo_trinh, khoang_cach):
    tong = 0
    for i in range(len(lo_trinh) - 1):
        a = lo_trinh[i]
        b = lo_trinh[i + 1]
        tong += khoang_cach[a][b]
    return tong

# ===============================
# 2. Tạo lộ trình ban đầu + lân cận
# ===============================
def tao_lo_trinh(so_diem):
    lo_trinh = list(range(so_diem))
    random.shuffle(lo_trinh)
    return lo_trinh

def lo_trinh_lan_can(lo_trinh):
    a, b = random.sample(range(len(lo_trinh)), 2)
    lo_trinh_moi = lo_trinh[:]
    lo_trinh_moi[a], lo_trinh_moi[b] = lo_trinh_moi[b], lo_trinh_moi[a]
    return lo_trinh_moi

# ===============================
# 3. Thuật toán Simulated Annealing
# ===============================
def toi_thep(khoang_cach, nhiet_do=1000, giam_nhiet=0.95, vonglap=1000):
    lo_trinh_ht = tao_lo_trinh(len(khoang_cach))
    chi_phi_ht = tinh_chi_phi(lo_trinh_ht, khoang_cach)

    lo_trinh_best = lo_trinh_ht[:]
    chi_phi_best = chi_phi_ht

    for _ in range(vonglap):
        lo_trinh_moi = lo_trinh_lan_can(lo_trinh_ht)
        chi_phi_moi = tinh_chi_phi(lo_trinh_moi, khoang_cach)

        if chi_phi_moi < chi_phi_ht:
            lo_trinh_ht, chi_phi_ht = lo_trinh_moi, chi_phi_moi
        else:
            xac_suat = math.exp(-(chi_phi_moi - chi_phi_ht) / nhiet_do)
            if random.random() < xac_suat:
                lo_trinh_ht, chi_phi_ht = lo_trinh_moi, chi_phi_moi

        if chi_phi_ht < chi_phi_best:
            lo_trinh_best, chi_phi_best = lo_trinh_ht[:], chi_phi_ht

        nhiet_do *= giam_nhiet

    return lo_trinh_best, chi_phi_best

# ===============================
# 4. Giao diện Streamlit
# ===============================
st.title("🚍 Mô phỏng tối ưu lịch trình xe buýt (Simulated Annealing)")

# Người dùng chọn số điểm dừng
so_diem = st.slider("Chọn số điểm dừng:", 3, 8, 5)

# Tạo ma trận khoảng cách ngẫu nhiên
random.seed(42)
khoang_cach = [[0 if i == j else random.randint(10, 40) for j in range(so_diem)] for i in range(so_diem)]

st.subheader("📌 Ma trận khoảng cách giữa các điểm dừng")
st.table(khoang_cach)

if st.button("▶️ Chạy tối ưu"):
    lo_trinh, chiphi = toi_thep(khoang_cach)

    st.subheader("✅ Kết quả tìm được")
    st.write("🔹 Lộ trình tối ưu:", lo_trinh)
    st.write("🔹 Tổng thời gian di chuyển:", f"{chiphi} phút")
