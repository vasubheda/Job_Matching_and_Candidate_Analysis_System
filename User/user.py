import os
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

def run():
    load_dotenv()
    os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
    groq_api_key = os.getenv('GROQ_API_KEY')
    
    ## LLM Model and Embeddings
    llm = ChatGroq(model='llama3-70b-8192', groq_api_key=groq_api_key)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    resume=st.file_uploader("Upload your resume",type=['pdf','docx'])
    if resume:
        file_name=resume.name
        if file_name.endswith('.pdf'):
            temppdf=f"./{file_name}"
            with open(temppdf,'wb') as file:
                file.write(resume.getvalue())
                    
            loader=PyPDFLoader(temppdf)
                
        else:
            tempdoc=f"./{file_name}"
            with open(tempdoc,'wb') as file:
                file.write(resume.getvalue())
                    
            loader=Docx2txtLoader(tempdoc)
        
        docs=loader.load()
        text=docs[0].page_content
        
        storage_directory='D:\Programming\Data Science\Gen AI\Individual_Projects\Job_Matching_and_Candidate_Analysis_System\chromadb'
        vectorstore=Chroma(persist_directory=storage_directory,embedding_function=embeddings)
        
        retriever=vectorstore.as_retriever(search_type='similarity')
        matching_docs=retriever.get_relevant_documents(text)
        
        prompt_template="""
        Based on this resume:
        {resume}
        Compare it with the job description:
        {job_description}
        Identify all the unique job roles and calculate the matching score out of 10.
        Then, Provide us the following in descending order with respect to the matching score:
        1. Provide the job role/title.
        2. Provide analytics to show why a candidate is a good fit for that particular job, highlighting:
            - Rank among all other job descriptions.
            - Skill match percentage.
            - how the candidate's experience aligns with the job's requirements.
            - Are the degree and certifications relevant to the job.
            - Tools and technologies mentioned in both the resume and job description.
            - matching score out of 10.
        Note: Provide very concise and onto the point response.
        DONT REPEAT ANY JOB DESCRIPTIONS WHICH ARE ALREADY PRESENT IN THE RESPONSE.
        """
        prompt=PromptTemplate(input_variables=["resume","job_description"],template=prompt_template)
        chain=LLMChain(llm=llm,prompt=prompt)
        
        for doc in matching_docs:
            job_description=doc.page_content
            result=chain.run({"resume":text,"job_description":job_description})
            st.write(result)