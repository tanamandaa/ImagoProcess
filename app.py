import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.title("ImagoProcess: Point Operations & Filters")
st.sidebar.title("Informasi Mahasiswa")
st.sidebar.info("Oleh: Intan Amanda")

uploaded_file = st.file_uploader("Upload Foto", type=['jpg', 'png', 'jpeg'])

if uploaded_file:
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

    option = st.selectbox("Pilih Operasi", 
                          ["Original", "Brightness", "Gamma Correction", "Blurring", "Sharpening"])

    if option == "Brightness":
        beta = st.slider("Brightness Value", 0, 100, 30)
        result = cv2.convertScaleAbs(img_cv, alpha=1.0, beta=beta)
    
    elif option == "Gamma Correction":
        gamma = st.slider("Gamma", 0.1, 3.0, 1.0)
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
        result = cv2.LUT(img_cv, table)
    
    elif option == "Blurring":
        k_size = st.slider("Kernel Size", 3, 15, 5, step=2)
        result = cv2.blur(img_cv, (k_size, k_size))
        
    elif option == "Sharpening":
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        result = cv2.filter2D(img_cv, -1, kernel)
    
    else:
        result = img_cv

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Gambar Asli")
        st.image(image, use_container_width=True)
    
    with col2:
        st.subheader(f"Hasil {option}")
        result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
        st.image(result_rgb, use_container_width=True)