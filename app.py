from dotenv import load_dotenv
load_dotenv()
import base64
import streamlit as st
import os
import io
import fitz  # PyMuPDF for PDF processing
import google.generativeai as genai

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get response from Gemini
def get_gemini_response(input, pdf_content, prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([input, pdf_content[0], prompt])
        return response.text
    except Exception as e:
        st.error(f"Error with Gemini API: {e}")
        return None

# Function to process the uploaded PDF and extract the first page as an image
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        pdf_document = fitz.open("pdf", uploaded_file.read())
        first_page = pdf_document[0]
        # Convert page to image
        pix = first_page.get_pixmap()
        img_byte_arr = io.BytesIO(pix.tobytes("jpeg"))
        
        # Encode image in base64
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr.getvalue()).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit App UI
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")

# Text input and file upload
input_text = st.text_area("Job Description:", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")
submit3 = st.button("Percentage Match")

input_prompt1 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
Your task is to evaluate the resume against the provided job description. Provide the percentage match if the resume matches
the job description. First, output the match percentage, then list missing keywords, and finally give your final thoughts.
"""

# Execute actions based on the button clicked
if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        if response:
            st.subheader("The Response is")
            st.write(response)
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        if response:
            st.subheader("The Response is")
            st.write(response)
    else:
        st.write("Please upload the resume")
