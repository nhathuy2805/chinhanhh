import streamlit as st
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import io

# Khởi tạo session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'current_image' not in st.session_state:
    st.session_state.current_image = None

st.title("🖼️ Ứng dụng chỉnh sửa ảnh")

# Upload ảnh
uploaded_file = st.file_uploader("📤 Tải ảnh lên", type=['jpg', 'jpeg', 'png'])
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.session_state.history = [image.copy()]
    st.session_state.current_image = image.copy()

# Hiển thị ảnh hiện tại
if st.session_state.current_image:
    st.image(st.session_state.current_image, caption="Ảnh hiện tại", use_column_width=True)

    st.subheader("✨ Chức năng chỉnh sửa")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔁 Lật ngang"):
            img = st.session_state.current_image.transpose(Image.FLIP_LEFT_RIGHT)
            st.session_state.history.append(img)
            st.session_state.current_image = img

        if st.button("🔄 Lật dọc"):
            img = st.session_state.current_image.transpose(Image.FLIP_TOP_BOTTOM)
            st.session_state.history.append(img)
            st.session_state.current_image = img

        if st.button("🌑 Trắng đen"):
            img = st.session_state.current_image.convert("L").convert("RGB")
            st.session_state.history.append(img)
            st.session_state.current_image = img

        if st.button("💡 Tăng sáng"):
            enhancer = ImageEnhance.Brightness(st.session_state.current_image)
            img = enhancer.enhance(1.5)
            st.session_state.history.append(img)
            st.session_state.current_image = img

    with col2:
        if st.button("📐 Xoay 90°"):
            img = st.session_state.current_image.rotate(90, expand=True)
            st.session_state.history.append(img)
            st.session_state.current_image = img

        if st.button("🔲 Cắt ảnh"):
            w, h = st.session_state.current_image.size
            img = st.session_state.current_image.crop((w//4, h//4, 3*w//4, 3*h//4))
            st.session_state.history.append(img)
            st.session_state.current_image = img

        if st.button("🎨 Vintage"):
            img = ImageOps.colorize(st.session_state.current_image.convert("L"), "#704214", "#C0C0C0")
            st.session_state.history.append(img)
            st.session_state.current_image = img

        if st.button("📸 Tăng tương phản"):
            enhancer = ImageEnhance.Contrast(st.session_state.current_image)
            img = enhancer.enhance(1.5)
            st.session_state.history.append(img)
            st.session_state.current_image = img

    with col3:
        if st.button("🔍 Làm nét"):
            img = st.session_state.current_image.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
            st.session_state.history.append(img)
            st.session_state.current_image = img

        if st.button("💧 Làm mờ"):
            img = st.session_state.current_image.filter(ImageFilter.GaussianBlur(2))
            st.session_state.history.append(img)
            st.session_state.current_image = img

        if st.button("❄️ Lạnh"):
            enhancer = ImageEnhance.Color(st.session_state.current_image)
            img = enhancer.enhance(0.5)
            st.session_state.history.append(img)
            st.session_state.current_image = img

        if st.button("🔥 Ấm"):
            enhancer = ImageEnhance.Color(st.session_state.current_image)
            img = enhancer.enhance(1.5)
            st.session_state.history.append(img)
            st.session_state.current_image = img

    # Tách kênh màu RGB
    st.subheader("🌈 Tách kênh màu RGB")
    channel = st.radio("Chọn kênh màu muốn tách:", ["Red", "Green", "Blue"])
    if st.button("Tách kênh"):
        r, g, b = st.session_state.current_image.split()
        if channel == "Red":
            img = Image.merge("RGB", (r, Image.new("L", r.size), Image.new("L", r.size)))
        elif channel == "Green":
            img = Image.merge("RGB", (Image.new("L", g.size), g, Image.new("L", g.size)))
        else:
            img = Image.merge("RGB", (Image.new("L", b.size), Image.new("L", b.size), b))
        st.session_state.history.append(img)
        st.session_state.current_image = img

    # Undo
    if st.button("↩️ Quay lại thao tác trước"):
        if len(st.session_state.history) > 1:
            st.session_state.history.pop()
            st.session_state.current_image = st.session_state.history[-1]
        else:
            st.warning("Không còn thao tác trước đó.")

    # Xem ảnh hiện tại
    if st.button("👁️ Xem ảnh hiện tại"):
        st.image(st.session_state.current_image, caption="Ảnh hiện tại", use_column_width=True)

    # Tải ảnh xuống
    img_bytes = io.BytesIO()
    st.session_state.current_image.save(img_bytes, format='PNG')
    st.download_button("📥 Tải ảnh xuống", data=img_bytes.getvalue(), file_name="edited_image.png", mime="image/png")