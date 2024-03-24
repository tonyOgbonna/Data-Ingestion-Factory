import gradio as gr
import requests
from io import BytesIO
from PyPDF2 import PdfReader
import youtube_transcript_api

def extract_text(content_type, input_data):
    extracted_text = "Text extraction not implemented for this type."
    
    if content_type == "PDF File":
        reader = PdfReader(BytesIO(input_data))
        extracted_text = "\n\n".join([page.extract_text() for page in reader.pages])
        
    elif content_type == "Text File":
        extracted_text = input_data.decode("utf-8")
        
    elif content_type == "URL":
        response = requests.get(input_data)
        extracted_text = response.text[:1000]  # Displaying only the first 1000 characters for demonstration
        
    elif content_type == "YouTube Video Link":
        video_id = input_data.split("watch?v=")[-1]
        transcript_list = youtube_transcript_api.YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_transcript(['en'])
        extracted_text = "\n".join([t['text'] for t in transcript.fetch()])
        
    return extracted_text

with gr.Blocks() as app:
    gr.Markdown("# Text Content Extractor")
    
    with gr.Row():
        content_type = gr.Radio(["PDF File", "Text File", "URL", "YouTube Video Link"], label="Select Content Type")
        input_data = gr.Textbox(label="Input", lines=2)
    
    output_text = gr.Textbox(label="Extracted Text", lines=10, interactive=True)
    
    content_type.change(fn=lambda x: "Enter URL" if x == "URL" or x == "YouTube Video Link" else "Upload File", 
                        inputs=content_type, 
                        outputs=input_data)
    
    gr.Button("Extract").click(extract_text, inputs=[content_type, input_data], outputs=output_text)

app.launch()