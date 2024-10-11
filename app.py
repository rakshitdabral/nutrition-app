from dotenv import load_dotenv
from google.generativeai import upload_file

load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input , image , prompt):
    model = genai.GenerativeModel('gemini-1.5-flash-002')
    response = model.generate_content([input, image[0],prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_part = [{
            "mime_type" : uploaded_file.type,
            "data" : bytes_data
        }]
        return image_part
    else:
        raise FileNotFoundError("No File Uploaded")

input_prompts = """
    You are an expert in Nutritionist where you need to see the food items from the image and 
    calculate the total calorie , also provide the details of every food items with calorie
    intake in below format strictly and donot add any other unnecessary details 
    
    1. Item 1 - no of calorie
    2. Item 2 - no of calorie
    ----
    ----
"""

st.set_page_config(page_title="AI Nutritionist App")

st.header("AI Nutritionist App")
input = st.text_input("Input prompt" , key="input")
uploaded_file = st.file_uploader("Choose an image...." , type=["jpg", "jpeg","png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image" ,use_column_width=True)

submit = st.button("Tell me the total Calorie")

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompts,image_data, input )
    st.subheader("The response is")
    st.write(response)
