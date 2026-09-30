import streamlit as st
import pandas as pd

# Cấu hình trang ứng dụng
st.set_page_config(
    page_title="Công cụ tính Lãi suất Tiết kiệm",
    page_icon="💰",
    layout="centered"
)

st.title("💰 Ứng dụng Tính Lãi Gửi Tiết Kiệm")
st.write("Nhập các thông tin dưới đây để tính toán số tiền lãi nhận được.")

# Chia bố cục giao diện thành 2 cột nhập liệu
col1, col2 = st.columns(2)

with col1:
    so_tien_goc = st.number_input(
        "Số tiền gửi ban đầu (VNĐ):", 
        min_value=0, 
        value=100000000, 
        step=1000000,
        format="%d"
    )
    
    ky_han_thang = st.number_input(
        "Kỳ hạn gửi (tháng):", 
        min_value=1, 
        value=12, 
        step=1
    )

with col2:
    lai_suat_nam = st.number_input(
        "Lãi suất gửi (% / năm):", 
        min_value=0.0, 
        value=6.0, 
        step=0.1,
        format="%.1f"
    )
    
    hinh_thuc = st.selectbox(
        "Hình thức nhận lãi:",
        options=["Lãnh lãi theo tháng", "Lãnh lãi theo quý", "Lãnh lãi cuối kỳ"]
    )

# Quy đổi số kỳ nhận lãi dựa trên hình thức và kỳ hạn
# 1 quý = 3 tháng
so_thang_moi_ky = 1
if hinh_thuc == "Lãnh lãi theo quý":
    so_thang_moi_ky = 3
elif hinh_thuc == "Lãnh lãi cuối kỳ":
    so_thang_moi_ky = ky_han_thang

# Tổng số lần nhận lãi (số kỳ)
tong_so_ky = ky_han_thang / so_thang_moi_ky

# Kiểm tra tính hợp lệ của kỳ hạn so với hình thức nhận lãi
if ky_han_thang % so_thang_moi_ky != 0:
    st.warning(f"⚠️ Kỳ hạn {ky_han_thang} tháng không chia hết cho hình thức nhận '{hinh_thuc}'. Kết quả dưới đây được tính toán dựa trên số kỳ lẻ thực tế ({tong_so_ky:.2f} kỳ).")

# Tính lãi suất của một kỳ nhận lãi (Lãi suất năm / 12 tháng * số tháng của kỳ)
lai_suat_ky = (lai_suat_nam / 100) / 12 * so_thang_moi_ky

# --- THỰC HIỆN TÍNH TOÁN ---

# 1. LÃI ĐƠN (Tiền lãi mỗi kỳ cố định dựa trên gốc ban đầu)
lai_dinh_ky_don = so_tien_goc * lai_suat_ky
tong_lai_don = lai_dinh_ky_don * tong_so_ky
tong_goc_lai_don = so_tien_goc + tong_lai_don

# 2. LÃI KÉP (Tiền lãi cộng dồn vào gốc sau mỗi kỳ)
tong_goc_lai_kep = so_tien_goc * ((1 + lai_suat_ky) ** tong_so_ky)
tong_lai_kep = tong_goc_lai_kep - so_tien_goc
# Đối với lãi kép, số tiền nhận định kỳ sẽ tăng dần, hiển thị trung bình hoặc tính theo kỳ đầu
lai_dinh_ky_kep_dau = so_tien_goc * lai_suat_ky 


# --- HIỂN THỊ KẾT QUẢ ---
st.markdown("---")
st.subheader("📊 Kết quả dự toán lãi suất")

# Tạo 2 tabs tương ứng với Lãi đơn và Lãi kép để người dùng dễ so sánh
tab1, tab2 = st.tabs(["🔹 Lãi Đơn (Rút lãi định kỳ)", "🔸 Lãi Kép (Lãi nhập gốc)"])

with tab1:
    st.markdown("### Phương thức Lãi Đơn")
    st.caption("Áp dụng khi bạn rút tiền lãi ra chi tiêu sau mỗi kỳ nhận lãi, tiền gốc giữ nguyên.")
    
    c1, c2, c3 = st.columns(3)
    c1.metric(
        label=f"Tiền lãi định kỳ ({hinh_thuc.split()[-1]})", 
        value=f"{int(lai_dinh_ky_don):,} VNĐ" if hinh_thuc != "Lãnh lãi cuối kỳ" else "Nhận cuối kỳ"
    )
    c2.metric(label="Tổng tiền lãi", value=f"{int(tong_lai_don):,} VNĐ")
    c3.metric(label="Tổng gốc + lãi nhận được", value=f"{int(tong_goc_lai_don):,} VNĐ")

with tab2:
    st.markdown("### Phương thức Lãi Kép")
    st.caption("Áp dụng khi bạn không rút lãi, tiền lãi tự động cộng dồn vào gốc để tính lãi cho kỳ tiếp theo.")
    
    c1, c2, c3 = st.columns(3)
    if hinh_thuc == "Lãnh lãi cuối kỳ":
        c1.metric(label="Tiền lãi nhận được", value=f"{int(tong_lai_kep):,} VNĐ")
    else:
        c1.metric(label="Tiền lãi kỳ đầu tiên", value=f"{int(lai_dinh_ky_kep_dau):,} VNĐ")
        
    c2.metric(label="Tổng tiền lãi tích lũy", value=f"{int(tong_lai_kep):,} VNĐ")
    c3.metric(label="Tổng gốc + lãi nhận được", value=f"{int(tong_goc_lai_kep):,} VNĐ")

# Lưu ý nhỏ về quy định ngân hàng thực tế
st.markdown("---")
st.info("💡 *Lưu ý: Công thức trên dựa trên toán học lý thuyết chuẩn. Thực tế tại các Ngân hàng thương mại, tiền lãi có thể chênh lệch vài đồng tùy thuộc vào số ngày thực tế trong tháng/năm (365 hoặc 360 ngày) và quy định làm tròn của từng ngân hàng.*")
