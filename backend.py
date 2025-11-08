import os
import PyPDF2
from dotenv import load_dotenv
from langchain_openai import AzureOpenAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.chains import RetrievalQA

load_dotenv()

vectorstore = None
qa_chain = None

def process_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    if not text.strip():
        raise ValueError("No text could be extracted from the PDF.")


    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_text(text)


    docs = [Document(page_content=chunk) for chunk in chunks]


    embeddings = AzureOpenAIEmbeddings(
        azure_endpoint=os.getenv("AZURE_OPENAI_EMB_API_BASE"),
        api_key=os.getenv("AZURE_OPENAI_EMB_API_KEY"),
        deployment=os.getenv("AZURE_OPENAI_EMB_DEPLOYMENT_NAME"),
        api_version="2023-05-15"
    )

    global vectorstore
    vectorstore = FAISS.from_documents(docs, embeddings)


    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    retriever = vectorstore.as_retriever()

    global qa_chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    return "PDF processed and vector store created successfully!"


def answer_question(question):

    global qa_chain
    if qa_chain is None:
        raise ValueError("Please upload and process a PDF first.")
    response = qa_chain({"query": question})
    return response["result"]

