import shutil
import os
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from services import transcribe_audio, summarize_text

app = FastAPI()

templates = Jinja2Templates(directory="templates")

os.makedirs("temp", exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/process")
async def process_audio(file: UploadFile = File(...)):
    temp_filename = f"temp/{file.filename}"

    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        transcript_text = transcribe_audio(temp_filename)

        summary_text = summarize_text(transcript_text)

        os.remove(temp_filename)

        return {
            "filename": file.filename,
            "transcript_preview": transcript_text[:200] + "...",
            "summary": summary_text
        }

    except Exception as e:
        return {"error": str(e)}