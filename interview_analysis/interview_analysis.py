import streamlit as st
import os

ffmpeg_path = r"C:\Users\Admin\Downloads\ffmpeg-7.1-essentials_build\bin"  # Change this to your actual path
os.environ["PATH"] += os.pathsep + ffmpeg_path

import tempfile
import whisper
import ffmpeg
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from moviepy.editor import VideoFileClip

st.set_page_config(page_title="Interview Analysis",page_icon="💼")

st.header("Interview Analysis")
st.subheader("Uploade the interview video to recieve a detailed summary of the candidate's responses.")

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
groq_api_key = os.getenv('GROQ_API_KEY')
model=whisper.load_model("base")
llm=ChatGroq(model="llama3-70b-8192",groq_api_key=groq_api_key)

def extract_audio(video_path, audio_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_path)
    video.close()
    
def run():
    interview=st.file_uploader("Upload Interview Video",type=["mov","mp4","avi"])

    if interview:
        file_name=interview.name
        temp_vdo=f"./{file_name}"
        temp_ado=r"D:\Programming\Data Science\Gen AI\Individual_Projects\Job_Matching_and_Candidate_Analysis_System\interview_analysis\audio.wav"
        
        with open(temp_vdo,'wb') as file:
            file.write(interview.read())
        st.write("Analyzing Interview.......")
        extract_audio(temp_vdo,temp_ado)
        
        result=model.transcribe(r"D:\Programming\Data Science\Gen AI\Individual_Projects\Job_Matching_and_Candidate_Analysis_System\interview_analysis\audio.wav")
        transcription=result["text"]
        
        st.write("Generating Response.......")
        
        prompt_template=f"""
        You are an expert in analyzing interviews. Given the following transcription of an interview, summarize the candidate's responses,
        and highlight key traits such as 
        1. Communication Style (How the candidate expresses ideas and conveys information)
        2. Active Listening (The candidate’s ability to understand and respond appropriately to questions)
        3. Engagement with the Interviewer (The level of interaction and rapport established during the interview)
        
        Interview Transcript:
        {transcription}
        
        Please provide a detailed analysis
        """
        prompt=PromptTemplate(input_variables=["transcription"],template=prompt_template)
        chain=LLMChain(llm=llm,prompt=prompt)
        response=chain.run({"transcription":transcription})
        # summary=response["content"]
        
        st.subheader("Interview Summary")
        st.write(response)
