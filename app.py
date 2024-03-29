import streamlit as st
from dotenv import load_dotenv

load_dotenv() ##load all the nevironment variables
import os
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# prompt="""You are Yotube video summarizer. You will be taking the transcript text
# and summarizing the entire video and providing the important summary in points
# within 5000 words. Please provide the summary of the text given here:  """

# prompt = """As a YouTube video summarizer, your task is to generate a concise summary of the provided transcript.
#  Your summary should encapsulate the key points discussed in the video within a maximum of 5000 words. 
#  Please analyze the transcript below and provide a detailed summary."""

# prompt = """You are a concise and informative YouTube video summarizer. 
# Analyze the provided transcript text and identify the key points discussed in the video. 
# Present a bulleted list summary highlighting the most important information, focusing on actionable takeaways and key concepts. 
# Ensure the summary is clear, well-structured, and adheres to a 5000-word limit."""

prompt = """As a YouTube video summarizer, your objective is to thoroughly analyze the transcript text of the video and 
provide a comprehensive summary that elaborates on the key topics discussed. Your summary should delve into each important 
topic in detail, providing insightful explanations and relevant information. Ensure that the summary is informative and 
engaging, covering essential aspects within a word limit of 5000 words. Please proceed to generate the summary based on the 
provided transcript:"""

## getting the transcript data from yt videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e
    
## getting the summary based on Prompt from Google Gemini Pro
# def generate_gemini_content(transcript_text,prompt):

#     model=genai.GenerativeModel("gemini-pro")
#     response=model.generate_content(prompt+transcript_text)
#     return response.text
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(str(prompt) + " " + str(transcript_text))
    return response.text


st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes"):
    transcript_text=extract_transcript_details(youtube_link)

    if transcript_text:
        summary=generate_gemini_content(transcript_text,prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)




