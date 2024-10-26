JOB MATCHING AND CANDIDATE ANALYSIS SYSTEM

The project focuses on job matching and interview analysis designed to automate resume-job matching and analyzing interview videos. This project uses NLP,LLMs,RAG and vector databases.

Main Features:
1. Job Matching
2. Interview Analysis

Project Structure:
- app.py
- Recruiter/jobs.py
- User/user.py
- interview_analysis/interview_analysis.py
- requirements.txt

Let's start with the setup -

Setup Instructions:
- Create a virtual environment for our project by using the command :
    "python -m venv environment_name"

- Activate the virtual environment by using the bash command (if using bash terminal) :
    "source environment_name/Scripts/activate"

- Install the libraries from "requirements.txt" file by using the command :
    "pip install -r requirements.txt"
    (make sure all the requirements are installed)

- To Run the Application use the command:
    "streamlit run app.py"
    (make sure you are in the same folder as app.py when running the command.)

Additional Information:
- I have provided the ".env" file along with all the folders and files so that the groq api keys and huggingface tokens are not required additionally. I have already added my api key and token in my env file.
- Our code required FFMPEG library to be downloaded additionally to add the functionality of transcribing and handling the media files. So I have downloaded it, added the folder here and integrated it with our code.

Usage Guidelines:
- Upon running the streamlit app, you can find basic information and a navigation bar on the left side.
-  In the navigation bar, you can encounter 3 main options/functionalities.
    1. Recruiter - Recruiter dashboard (Upload job descriptions).
    2. User - User Dashboard (Upload resume).
    3. Interview Analysis - Dashboard for interview analysis (Upload interview video for analysis).
- You can choose either one of them according to your needs.
- Ideally, there would be no job descriptions uploaded initially. To get the job matching results in user dashboard, you would have to upload job descriptions in recruiter dashboard first.
- I have provided "Upload samples" folder in the zip file for testing, where you can find samples of interview,job descriptions and resume.

Results :
- You can see job-matching results in user dashboard and interview analysis results in interview analysis dashboard once executed.

Dependencies :
All the dependencies are present in requirements.txt. Once the setup is complete, there would be no additional dependencies required.