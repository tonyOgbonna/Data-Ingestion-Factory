import streamlit as st
import requests
from PyPDF2 import PdfReader
from io import BytesIO
import youtube_transcript_api

def extract_text_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = "\n\n".join([page.extract_text() for page in reader.pages])
    return text

def extract_text_txt(uploaded_file):
    text = uploaded_file.read().decode("utf-8")
    return text

def extract_text_url(url):
    response = requests.get(url)
    return response.text[:1000]  # Displaying only the first 1000 characters for demonstration

def extract_text_youtube(url):
    video_id = url.split("watch?v=")[-1]
    try:
        transcript_list = youtube_transcript_api.YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_transcript(['en'])
        text = "\n".join([t['text'] for t in transcript.fetch()])
    except Exception as e:
        text = str(e)
    return text

st.title("Text Content Extractor")

content_type = st.radio("Select Content Type", ["PDF File", "Text File", "URL", "YouTube Video Link"])

if content_type in ["PDF File", "Text File"]:
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "txt"])
    if uploaded_file is not None:
        if content_type == "PDF File":
            extracted_text = extract_text_pdf(uploaded_file)
        else:
            extracted_text = extract_text_txt(uploaded_file)
        st.text_area("Extracted Text", value=extracted_text, height=300)
elif content_type in ["URL", "YouTube Video Link"]:
    input_url = st.text_input("Enter URL")
    if input_url:
        if content_type == "URL":
            extracted_text = extract_text_url(input_url)
        else:
            extracted_text = extract_text_youtube(input_url)
        st.text_area("Extracted Text", value=extracted_text, height=300)