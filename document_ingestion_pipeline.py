import os##for doing the file management 
import glob## accesssing the file using the pattern 
from pathlib import Path##used for handeling the file path in string object 
from langchain_core.documents import Document##it is uded to perform langchain document structure operation
from langchain_pymupdf4llm import PyMuPDF4LLMLoader##it is hybrid version of pdf reader it read the content form the pdf of for both scanned and the originay format 
from langchain_text_splitters import MarkdownTextSplitter##used to split the document into chunks for embedding for reducing the LLM context window size 
from langchain_huggingface import HuggingFaceEmbeddings##importing for the purpose of loading the embedding model to convert the chuncks to vector 
from sentence_transformers import SentenceTransformer#the back embedding model was working by the sentence transformer
from langchain_chroma import Chroma
import os


"""
This class handles the full process of getting the pdf ---->documents-------->chunks------->vector_embedding---->storing in vector DataBase
"""
class Document_ingestion:
    """This handles the convertion pdf parsing and converting to the document structure """

    def ingestion_from_pdf_to_document(self,path_name):
        filenames = glob.glob(
        f"{path_name}/**/*.pdf",
        recursive=True
        )##identify the pattern file recurisevely and store the all file names it return the list 
        documents=[]
        print("Now currently entering into the loop for")
        for filename in filenames:##travering the file names for the purpose of getting the path
            path=Path(filename)##getting the path in string object 
            if path.is_file() and path.suffix.lower()==".pdf":#checking the path is a file path and it is in pdf format or not 
                print("Started to reading the file ")
                loader = PyMuPDF4LLMLoader(path)##Loading the pdf parsing model to parse our pdf I used this model because our data is a scanned and the orginal pdf parsed and loaded 
                print(f"\nfile {path} is  readed and now it is loading into the documet in the lanchain document format🫡 ")
                docs=loader.load()##loading the parsed data into the docs variable  return the list of document object 
                documents.extend(docs)##using the extend instead of append ,because append create the new list and store 
        print("The file is fully loaded🥳")        
        return documents
    
    """
    ==================================================================================================================================
    This divide the document into the chuncks .
    """
    def chunking_pipeline(self,documents):
        splitter = MarkdownTextSplitter(
        chunk_size=1000, 
        chunk_overlap=150
        )#using the mark down text splitter because the  PyMuPDF4LLMLoader return the docs in the markdown format
        final_chunks = splitter.split_documents(documents)
        return final_chunks
    """
    It handles the full process of converting the pdf to vector and loading into the vector database.the main function is storing in the vector data base
    """
    def pdf_to_vector_database(self,path_name,vector_name):
        documents=self.ingestion_from_pdf_to_document(path_name)
        print("\npdf to document was converted")
        chunks=self.chunking_pipeline(documents)
        print("\n chunks was created successfully")
        print("\nCrating the embedding model🫣")
        """Loading our hugging face model to converting the chuncks to embedding and store in the vector database"""
        embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    
        )
        print("\nThe model was loaded successfully 🫡🥲")


        print("\n Now started to loading into the vector database😎")
        print(embeddings)
        if os.path.exists(vector_name):
                Chroma(persist_directory=vector_name, embedding_function=embeddings).delete_collection()
        vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=vector_name)
        print(f"Vectorstore created with {vectorstore._collection.count()} documents")
    def ingestion_from_pdf_to_document_for_user_live(self,path_name):

        documents=[]
        
        loader = PyMuPDF4LLMLoader(path_name)
        print(f"\nfile {path_name} is  readed and now it is loading into the documet in the lanchain document format🫡 ")
        docs=loader.load()
        documents.extend(docs)
        print("The file is fully loaded🥳")        
        return documents
    def pdf_to_vector_database_for_live_user(self,path_name,vector_name):
        documents=self.ingestion_from_pdf_to_document_for_user_live(path_name)
        print("\npdf to document was converted")
        chunks=self.chunking_pipeline(documents)
        print("\n chunks was created successfully")
        print("\nCrating the embedding model🫣")
        embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    
        )
        print("\nThe model was loaded successfully 🫡🥲")


        print("\n Now started to loading into the vector database😎")
        print(embeddings)
        if os.path.exists(vector_name):

           Chroma(persist_directory=vector_name, embedding_function=embeddings).delete_collection()

        vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=vector_name)

        print(f"Vectorstore created with {vectorstore._collection.count()} documents")
        


