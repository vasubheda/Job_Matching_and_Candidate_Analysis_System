import os
import streamlit as st
import recruiter.jobs as jobs
import User.user as user
import interview_analysis.interview_analysis as analysis


## Streamlit app

def main():
    st.sidebar.title("Navigation")
    options=["Home","Recruiter","User","Interview Analysis"]
    choice=st.sidebar.selectbox("Choose your functionality",options,index=0)
    
    if choice=="Home":
        st.title("📃 : Job Matching and Candidate Analysis System")
        st.subheader("A tool that enhances the recruitment process by automating the alignment of resumes with job requirements and evaluating interview content.")
        
    elif choice=="Recruiter":
        st.subheader("Recruiter Dashboard")
        jobs.run()
    
    elif choice=="User":
        st.subheader("User Dashboard")
        user.run()
        
    elif choice=="Interview Analysis":
        st.subheader("Interview Analysis")
        analysis.run()
        
if __name__=="__main__":
    main()