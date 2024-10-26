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

# Run function, which is executed when the recruiter option is selected
def run():
    load_dotenv()
    
    # Fetching our hugging face token and groq api key from .env file
    os.environ["HF_TOKEN"]=os.getenv("HF_TOKEN")
    os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
    groq_api_key=os.getenv('GROQ_API_KEY')
    
    # LLM Model and HuggingFace Embeddings
    llm=ChatGroq(model='llama3-70b-8192',groq_api_key=groq_api_key)
    embeddings=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    st.subheader("Here you can upload multiple job descriptions in formats like TEXT or JSON")
    job_descriptions=st.file_uploader("Upload your job description",accept_multiple_files=True,type=['txt','json'])
    if job_descriptions:
        try:
            documents=[]
            
            ## This will go through each uploaded file and convert it into text 
            # after which it will get appended into our documents list.
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
                    
        ## Splitting the documents
            text_splitter=RecursiveCharacterTextSplitter(chunk_size=2500,chunk_overlap=0)
            splits=text_splitter.split_documents(documents)
            
        ## Specifying the directory for ChromaDB storage (our persistent vector database)
            storage_directory='chromadb'
            
        ## Creating chromadb vector database
            vectorstore=Chroma.from_documents(documents=splits,embedding=embeddings,persist_directory=storage_directory)
            st.success("Documents uploaded and processed successfully!")
            return vectorstore
        
        except Exception as e:
            print("An error Occured",e)