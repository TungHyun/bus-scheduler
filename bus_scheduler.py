import streamlit as st
import random
import numpy as np
import pandas as pd

# ===== Hàm tính chi phí =====
def calculate_cost(route, distance_matrix):
    cost = 0
    for i in range(len(route) - 1):
        cost += distance_matrix[route[i]][route[i+1]]
    return cost

# ===== Thuật toán tôi luyện =====
def simulated_annealing(distance_matrix, T=1000, alpha=0.99, stopping_T=1):
    n = len(distance_matrix)
    current_solution = list(range(n))
    random.shuffle(current_solution)
    current_cost = calculate_cost(current_solution, distance_matrix)
    
    best_solution = list(current_solution)
    best_cost = current_cost
    
    while T > stopping_T:
        new_solution = list(current_solution)
        i, j = random.sample(range(n), 2)
        new_solution[i], new_solution[j] = new_solution[j], new_solution[i]
        new_cost = calculate_cost(new_solution, distance_matrix)
        
        if new_cost < current_cost or random.random() < np.exp((current_cost - new_cost) / T):
            current_solution = new_solution
            current_cost = new_cost
            if new_cost < best_cost:
                best_solution = new_solution
                best_cost = new_cost
        T *= alpha
    
    return best_solution, best_cost

# ===== Giao diện Streamlit =====
st.title("🚌 Tối ưu lộ trình bằng Thuật toán Tôi luyện (Simulated Annealing)")

st.subheader("📌 Nhập ma trận thời gian di chuyển (phút)")
n = st.number_input("Số điểm dừng:", min_value=2, max_value=10, value=3)

# Tạo bảng mặc định
default_matrix = [[0 if i == j else random.randint(5, 30) for j in range(n)] for i in range(n)]
columns = [f"Điểm {j+1}" for j in range(n)]
index = [f"Điểm {i+1}" for i in range(n)]
df = pd.DataFrame(default_matrix, columns=columns, index=index)

# Cho phép chỉnh sửa bảng
edited_df = st.data_editor(df, num_rows="dynamic", key="matrix_input")
distance_matrix = edited_df.values.tolist()

if st.button("🚀 Chạy tối ưu"):
    best_route, best_cost = simulated_annealing(distance_matrix)
    # Đổi số thành "Điểm i"
    route_str = " → ".join([f"Điểm {i+1}" for i in best_route])
    
    st.success("✅ Kết quả tìm được:")
    st.write(f"**Lộ trình tối ưu:** {route_str}")
    st.write(f"**Tổng thời gian:** {best_cost} phút")
