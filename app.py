import os
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai
import streamlit as st
from PIL import Image

google_api_key=os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=google_api_key)
model=genai.GenerativeModel("gemini-1.5-flash-exp-0827")




def get_response(input_prompt,image):
    response=model.generate_content([input_prompt,image[0]])
    return response.text

def input_image_processing(uploaded_file):
    if (uploaded_file is not None):
        bytes_data=uploaded_file.getvalue()
        image_parts=[
            {
                "mime_type":uploaded_file.type,
                "data":bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("Please Upload an image")

st.set_page_config(page_title="Find what you eat ?")
st.header("Find what you eat ?")

uploaded_file=st.file_uploader("Click to Upload the Image",type=['jpg','jpeg','png'])

image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image=image,caption="Uploaded Image:",use_column_width=False,width=300)

submit=st.button("Press me to know about your food")

input_prompt="""
You are a highly experienced nutritionist.
 Analyze the food items in the provided image and perform the following tasks:

Identify each food item and calculate its calorie content.
Present the details in the format below:
Item 1 - X calories
Item 2 - Y calories
(Continue in this format for all items)
Provide a concise evaluation of whether the overall meal is healthy or not.
Calculate and display the calorie breakdown by key nutrients (carbohydrates, fats, fibers, sugars, etc.).
Recommend additional food items that would improve the nutritional balance to maintain a healthy diet.
"""

if submit:
    image_data=input_image_processing(uploaded_file=uploaded_file)
    response=get_response(input_prompt=input_prompt,image=image_data)
    st.write("The response is")
    st.write(response)







