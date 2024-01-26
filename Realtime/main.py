import cv2
import streamlit as st

st.title("Final Year project ")
run = st.checkbox('Run')
FRAME_WINDOW = st.image([])
camera = cv2.VideoCapture(0)

while run:
    #st.info["YES"]
    from fall_detection import falldetection
    falldetection()
else:
    st.write('Stopped')