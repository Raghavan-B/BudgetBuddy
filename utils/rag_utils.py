import os
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS

def get_gemini_response(prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text

def prompt_template_dash():
    prompt="""You are a financial expert reviewing the user's Dashboard on the BudgetBuddy app. 
    Analyze their daily tracked expenses for today, the cumulative expenses for the month across all categories (Rent, Shopping, Daily Spendings, Loan, Bills, Others, Groceries), 
    and the optimal budget allocation calculated by BudgetBuddy.

Provide a **holistic overview** of their current financial status.  
- Highlight areas where they are overspending or underspending compared to the optimal budget.  
- Advise on how their current spending aligns with meeting their monthly savings target.  
- Motivate the user by acknowledging positive financial habits while offering specific guidance for improvement.  

Conclude with an overall assessment:  
- Are they on track to meet their savings target?  
- What should they focus on in the coming days to improve their financial standing?  

Ensure your tone is friendly, polite, and encouraging, with actionable and personalized advice. Avoid generic suggestions, focusing on specific spending categories and their impact.  



"""
    return prompt


def load_vectorstore_as_retriever():
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    vector_store = FAISS.load_local("faiss_index",embeddings,allow_dangerous_deserialization=True)
    return vector_store.as_retriever()


def prompt_template_chat():
    prompt = """You are a financial expert specialized in personal finance, integrated into the BudgetBuddy app. 
    Users can ask you any questions about their finances, including personalized queries related to their spending, saving habits, and optimal budget.  

    Retrieve relevant information from the context and their persona (including their tracked spending, cumulative expenses, and savings goals) to provide **accurate and personalized answers** to their queries.
    If the user asks for general financial advice (e.g., "How to invest?" or "How to increase income?"), provide comprehensive,
    actionable advice based on general financial knowledge and the context available.  

    If the question is unclear or unrelated to personal finance, politely request clarification or provide a 
    generic overview of the topic if it fits within the financial domain. Always prioritize politeness and motivation in your tone, 
    ensuring that users feel supported and guided in their financial journey.  
    
    You can have a reference on the following context whenever needed (you dont have to specify the references just say based on my knowledge)
    and the information given is :
    {context}

    Question: {question}
    """
    return prompt

def get_pdf_text(pdf_docs):
    text = ''
    for pdf in os.listdir(pdf_docs):
        pdf_reader = PdfReader(os.path.join(pdf_docs,pdf))
        for page in pdf_reader.pages:
            text+=page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 10000,chunk_overlap = 1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks,embedding = embeddings)
    vector_store.save_local("faiss_index")
    print("Vector Store Saved successfully")


def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])
