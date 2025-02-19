import os
import json
import streamlit as st
import google.generativeai as genai
from PIL import Image
import easyocr
from dotenv import load_dotenv
import numpy as np

# Load the environment variable
load_dotenv()

# Initialize the Google Generative AI API Key
api_key=os.getenv("GOOGLE_API_KEY")

# Set up the Streamlit app with an icon and title
st.set_page_config(
  page_title="Python Code Reviewer", 
  layout="wide",
  page_icon="🤖")

# Inject Material UI CSS
st.markdown("""
    <link href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css" rel="stylesheet">
    <style>
        body {
            /*font-family: 'Roboto', sans-serif;*/
            background-color: #121212;
            color: white;
        }
        .stTextArea textarea {
            background-color: black !important;
            color: white !important;
            border: 1px solid white !important;
            outline: none !important;
            height: 300px !important;
            width: 100% !important;
        }
        .stTextArea textarea:focus {
            outline: 2px solid yellow !important;
            border: 1px solid yellow !important;
        }
    </style>
""", unsafe_allow_html=True)

# Configure Gemini API Key
genai.configure(api_key=api_key) 

# Initialize EasyOCR reader (with caching)
@st.cache_resource
def load_easyocr_model():
    return easyocr.Reader(['en'])  # Specify languages as needed

reader = load_easyocr_model()

def extract_code(uploaded_file):
    if uploaded_file.name.endswith(".py"):
        return uploaded_file.read().decode("utf-8")
    elif uploaded_file.name.endswith(".ipynb"):
        notebook = json.load(uploaded_file)
        code_cells = [
            cell["source"] for cell in notebook["cells"] if cell["cell_type"] == "code"
        ]
        return "\n".join(["".join(cell) for cell in code_cells])
    else:
        return None

def image_to_text(uploaded_image):
    try:
        image = Image.open(uploaded_image)
        image = np.array(image)
        result = reader.readtext(image)
        extracted_text = ""
        for (bbox, text, prob) in result:
            extracted_text += text + "\n"  # Combine text from all bounding boxes
        return extracted_text
    except Exception as e:
        st.error(f"Error during image to text conversion: {e}") # Show error in Streamlit
        return None

def review_code(user_prompt: str) -> str:
    sys_prompt = """
    You are an expert AI code reviewer integrated into a user-friendly application designed to analyze Python code submitted by users. Your role is to perform the following:
    1. ## Bug Report: Identify potential bugs, syntax errors, and logical flaws in the code.
    2. ## Fixed Code: Return fixed or optimized code snippets alongside explanations of the changes made.
    3. ## User Guidance: Ensure feedback is concise, easy to understand, and helpful for developers of varying experience levels.
    Maintain a professional tone while keeping explanations simple and accessible. Focus on accuracy, efficiency, and improving the user's understanding of best coding practices.
    ### Important Note:
    If any questions are asked that are not related to Python and coding, just refer to some Google links related to it and clarify that you will not be able to answer any other questions.
    """

    gemini = genai.GenerativeModel(
        model_name="models/gemini-2.0-flash-exp",
        system_instruction=sys_prompt
    )

    try:
        response = gemini.generate_content(user_prompt)
        return response.text
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Streamlit UI
st.header("📝 Python Code Reviewer Using Gemini AI")

# Input Options
input_type = st.radio("Choose input method:", ("Text Input", "File Upload", "Image Upload"))

code_to_review = ""
uploaded_file = None
uploaded_image = None

if input_type == "Text Input":
    code_to_review = st.text_area("Paste your Python code here:", height=200)
elif input_type == "File Upload":
    uploaded_file = st.file_uploader("Upload a `.py` or `.ipynb` file", type=["py", "ipynb"])
    if uploaded_file:
        code_to_review = extract_code(uploaded_file)
        if code_to_review is None:
            st.error("Invalid file format! Please upload a `.py` or `.ipynb` file.")
elif input_type == "Image Upload":
    uploaded_image = st.file_uploader("Upload an image containing code", type=["png", "jpg", "jpeg"])
    if uploaded_image:
        st.image(uploaded_image, caption="Uploaded Image", use_container_width=True)
        with st.spinner("Converting image to text..."):
            code_to_review = image_to_text(uploaded_image)
            if code_to_review:  # Only proceed if conversion was successful
                st.success("Code extracted successfully!")
            else:
                st.error("Code extraction failed. Please try a different image.")
                code_to_review = "" # Clear code to review if conversion fails

if st.button("Review Code"):
    if not code_to_review.strip():
        st.warning("Please provide Python code through text or file upload.")
    else:
        st.subheader("📌 Extracted Code")
        st.code(code_to_review, language="python")
        
        with st.spinner("Reviewing your code..."):
            review = review_code(code_to_review)
            st.subheader("✅ Code Review Report")
            st.write(review)
