import os
import streamlit as st
import Recruiter.jobs as jobs
import User.user as user
import interview_analysis.interview_analysis as analysis


## Streamlit app

def main():
    st.sidebar.title("Choose your Functionality")
    options=["Home","Recruiter","User","Interview Analysis"]
    choice=st.sidebar.selectbox("Functionalities",options,index=0)
    
    if choice=="Home":
        st.title("👨🏻‍💼 : Job Matching and Candidate Analysis System")
        st.subheader("A tool that enhances the recruitment process by automating the alignment of resumes with job requirements and evaluating interview content.")
        st.write("Go ahead and give it a try!!!")
        
    elif choice=="Recruiter":
        st.header("Recruiter Dashboard")
        jobs.run()
    
    elif choice=="User":
        st.header("User Dashboard")
        user.run()
        
    elif choice=="Interview Analysis":
        st.header("Interview Analysis")
        analysis.run()
        
if __name__=="__main__":
    main()