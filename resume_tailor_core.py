# resume_tailor_core.py

import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

def analyze_resume(resume_path, jd_path):
    # --- Load PDF Documents ---
    resume_docs = PyPDFLoader(resume_path).load()
    jd_docs = PyPDFLoader(jd_path).load()
    all_docs = resume_docs + jd_docs

    # --- Split into Chunks ---
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = splitter.split_documents(all_docs)

    # --- Create Embeddings & Retriever ---
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(split_docs, embedding_model)
    retriever = vectorstore.as_retriever()

    # --- Load OpenAI model ---
    llm = ChatOpenAI(
        temperature=0.3,
        model="gpt-4o-mini",  # or "gpt-3.5-turbo"
        max_tokens=1000,
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_api_base=os.getenv("OPENAI_BASE_URL")
    )

    # --- Retrieval QA Chain ---
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    # --- Ask the question ---
    question = "What improvements can I make to my resume for this job description?"
    return qa_chain.run(question)
