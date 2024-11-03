import os
import logging
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.docstore.document import Document
from langchain.text_splitter import TokenTextSplitter
from langchain_mistralai import ChatMistralAI
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from src.prompt import prompt_template, refine_template  # Import the templates

# Load environment variables
load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
os.environ["MISTRAL_API_KEY"] = MISTRAL_API_KEY

HF_TOKEN = os.getenv("HF_TOKEN")
os.environ["HF_TOKEN"] = HF_TOKEN

# Set up logging for better debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

    logger.info(f"Generated {len(document_ques_gen)} chunks for questions and {len(document_answer_gen)} for answers.")

    return document_ques_gen, document_answer_gen

def llm_pipeline(file_path, num_questions):
    document_ques_gen, document_answer_gen = file_processing(file_path)

    # Initialize LLM with temperature control
    llm_ques_gen_pipeline = ChatMistralAI(
        temperature=0.3,
        model="mistral-large-latest"
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

    ques_gen_chain = load_summarize_chain(
        llm=llm_ques_gen_pipeline,
        chain_type="refine",
        verbose=True,
        question_prompt=PROMPT_QUESTIONS,
        refine_prompt=REFINE_PROMPT_QUESTIONS
    )

    # Run question generation chain
    try:
        ques = ques_gen_chain.run({
            'input_documents': document_ques_gen,
            'num_questions': num_questions
        })
    except Exception as e:
        logger.error(f"Question generation failed: {e}")
        raise ValueError(f"Question generation failed: {str(e)}")

    # Embeddings for answer generation
    embeddings = MistralAIEmbeddings(model="mistral-embed")
    vector_store = FAISS.from_documents(document_answer_gen, embeddings)

    # LLM for answer generation
    llm_answer_gen = ChatMistralAI(temperature=0.1, model="mistral-large-latest")

    # Process the questions into a list
    ques_list = ques.strip().split("\n")
    filtered_ques_list = [q for q in ques_list if q.strip().endswith('?') or q.strip().endswith('.')]

    # Retrieval-based answer generation
    answer_generation_chain = RetrievalQA.from_chain_type(
        llm=llm_answer_gen,
        chain_type="stuff",
        retriever=vector_store.as_retriever()
    )
    
    logger.info(f"Generated {len(filtered_ques_list)} questions.")

    # Return structured data for easier frontend handling
    return {
        "answer_generation_chain": answer_generation_chain,
        "questions": filtered_ques_list
    }