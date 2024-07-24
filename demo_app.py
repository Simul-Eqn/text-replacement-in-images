import streamlit as st 
from PIL import Image, ImageChops 

import image_text_replacer 

st.header("Upload your image here to test the text replacer!")

init_session_state_values = {
    'ress': None, 
    'image': None, 
    'show_bg': True, 
    'black_text': True, 
    'i': 0, 
    'detection_model_name': 'OpenCV EAST', 
}
for k, v in init_session_state_values.items(): 
    if k not in st.session_state: 
        st.session_state[k] = v 
        
st.session_state['detection_model_name'] = st.selectbox('Model used:', ['OpenCV EAST', 'Vision API'])

image_uploader = st.file_uploader("", type=["jpg","png","jpeg","webp"])
if image_uploader is not None:
    image = Image.open(image_uploader)
    if (not st.session_state['image']) or (not (ImageChops.difference(st.session_state['image'], image)) ): # if it's a new images 
        ress = image_text_replacer.get_texts_bboxes_dirns(image, get_with=st.session_state['detection_model_name']) 
        st.session_state['image'] = image 
        st.session_state['ress'] = ress 
    else: 
        ress = st.session_state['ress'] 

    st.image(image, "original image")
    

    def toggle_bg(): 
        st.session_state['show_bg'] = not st.session_state['show_bg'] 
        print(st.session_state['show_bg'])
        draw_replaced_image() 
    
    def toggle_black_text(): 
        st.session_state['black_text'] = not st.session_state['black_text'] 
        print(st.session_state['black_text'])
        draw_replaced_image() 

    #modelname = st.session_state['detection_model_name'] 
    
    #def set_detection_model(): 
    #    st.session_state['detection_model_name'] = modelname 

    def draw_replaced_image(): 
        st.session_state['i'] += 2 
        st.button('Hide background' if st.session_state['show_bg'] else 'Show background', "s/h bg"+str(st.session_state['i']), on_click=toggle_bg)
        st.button('Switch to white text' if st.session_state['black_text'] else 'Switch to black text', "b/w text"+str(st.session_state['i']), on_click=toggle_black_text)
        
        replaced_image = image_text_replacer.redraw_img(image, ress, st.session_state['show_bg'], st.session_state['black_text'])
        st.image(replaced_image, "replaced image")
    
    draw_replaced_image() 

    

    
    


