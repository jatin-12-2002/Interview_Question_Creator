import time
import os
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
from langchain.docstore.document import Document
from langchain.text_splitter import TokenTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from src.prompt import prompt_template, refine_template  # Import the templates

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# Function to implement retry mechanism with exponential backoff
def call_with_retry(func, retries=3, delay=2):
    attempt = 0
    while attempt < retries:
        try:
            return func()
        except Exception as e:
            attempt += 1
            print(f"Error: {str(e)}. Retrying {attempt}/{retries}...")
            if attempt < retries:
                time.sleep(delay)  # Wait before retrying
                delay *= 2  # Exponential backoff
            else:
                raise ValueError(f"Failed after {retries} attempts: {str(e)}")

def file_processing(file_path):
    try:
        loader = PyPDFLoader(file_path)
        data = loader.load()
    except Exception as e:
        raise ValueError(f"Failed to load PDF: {str(e)}")

    # Aggregate content from all PDF pages
    question_gen = ''.join([page.page_content for page in data])

    # Split content into chunks for question generation
    splitter_ques_gen = TokenTextSplitter(
        model_name='gpt-3.5-turbo',
        chunk_size=10000,
        chunk_overlap=200
    )
    chunks_ques_gen = splitter_ques_gen.split_text(question_gen)

    # Create Document objects from text chunks
    document_ques_gen = [Document(page_content=t) for t in chunks_ques_gen]

    # Split content for answer generation
    splitter_ans_gen = TokenTextSplitter(
        model_name='gpt-3.5-turbo',
        chunk_size=1000,
        chunk_overlap=100
    )
    document_answer_gen = splitter_ans_gen.split_documents(document_ques_gen)

    return document_ques_gen, document_answer_gen

def llm_pipeline(file_path, num_questions):
    document_ques_gen, document_answer_gen = file_processing(file_path)

    # Initialize LLM with temperature control
    llm_ques_gen_pipeline = ChatGoogleGenerativeAI(
        temperature=0.3,
        model="gemini-1.5-flash"
    )

    # Create prompt templates for questions and refining
    PROMPT_QUESTIONS = PromptTemplate(
        template=prompt_template,
        input_variables=["text", "num_questions"]
    )

    REFINE_PROMPT_QUESTIONS = PromptTemplate(
        template=refine_template,
        input_variables=["existing_answer", "text"]
    )

    # Retry mechanism for the question generation chain
    def question_generation_func():
        ques_gen_chain = load_summarize_chain(
            llm=llm_ques_gen_pipeline,
            chain_type="refine",
            verbose=True,
            question_prompt=PROMPT_QUESTIONS,
            refine_prompt=REFINE_PROMPT_QUESTIONS
        )

        return ques_gen_chain.run({
            'input_documents': document_ques_gen,
            'num_questions': num_questions
        })

    try:
        # Using retry mechanism
        ques = call_with_retry(question_generation_func, retries=3, delay=5)
    except Exception as e:
        raise ValueError(f"Question generation failed: {str(e)}")

    # Embeddings for answer generation
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_documents(document_answer_gen, embeddings)

    # LLM for answer generation
    llm_answer_gen = ChatGoogleGenerativeAI(temperature=0.1, model="gemini-1.5-flash")

    # Process the questions into a list
    ques_list = ques.split("\n")
    filtered_ques_list = [q for q in ques_list if q.endswith('?') or q.endswith('.')]

    # Retrieval-based answer generation
    answer_generation_chain = RetrievalQA.from_chain_type(
        llm=llm_answer_gen,
        chain_type="stuff",
        retriever=vector_store.as_retriever()
    )

    return answer_generation_chain, filtered_ques_list