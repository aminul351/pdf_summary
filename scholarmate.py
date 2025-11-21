import streamlit as st
import tempfile
import os
# from dotenv import load_dotenv
import google.generativeai as genai
from PyPDF2 import PdfReader

# load_dotenv()

# Load API key
genai.configure(api_key=os.environ[GEMINI_API_KEY])

# Use FREE MODEL
model = genai.GenerativeModel("gemini-pro-latest")

def summarize_text(text):
    response = model.generate_content(
        f"Summarize the following text:\n\n{text}"
    )
    return response.text

def summarize_pdf(file):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(file.read())
        tmp_path = tmp.name

    reader = PdfReader(tmp_path)
    full_text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            full_text += page_text + "\n\n"

    os.remove(tmp_path)
    return summarize_text(full_text)

st.title("Multiple PDF Summarizer (Gemini Free API)")

uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)

if uploaded_files:
    if st.button("Generate Summary"):
        st.write("Summaries:\n")
        for i, pdf in enumerate(uploaded_files):
            st.subheader(f"Summary for PDF {i+1}:")
            st.write(summarize_pdf(pdf))
