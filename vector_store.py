#This will generate the vector db from the books
import os
import google.generativeai as genai
from utils.rag_utils import get_pdf_text,get_text_chunks,get_vector_store
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))



# def get_conv_chain():
#     prompt_template = """
#     Answer the question as detailed as possible from the provided context,
#     make sure to provide answer accurately based on the context, don't provide 
#     the wrong answer,
#     Context: \n {context}?\n
#     Question: \n {question}\n

#     Answer: 
#     """
#     model = ChatGoogleGenerativeAI(model = 'gemini-pro',temperature=0.3)

#     prompt = PromptTemplate(template=prompt_template,input_variables=['context','question'])
#     chain = load_qa_chain(
#         model,chain_type='stuff',
#         prompt = prompt
#     )
#     return chain

# def user_input(query):
#     embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
#     vector_db = FAISS.load_local('faiss_index',embeddings,allow_dangerous_deserialization=True)
    
#     docs = vector_db.similarity_search(query)
#     chain = get_conv_chain()

#     response = chain(
#         {"input_documents": docs,"question":query},
#         return_only_outputs=True
#     )

#     print(response)

def create_vector_store():
    pdf_docs = "references"
    raw_text = get_pdf_text(pdf_docs)
    text_chunks = get_text_chunks(raw_text)
    get_vector_store(text_chunks)

if __name__ == '__main__':
    create_vector_store()




