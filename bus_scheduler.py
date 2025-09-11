import streamlit as st
import random
import numpy as np

# Hàm chi phí (tổng thời gian chạy + số chuyến)
def cost(schedule):
    total_time = sum(schedule)
    overload_penalty = abs(len(schedule) - st.session_state["num_buses"]) * 10
    return total_time + overload_penalty

# Sinh lời giải lân cận
def neighbor(schedule):
    new_schedule = schedule[:]
    i = random.randint(0, len(schedule) - 1)
    new_schedule[i] += random.choice([-5, 5])
    new_schedule[i] = max(5, new_schedule[i])  # thời gian tối thiểu 5 phút
    return new_schedule

# Thuật toán Simulated Annealing
def simulated_annealing(num_buses, num_routes, iterations, temp):
    # Khởi tạo lịch ngẫu nhiên
    schedule = [random.randint(10, 50) for _ in range(num_buses)]
    best = schedule[:]
    best_cost = cost(best)

    for _ in range(iterations):
        new_schedule = neighbor(schedule)
        c_old, c_new = cost(schedule), cost(new_schedule)

        if c_new < c_old or random.random() < np.exp((c_old - c_new) / temp):
            schedule = new_schedule[:]

        if cost(schedule) < best_cost:
            best = schedule[:]
            best_cost = cost(best)

        temp *= 0.99  # giảm nhiệt độ dần

    return best, best_cost


# ================= STREAMLIT UI =================
st.title("🚌 Tối ưu Lịch Xe Buýt bằng Thuật toán Tôi thép (SA)")

st.sidebar.header("⚙️ Tuỳ chọn")
num_buses = st.sidebar.number_input("Số xe buýt", 1, 20, 5)
num_routes = st.sidebar.number_input("Số tuyến đường", 1, 10, 3)
iterations = st.sidebar.slider("Số lần lặp", 100, 5000, 1000, 100)
temperature = st.sidebar.slider("Nhiệt độ ban đầu", 10, 500, 100, 10)

if "num_buses" not in st.session_state:
    st.session_state["num_buses"] = num_buses

if st.button("🚀 Chạy tối ưu"):
    best_schedule, best_cost = simulated_annealing(num_buses, num_routes, iterations, temperature)
    st.success("Lịch chạy xe buýt tối ưu tìm được:")
    for i, t in enumerate(best_schedule, 1):
        st.write(f"Xe {i}: {t} phút/chuyến")
    st.write(f"👉 Tổng chi phí = {best_cost}")
