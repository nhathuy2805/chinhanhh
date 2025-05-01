import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import io

# Thiết lập tiêu đề trang
st.set_page_config(page_title="Ứng dụng chỉnh sửa ảnh", layout="centered")
st.title("🖼️ Ứng dụng chỉnh sửa ảnh")

# Biến lưu trữ lịch sử ảnh để hỗ trợ undo
if "history" not in st.session_state:
    st.session_state.history = []

# Hàm hiển thị ảnh
def display_image(img):
    st.image(img, caption="Ảnh hiện tại", use_column_width=True)

# Tải ảnh lên
uploaded_file = st.file_uploader("Tải ảnh lên", type=["jpg", "jpeg", "png"])
if uploaded_file:
    img = Image.open(uploaded_file).convert("RGB")
    st.session_state.history = [img.copy()]  # Lưu bản gốc
    display_image(img)

# Nếu đã có ảnh trong lịch sử
if st.session_state.history:
    img = st.session_state.history[-1]

    # Chức năng chỉnh sửa ảnh
    st.subheader("🔧 Các chức năng chỉnh sửa")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Trắng đen"):
            img = img.convert("L").convert("RGB")
            st.session_state.history.append(img)
        if st.button("Làm mờ"):
            img = img.filter(ImageFilter.GaussianBlur(3))
            st.session_state.history.append(img)
        if st.button("Lật ngang"):
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
            st.session_state.history.append(img)

    with col2:
        if st.button("Lật dọc"):
            img = img.transpose(Image.FLIP_TOP_BOTTOM)
            st.session_state.history.append(img)
        if st.button("Tăng sáng"):
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(1.5)
            st.session_state.history.append(img)
        if st.button("Tăng tương phản"):
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.5)
            st.session_state.history.append(img)

    with col3:
        if st.button("Làm nét"):
            img = img.filter(ImageFilter.UnsharpMask())
            st.session_state.history.append(img)
        if st.button("Xoay 90°"):
            img = img.rotate(-90, expand=True)
            st.session_state.history.append(img)
        if st.button("Cắt ảnh (trung tâm)"):
            w, h = img.size
            left = w // 4
            top = h // 4
            right = w * 3 // 4
            bottom = h * 3 // 4
            img = img.crop((left, top, right, bottom))
            st.session_state.history.append(img)

    st.markdown("---")

    # Bộ lọc màu
    st.subheader("🎨 Bộ lọc màu")

    col4, col5, col6 = st.columns(3)
    with col4:
        if st.button("Bộ lọc Vintage"):
            gray = img.convert("L")
            img = ImageOps.colorize(gray, "#704214", "#C0A080")
            st.session_state.history.append(img)
    with col5:
        if st.button("Bộ lọc lạnh"):
            r, g, b = img.split()
            b = b.point(lambda i: min(255, i + 30))
            img = Image.merge("RGB", (r, g, b))
            st.session_state.history.append(img)
    with col6:
        if st.button("Bộ lọc ấm"):
            r, g, b = img.split()
            r = r.point(lambda i: min(255, i + 30))
            img = Image.merge("RGB", (r, g, b))
            st.session_state.history.append(img)

    # Tách kênh RGB
    st.subheader("🌈 Tách kênh màu RGB")
    channel = st.radio("Chọn kênh", ["R", "G", "B"])
    if st.button("Tách kênh màu"):
        r, g, b = img.split()
        if channel == "R":
            img = Image.merge("RGB", (r, Image.new("L", r.size), Image.new("L", r.size)))
        elif channel == "G":
            img = Image.merge("RGB", (Image.new("L", g.size), g, Image.new("L", g.size)))
        else:
            img = Image.merge("RGB", (Image.new("L", b.size), Image.new("L", b.size), b))
        st.session_state.history.append(img)

    # Undo
    st.subheader("↩️ Hoàn tác")
    if st.button("Quay lại thao tác trước"):
        if len(st.session_state.history) > 1:
            st.session_state.history.pop()
            img = st.session_state.history[-1]
        else:
            st.warning("Không có thao tác trước đó để quay lại.")

    # Hiển thị ảnh sau khi chỉnh sửa
    display_image(img)

    # Tải ảnh về
    st.subheader("📥 Tải ảnh đã chỉnh sửa")
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    st.download_button(label="Tải ảnh", data=img_byte_arr.getvalue(), file_name="edited_image.png", mime="image/png")