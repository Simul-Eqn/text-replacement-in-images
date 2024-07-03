import streamlit as st 
from PIL import Image 

import image_text_replacer 

st.header("Upload your image here to test the text replacer!")

image_uploader = st.file_uploader("", type=["jpg","png","jpeg","webp"])
if image_uploader is not None:
    image = Image.open(image_uploader)
    st.image(image, "original image")
    replaced_image = image_text_replacer.replace_image(image) 
    st.image(replaced_image, "replaced image")


