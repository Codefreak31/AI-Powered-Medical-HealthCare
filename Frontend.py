import base64
import requests
import streamlit as st

def set_background(image_path):
    with open(image_path, "rb") as img_file:
        bin_str = base64.b64encode(img_file.read()).decode()

    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/jpeg;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

def main():
    background_image_path = r'path\user\examplefile\img.jpg'
    set_background(background_image_path)

    # Use markdown to style the text
    st.markdown('<h2 style="color:black;font-size:50px;font-weight:bold">Please input your prescription</h2>', unsafe_allow_html=True)
    
    # Add file uploader
    uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        # Display uploaded image
        col1, col2 = st.columns([1, 3])
        with col1:
            pass  # This column will be empty
        with col2:
            uploaded_image_placeholder = st.empty()
            uploaded_image_placeholder.image(uploaded_file, caption='Uploaded Image', use_column_width=True)

        # Perform OCR when user clicks a button
        if st.button('Perform OCR'):
            # Send image to FastAPI backend for OCR
            files = {'image': uploaded_file}
            response = requests.post('http://127.0.0.1:8000/perform_ocr', files=files)

            # Display detected text returned by the backend
            if response.status_code == 200:
                detected_text = response.text
                detected_text_lines = detected_text.splitlines()

                # Use markdown to render the text with correct line breaks and styling
                col3, col4 = st.columns([1, 3])
                with col3:
                    pass  # This column will be empty
                with col4:
                    st.markdown(f'<p style="color:black; font-size:20px;font-weight:bold">{detected_text}</p>', unsafe_allow_html=True)
            else:
                st.error("Failed to perform OCR. Please try again.")

if __name__ == "__main__":
    main()
