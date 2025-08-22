from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import PyPDF2
import io
from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import login
import torch
from typing import Dict
import uvicorn
import re
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

login(new_session=False)

app = FastAPI(title="Resume Analysis", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B-Instruct",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map="auto" if torch.cuda.is_available() else None
)

class AnalysisResult(BaseModel):
    overall_score: float
    overall_score_reason: str
    programming_score: float
    programming_score_reason: str
    ai_ml_score: float
    ai_ml_score_reason: str
    analytical_score: float
    analytical_score_reason: str
    tech_experience_score: float
    tech_experience_score_reason: str
    tools_score: float
    tools_score_reason: str
    knowledge_score: float
    knowledge_score_reason: str


class ResumeAnalyzer:
    def __init__(self):
        self.job_description = """
        ตำแหน่ง: AI & Data Solution Intern

        Responsibilities
        ทำงานร่วมกับผู้ใช้งานหรือทีมพัฒนาธุรกิจ เพื่อรวบรวมและทำความเข้าใจความต้องการของระบบ
        ออกแบบ พัฒนา และปรับแต่งคำสั่ง prompt เพื่อเพิ่มประสิทธิภาพการทำงานของ AI
        ออกแบบโครงสร้างระบบ กระบวนการทำงาน และการใช้งานของ AI application
        ใช้ Large Language Models (LLMs) เพื่อพัฒนา AI application
        ทดสอบการทำงานและประเมินประสิทธิภาพของ AI application
        ทำงานร่วมกับทีมวิศวกรซอฟต์แวร์อย่างใกล้ชิด เพื่อนำ AI application ไปใช้ในระบบจริง

        Qualifications
        ชำนาญในการเขียนโปรแกรมด้วย Python, prompt engineering, และ context engineering
        มีทักษะในการคิดวิเคราะห์และแก้ไขปัญหาได้อย่างดีเยี่ยม
        มีความสนใจในด้าน AI ระบบอัตโนมัติ (automation) และ data-driven solutions
        มีความเข้าใจพื้นฐานเกี่ยวกับการ Natural Language Processing - NLP และแนวคิดของ machine learning
        มีประสบการณ์ในการทำงานกับ API, JSON หรือ automation pipelines
        หากมีประสบการณ์การใช้งานเครื่องมือหรือเทคโนโลยี เช่น n8n, SQL, Docker หรือ แพลตฟอร์ม Cloud จะได้รับการพิจารณาเป็นพิเศษ
        """

    def extract_resume_pdf(self, pdf_file) -> str:
        """Extract text from PDF resume"""
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception:
            raise HTTPException(status_code=400, detail="Failed to extract text from PDF")

    def llm_analyze(self, resume_text: str) -> Dict:
        """Use Llama LLM to analyze resume"""
        prompt = f""" You are an expert resume analyzer for AI and Data Solution roles.

        Job Description:
        {self.job_description}

        Candidate Resume:
        {resume_text}

        Analyze and provide scores (1-10 score can be float) with reasons:
        - overall_score
        - programming_score
        - ai_ml_score
        - analytical_score
        - tech_experience_score
        - tools_score
        - knowledge_score

        Respond ONLY in JSON format.
        {{
            "overall_score": <1-10>,
            "overall_score_reason": "<reason>",
            "programming_score": <1-10>,
            "programming_score_reason": "<reason>",
            "ai_ml_score": <1-10>,
            "ai_ml_score_reason": "<reason>",
            "analytical_score": <1-10>,
            "analytical_score_reason": "<reason>",
            "tech_experience_score": <1-10>,
            "tech_experience_score_reason": "<reason>",
            "tools_score": <1-10>,
            "tools_score_reason": "<reason>",
            "knowledge_score": <1-10>,
            "knowledge_score_reason": "<reason>"
        }}
        """

        try:
            messages = [{"role": "user", "content": prompt}]

            inputs = tokenizer.apply_chat_template(
                messages,
                add_generation_prompt=True,
                tokenize=True,
                return_dict=True,
                return_tensors="pt"
            )

            if torch.cuda.is_available():
                inputs = {k: v.to(model.device) for k, v in inputs.items()}

            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=1200,
                    temperature=0.3,
                    do_sample=True,
                    pad_token_id=tokenizer.eos_token_id
                )

            response_text = tokenizer.decode(
                outputs[0][inputs["input_ids"].shape[-1]:],
                skip_special_tokens=True
            )

            print(f"Llama Response: {response_text}")

            clean_text = response_text.strip().replace("```json", "").replace("```", "")
            json_match = re.search(r'\{.*\}', clean_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                pattern = r'"(\w+)":\s*("[^"]*"|\d+\.?\d*)'
                matches = re.findall(pattern, json_str)
                cleaned_dict = {}
                for key, value in matches:
                    if re.match(r'^\d+\.?\d*$', value):
                        value = float(value)
                    else:
                        value = value.strip('"')
                    cleaned_dict[key] = value
                return cleaned_dict
            else:
                raise ValueError("No valid JSON found in LLM output")

        except Exception as e:
            print(f"Llama analysis error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Llama analysis failed: {str(e)}")

    def analyze_resume(self, pdf_file) -> AnalysisResult:
        resume_text = self.extract_resume_pdf(pdf_file)
        analysis = self.llm_analyze(resume_text)
        return AnalysisResult(**analysis)


analyzer = ResumeAnalyzer()

@app.post("/analyze-resume", response_model=AnalysisResult)
async def analyze_resume(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    content = await file.read()
    pdf_file = io.BytesIO(content)

    try:
        return analyzer.analyze_resume(pdf_file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/check")
async def check():
    return {"status": "active", "message": "Resume Analyzer API is running"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
