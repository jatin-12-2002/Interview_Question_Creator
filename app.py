from fastapi import FastAPI, Form, Request, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
import os
import aiofiles
from src.helper import llm_pipeline
from fastapi.middleware.cors import CORSMiddleware
from src.celery_app import celery

app = FastAPI()

# Allow all origins for testing; specify allowed origins in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (for styles, docs, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/analyze")
async def analyze_pdf(pdf_file: UploadFile = File(...), num_questions: int = Form(...)):
    base_folder = 'static/docs/'
    os.makedirs(base_folder, exist_ok=True)
    pdf_filename = os.path.join(base_folder, pdf_file.filename)

    # Save the uploaded PDF
    try:
        async with aiofiles.open(pdf_filename, 'wb') as out_file:
            content = await pdf_file.read()
            await out_file.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save PDF: {str(e)}")

    # Generate questions and answers
    try:
        output_file = get_docx(pdf_filename, num_questions)
        response_data = {"output_file": output_file}
        return JSONResponse(content=jsonable_encoder(response_data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during PDF analysis: {str(e)}")


def get_docx(file_path, num_questions):
    pipeline_output = llm_pipeline(file_path, num_questions)
    ques_list = pipeline_output["questions"]
    answer_generation_chain = pipeline_output["answer_generation_chain"]
    
    base_folder = 'static/output/'
    os.makedirs(base_folder, exist_ok=True)
    
    output_file_name = "QA.docx"
    output_file = os.path.join(base_folder, output_file_name)

    # Create a DOCX document
    from docx import Document
    doc = Document()
    doc.add_heading('Interview Questions and Answers', 0)

    for i, question in enumerate(ques_list[:num_questions], start=1):
        doc.add_heading(f"Question {i}:", level=1)
        doc.add_paragraph(question)

        # Retrieve answer
        try:
            answer = answer_generation_chain.run(question)
        except Exception as e:
            answer = f"Answer generation failed: {str(e)}"
        
        doc.add_heading("Answer:", level=2)
        doc.add_paragraph(answer)
        doc.add_paragraph("--------------------------------------------------\n\n")

    doc.save(output_file)
    return output_file_name


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True)