import os
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain_community.document_loaders import JSONLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

def run():
    load_dotenv()
    os.environ["HF_TOKEN"]=os.getenv("HF_TOKEN")
    os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
    groq_api_key=os.getenv('GROQ_API_KEY')
    
    # LLM Model and Embeddings
    llm=ChatGroq(model='llama3-70b-8192',groq_api_key=groq_api_key)
    embeddings=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    job_descriptions=st.file_uploader("Upload your job description",accept_multiple_files=True,type=['txt','json'])
    if job_descriptions:
        documents=[]
        for uploaded_file in job_descriptions:
            file_name=uploaded_file.name
            if file_name.endswith('.txt'):
                temptxt=f"./{file_name}"
                with open(temptxt,'wb') as file:
                    file.write(uploaded_file.getvalue())
                
                loader=TextLoader(temptxt)
                docs=loader.load()
                documents.extend(docs)
            
            else:
                tempjson=f"./{file_name}"
                with open(tempjson,'wb') as file:
                    file.write(uploaded_file.getvalue())
                
                loader=JSONLoader(tempjson)
                docs=loader.load()
                documents.extend(docs)
    ## Split and create embeddings for the documents
        text_splitter=RecursiveCharacterTextSplitter(chunk_size=2500,chunk_overlap=0)
        splits=text_splitter.split_documents(documents)
        
    ## Specify the directory for ChromaDB storage
        storage_directory='D:\Programming\Data Science\Gen AI\Individual_Projects\Job_Matching_and_Candidate_Analysis_System\chromadb'
    ## Creating chromadb vector database
        vectorstore=Chroma.from_documents(documents=splits,embedding=embeddings,persist_directory=storage_directory)
        return vectorstore