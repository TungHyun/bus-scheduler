import streamlit as st
import random
import numpy as np
import pandas as pd

# ===== Danh sách bến xe Hà Nội =====
ben_xe = [
    "Bến xe Giáp Bát",
    "Bến xe Nước Ngầm",
    "Bến xe Mỹ Đình",
    "Bến xe Gia Lâm",
    "Bến xe Yên Nghĩa",
    "Bến xe Sơn Tây",
    "Bến xe Trần Khát Chân",
    "Bến xe Kim Mã",
    "Bến xe Thượng Đình",
    "Bến xe Long Biên"
]

# ===== Hàm tính chi phí =====
def calculate_cost(route, distance_matrix):
    cost = 0
    for i in range(len(route) - 1):
        cost += distance_matrix[route[i]][route[i+1]]
    return cost

# ===== Thuật toán tôi thép (Simulated Annealing) =====
def simulated_annealing(distance_matrix, start, end, T=1000, alpha=0.99, stopping_T=1):
    n = len(distance_matrix)
    
    # danh sách các điểm trung gian (không gồm start, end)
    middle_nodes = [i for i in range(n) if i not in (start, end)]
    random.shuffle(middle_nodes)
    
    current_solution = [start] + middle_nodes + [end]
    current_cost = calculate_cost(current_solution, distance_matrix)
    
    best_solution = list(current_solution)
    best_cost = current_cost
    
    while T > stopping_T:
        new_solution = list(current_solution)
        # chỉ hoán đổi các điểm trung gian
        if len(middle_nodes) >= 2:
            i, j = random.sample(range(1, len(new_solution)-1), 2)
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
st.title("🚌 Tối ưu lộ trình xe buýt Hà Nội bằng Thuật toán Tôi thép")

st.subheader("📌 Bảng thời gian di chuyển giữa các bến (phút)")
n = st.number_input("Số bến xe muốn xét:", min_value=2, max_value=len(ben_xe), value=4)

# chọn tên bến tương ứng
selected_ben = ben_xe[:n]

# chọn điểm đầu & điểm cuối
start_point = st.selectbox("🚏 Chọn điểm xuất phát", selected_ben, index=0)

# danh sách điểm cuối (loại bỏ điểm đầu)
end_options = [b for b in selected_ben if b != start_point]
end_point = st.selectbox("🏁 Chọn điểm kết thúc", end_options, index=0)

# Tạo ma trận chỉ 1 lần khi số bến thay đổi
if "matrix" not in st.session_state or len(st.session_state.matrix) != n:
    st.session_state.matrix = [[0 if i == j else random.randint(10, 50) for j in range(n)] for i in range(n)]

# Nút tạo ma trận mới
if st.button("🎲 Random thời gian mới"):
    st.session_state.matrix = [[0 if i == j else random.randint(10, 50) for j in range(n)] for i in range(n)]

# Bảng editable (người dùng chỉnh trực tiếp)
df_raw = pd.DataFrame(st.session_state.matrix, columns=selected_ben, index=selected_ben)
edited_df = st.data_editor(df_raw, num_rows="fixed", key="matrix_editor")

# Cập nhật session_state bằng dữ liệu đã chỉnh sửa
st.session_state.matrix = edited_df.values.tolist()

# Chạy tối ưu
if st.button("🚀 Chạy tối ưu"):
    distance_matrix = st.session_state.matrix
    start_idx = selected_ben.index(start_point)
    end_idx = selected_ben.index(end_point)
    
    best_route, best_cost = simulated_annealing(distance_matrix, start_idx, end_idx)
    route_str = " → ".join([selected_ben[i] for i in best_route])
    
    st.success("✅ Kết quả tìm được:")
    st.write(f"**Lộ trình tối ưu:** {route_str}")
    st.write(f"**Tổng thời gian:** {best_cost} phút")
