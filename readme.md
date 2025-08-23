# AI-Powered Resume Analyzer

## This project is only analyze according with this Job Description !!!

ตำแหน่ง: AI & Data Solution Intern

Responsibilities
- ทำงานร่วมกับผู้ใช้งานหรือทีมพัฒนาธุรกิจ เพื่อรวบรวมและทำความเข้าใจความต้องการของระบบ
- ออกแบบ พัฒนา และปรับแต่งคำสั่ง prompt เพื่อเพิ่มประสิทธิภาพการทำงานของ AI
- ออกแบบโครงสร้างระบบ กระบวนการทำงาน และการใช้งานของ AI application
- ใช้ Large Language Models (LLMs) เพื่อพัฒนา AI application
- ทดสอบการทำงานและประเมินประสิทธิภาพของ AI application
- ทำงานร่วมกับทีมวิศวกรซอฟต์แวร์อย่างใกล้ชิด เพื่อนำ AI application ไปใช้ในระบบจริง

Qualifications
- ชำนาญในการเขียนโปรแกรมด้วย Python, prompt engineering, และ context engineering
- มีทักษะในการคิดวิเคราะห์และแก้ไขปัญหาได้อย่างดีเยี่ยม
- มีความสนใจในด้าน AI ระบบอัตโนมัติ (automation) และ data-driven solutions
- มีความเข้าใจพื้นฐานเกี่ยวกับการ Natural Language Processing - NLP และแนวคิดของ machine learning
- มีประสบการณ์ในการทำงานกับ API, JSON หรือ automation pipelines
- หากมีประสบการณ์การใช้งานเครื่องมือหรือเทคโนโลยี เช่น n8n, SQL, Docker หรือ แพลตฟอร์ม Cloud จะได้รับการพิจารณาเป็นพิเศษ

## Features

- **AI-Powered Analysis**: Uses Meta's Llama-3.1-8B model for intelligent resume evaluation
- **Comprehensive Scoring**: Provides detailed analysis across 7 key categories:
  - Overall Assessment
  - Programming Skills
  - AI/ML Knowledge
  - Analytical Thinking
  - Technical Experience
  - Tools & Technologies
  - Domain Knowledge
- **GPU Acceleration**: Automatically detects and utilizes GPU when available
- **RESTful API**: Clean FastAPI backend with comprehensive error handling
- **React Frontend**: User-friendly interface for PDF upload and results display
- **PDF Processing**: Robust text extraction from PDF resumes

### Backend Setup

1. Clone the repository:
```bash
git clone https://github.com/icemafree02/Resume-JD-analyzer.git
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the backend:
```bash
python main.py
```

### Frontend Setup (if applicable)

1. Navigate to frontend directory:
```bash
cd resume_frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm start
```

## API Endpoints

### `POST /analyze-resume`
Analyzes uploaded PDF resume and returns comprehensive scoring.

**Request:**
- Content-Type: `multipart/form-data`
- File: PDF resume

**Response:**
```json
{
  "overall_score": 8.5,
  "overall_score_reason": "Strong technical background with relevant AI/ML experience...",
  "programming_score": 9.0,
  "programming_score_reason": "Extensive Python experience with multiple frameworks...",
  "ai_ml_score": 7.5,
  "ai_ml_score_reason": "Good foundation in machine learning concepts...",
  "analytical_score": 8.0,
  "analytical_score_reason": "Demonstrates strong problem-solving abilities...",
  "tech_experience_score": 8.5,
  "tech_experience_score_reason": "Relevant technical projects and internships...",
  "tools_score": 7.0,
  "tools_score_reason": "Familiar with required tools, some gaps in cloud platforms...",
  "knowledge_score": 8.0,
  "knowledge_score_reason": "Strong understanding of AI/ML fundamentals..."
}
```

### `GET /job-description`
Returns the job description used for analysis.

### `GET /check`
Health check endpoint for API status.

## Technical Details

### GPU Optimization
- Automatically detects CUDA availability
- Uses `torch.float16` for GPU (memory efficient)
- Falls back to `torch.float32` on CPU
- Implements `device_map="auto"` for multi-GPU setups

### Error Handling
- PDF format validation
- Text extraction error recovery
- LLM generation failure handling
- JSON parsing error management
- Comprehensive HTTP status codes

### Model Configuration
- **Model**: Meta Llama-3.1-8B-Instruct
- **Temperature**: 0.3 (balanced creativity/consistency)
- **Max Tokens**: 1200
- **Precision**: FP16 (GPU) / FP32 (CPU)

## Performance

- **GPU Processing**: ~2-5 seconds per resume
- **CPU Processing**: ~30-60 seconds per resume
- **Memory Requirements**: 
  - GPU: ~16GB VRAM
  - CPU: ~32GB RAM

## Common Issues

1. **CUDA out of memory**
   - Reduce batch size or use smaller model variant
   - Enable model offloading with `device_map="auto"`

2. **PDF extraction fails**
   - Ensure PDF is not password-protected
   - Check PDF is text-based (not image-only)

3. **Slow CPU inference**
   - Consider using quantized models
   - Implement model caching
   - Use model servers like vLLM for production

⭐ Star this repo if you find it helpful!