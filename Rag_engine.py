from system_prompt import system_prompt##The package handle the system prompt based on the user selection of marks 
from langchain_classic.retrievers import EnsembleRetriever##this package was used to handle two retrivers Bm25 and the semantic search 
from langchain_community.retrievers import BM25Retriever##the package for the keyword  search
from langchain_core.documents import Document#to create langchain document structure it is a standard structure 
from langchain_huggingface import HuggingFaceEmbeddings##for performing the embedding task
from langchain_chroma import Chroma##importing the chroma db to store the vector 
from langchain_core.messages import SystemMessage, HumanMessage#importing to communicate with LLM
from langchain_openai import ChatOpenAI##Importing the langchain open Ai client api
import os#perform the file management 
from dotenv import load_dotenv#to overide the env variable 
from document_ingestion_pipeline import Document_ingestion##this package handles the full functionality of converting the pdf to vector and store in the vector data base
from langsmith import traceable


"""
This class going to handle the full process of retrival,agumentation and generation
"""

@traceable
class Rag_engine:
    ##the call back function for gradio framework for the function chat interface 
    def answer_call_back(message_from_user,history,user_semester,mark_value,file_upload):
       
        if file_upload and user_semester=="My Pdf":## Here we checking the logic the file is up[loaded and the user is willing to ask the question in the uploaded pdf]
            file_path=file_upload##storing the file path in the variable 
            print(file_upload)
            object_Document_ingestion=Document_ingestion()##creating the object for document injection class for the converting the uploaded file into vector and store into the data base for retrival
            object_Document_ingestion.pdf_to_vector_database_for_live_user(path_name=file_path,vector_name="user_vector")##the chuncking,vectorizing and storing process was happening here 
        load_dotenv(override=True)##overiting the env variable for loading the api of groq
        groq_api= os.getenv("GROQ_API")##loading the groq api from the env folder 
        llm=ChatOpenAI(temperature=0,model_name="openai/gpt-oss-120b",base_url="https://api.groq.com/openai/v1",api_key=groq_api)#calling the langchain chat open ai which is a wrapper of open ai python client library.I kept the temperature 0 ,because I need the full probability token from the model"        
        if user_semester=="Semester-1":##the vector database rooting  was appening here based on the  the user suggestion to selection of semester to get answer
            DB_NAME="Semester-1-data-source-vector"
        elif user_semester=="Semester-2":
            DB_NAME="Semester-2-data-source-vector"
        elif user_semester=="Semester-3":
            DB_NAME="Semester-3-data-source-vector"
        elif user_semester=="Semester-4":
            DB_NAME="Semester-4-data-source-vector"
        elif user_semester=="Semester-5":
            DB_NAME="Semester-5-data-source-vector"
        elif user_semester=="Semester-6":
            DB_NAME="Semester-6-data-source-vector"
        elif user_semester=="My Pdf":
            DB_NAME="user_vector"
        if mark_value=="16":#rooting to the various prompt based the user mark requirement
            print("Entered into 16 marks prompt")
            system_message=system_prompt.System_prompt_16
        elif mark_value=="10":
            system_message=system_prompt.System_prompt_10
        elif mark_value=="18":
            system_message=system_prompt.System_prompt_18
        elif mark_value=="20":

            system_message=system_prompt.System_prompt_20
        elif mark_value=="2":
            print("Entered into 2 marks prompt")
            system_message=system_prompt.System_prompt_2
        elif mark_value=="5":
            system_message=system_prompt.System_prompt_5
        elif mark_value=="Learn":
            system_message=system_prompt.System_prompt_learn
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")##loading the hugging face embedding model 
        vectorstore = Chroma(persist_directory=DB_NAME, embedding_function=embeddings)##creating the pointer to the vecotor store
        vector_retriver=vectorstore.as_retriever(search_type="similarity_score_threshold",search_kwargs={"score_threshold":0.1,"k":5})##creatingthe retriver for semantic search
        all_docs=vectorstore.get()["documents"]##here we need all document to compute TF-IDF scores
        bm25_docs=[
            Document(page_content=doc)
            for doc in all_docs
        ]
        bm25_retriver=BM25Retriever.from_documents(bm25_docs)
        bm25_retriver.k=5
        retriever=EnsembleRetriever(
            retrievers=[
                bm25_retriver,
                vector_retriver
            ],
            weights=[0.7,0.3]##the influence was making based on the weights in final score 
        )
        docs=retriever.invoke(message_from_user)##langchain high level abstraction of the   retriver to retrive and store the chuncks based on the user question

        system_message=system_message.format(answer_key=docs)##finally adding the chunks to the system prompt for the context 
        response=llm.invoke([SystemMessage(content=system_message), HumanMessage(content=message_from_user)])##the high level langchain abstraction of the open Ai python client library
        return response.content#finally returning the response of the llm 
    