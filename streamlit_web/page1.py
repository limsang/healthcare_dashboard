import streamlit as st
from PIL import Image
st.subheader("Home")

def Home():

    # Fxn
    @st.cache
    def load_image(image_file):
        img = Image.open(image_file)
        return img

    image_file = st.file_uploader("Upload Image",type=['png','jpeg','jpg'])
    if image_file is not None:

        # To See Details
        # st.write(type(image_file))
        # st.write(dir(image_file))
        file_details = {"Filename":image_file.name,"FileType":image_file.type,"FileSize":image_file.size}
        st.write(file_details)

        img = load_image(image_file)
        st.image(img,width=250,height=250)