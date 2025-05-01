import streamlit as st
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import io

# Tiêu đề
st.title("📸 Ứng dụng chỉnh sửa ảnh")

# Tải ảnh lên
uploaded_file = st.file_uploader("Tải ảnh lên", type=["jpg", "jpeg", "png"])

# Biến lưu ảnh đã chỉnh sửa
if "edited_image" not in st.session_state:
    st.session_state.edited_image = None

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    if st.session_state.edited_image is None:
        st.session_state.edited_image = image.copy()

    st.image(st.session_state.edited_image, caption="Ảnh hiện tại", use_column_width=True)

    # Các chức năng chỉnh sửa
    st.subheader("🛠️ Chỉnh sửa ảnh")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Chuyển trắng đen"):
            st.session_state.edited_image = st.session_state.edited_image.convert("L").convert("RGB")

        if st.button("Làm mờ"):
            st.session_state.edited_image = st.session_state.edited_image.filter(ImageFilter.GaussianBlur(2))

        if st.button("Lật ngang"):
            st.session_state.edited_image = st.session_state.edited_image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

        if st.button("Tăng sáng"):
            enhancer = ImageEnhance.Brightness(st.session_state.edited_image)
            st.session_state.edited_image = enhancer.enhance(1.5)

        if st.button("Tách kênh màu R"):
            r, g, b = st.session_state.edited_image.split()
            zero = Image.new("L", r.size)
            st.session_state.edited_image = Image.merge("RGB", (r, zero, zero))

    with col2:
        if st.button("Bộ lọc Vintage"):
            gray = st.session_state.edited_image.convert("L")
            st.session_state.edited_image = ImageOps.colorize(gray, "#704214", "#C0C0C0")

        if st.button("Làm nét"):
            st.session_state.edited_image = st.session_state.edited_image.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))

        if st.button("Lật dọc"):
            st.session_state.edited_image = st.session_state.edited_image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

        if st.button("Tăng tương phản"):
            enhancer = ImageEnhance.Contrast(st.session_state.edited_image)
            st.session_state.edited_image = enhancer.enhance(1.5)

        if st.button("Tách kênh màu G"):
            r, g, b = st.session_state.edited_image.split()
            zero = Image.new("L", g.size)
            st.session_state.edited_image = Image.merge("RGB", (zero, g, zero))

    with col3:
        if st.button("Bộ lọc lạnh"):
            st.session_state.edited_image = ImageEnhance.Color(st.session_state.edited_image).enhance(0.5)

        if st.button("Bộ lọc ấm"):
            st.session_state.edited_image = ImageEnhance.Color(st.session_state.edited_image).enhance(1.5)

        if st.button("Xoay ảnh 90°"):
            st.session_state.edited_image = st.session_state.edited_image.rotate(90, expand=True)

        if st.button("Cắt ảnh (giữa)"):
            w, h = st.session_state.edited_image.size
            st.session_state.edited_image = st.session_state.edited_image.crop((w//4, h//4, 3*w//4, 3*h//4))

        if st.button("Tách kênh màu B"):
            r, g, b = st.session_state.edited_image.split()
            zero = Image.new("L", b.size)
            st.session_state.edited_image = Image.merge("RGB", (zero, zero, b))

    # Hiển thị ảnh đã chỉnh sửa
    st.subheader("📷 Ảnh sau chỉnh sửa")
    st.image(st.session_state.edited_image, use_column_width=True)

    # Tải ảnh xuống
    st.subheader("💾 Tải ảnh xuống")
    img_bytes = io.BytesIO()
    st.session_state.edited_image.save(img_bytes, format="PNG")
    st.download_button("Tải ảnh PNG", data=img_bytes.getvalue(), file_name="edited_image.png", mime="image/png")

    # Nút hoàn tác
    if st.button("🔄 Đặt lại ảnh gốc"):
        st.session_state.edited_image = image.copy()