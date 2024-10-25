import streamlit as st
import os

## adding the path of our ffmpeg framework because ffmpeg is required for audio extraction and conversion
ffmpeg_path = r"D:\Programming\Data Science\Gen AI\Individual_Projects\Job_Matching_and_Candidate_Analysis_System\ffmpeg-7.1-essentials_build\bin"  # Change this to your actual path
os.environ["PATH"] += os.pathsep + ffmpeg_path

import whisper
import ffmpeg
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from moviepy.editor import VideoFileClip


# Function to extract audio using moviepy
def extract_audio(video_path, audio_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_path)
    video.close()

# Run function, which is executed when the interview analysis option is selected    
def run():

    st.subheader("Upload the interview video to recieve a detailed summary of the candidate's responses.")

    # Fetching the groq api key from our .env file
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
    groq_api_key = os.getenv('GROQ_API_KEY')
    
    #loading the whisper model
    model=whisper.load_model("base")
    
    # Defining our llm model with the help of ChatGroq
    llm=ChatGroq(model="llama3-70b-8192",groq_api_key=groq_api_key)
    
    # File uploader
    interview=st.file_uploader("Upload Interview Video",type=["mov","mp4","avi"])

    if interview:
        st.video(interview)
        st.success("Video Uploaded Successfully!")
        file_name=interview.name
        temp_vdo=f"./{file_name}"
        temp_ado=r"D:\Programming\Data Science\Gen AI\Individual_Projects\Job_Matching_and_Candidate_Analysis_System\interview_analysis\audio.wav"
        
        # Function to save the video file temporarily
        with open(temp_vdo,'wb') as file:
            file.write(interview.read())
        st.write("Analyzing Interview.......")
        
        # Calling our extract_audio function to extract the audio from our temporarily saved video
        extract_audio(temp_vdo,temp_ado)
        
        # Converting audio to text (transcription)
        result=model.transcribe(r"D:\Programming\Data Science\Gen AI\Individual_Projects\Job_Matching_and_Candidate_Analysis_System\interview_analysis\audio.wav")
        transcription=result["text"]
        
        st.write("Generating Response.......")
        
        # Our prompt to the llm
        prompt_template=f"""
        You are an expert in analyzing interviews. Given the following transcription of an interview, summarize the candidate's responses,
        and highlight key traits such as 
        1. Communication Style (How the candidate expresses ideas and conveys information)
        2. Active Listening (The candidate’s ability to understand and respond appropriately to questions)
        3. Engagement with the Interviewer (The level of interaction and rapport established during the interview)
        
        Interview Transcript:
        {transcription}
        Keep the response concise and cover all the points
        """
        
        # Our prompt template, llm chain and response after running the chain
        prompt=PromptTemplate(input_variables=["transcription"],template=prompt_template)
        chain=LLMChain(llm=llm,prompt=prompt)
        response=chain.run({"transcription":transcription})
        
        st.subheader("Interview Summary")
        
        # To display the response
        st.write(response)
