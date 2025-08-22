import React, { useState } from "react";

export default function ResumeAnalyzer() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState("No result yet.");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      alert("Please select a PDF file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setResult("Analyzing resume...");

    try {
      const response = await fetch("http://localhost:8000/analyze-resume", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Request failed");
      }

      const data = await response.json();
      setResult(JSON.stringify(data, null, 2));
    } catch (err) {
      setResult("Error: " + err.message);
    }
  };

  return (
    <div style={styles.container}>
      <h1>Resume Job Description Analyzer</h1>

      <div style={styles.contentBox}>
        <div style={styles.leftSide}>
          <div style={styles.jobBox}>
            <h4>ตำแหน่ง: AI & Data Solution Intern</h4>

            <h5>Responsibilities</h5>
            <ul> 
              <li>ทำงานร่วมกับผู้ใช้งานหรือทีมพัฒนาธุรกิจ เพื่อรวบรวมและทำความเข้าใจความต้องการของระบบ</li> 
              <li>ออกแบบ พัฒนา และปรับแต่งคำสั่ง prompt เพื่อเพิ่มประสิทธิภาพการทำงานของ AI</li> 
              <li>ออกแบบโครงสร้างระบบ กระบวนการทำงาน และการใช้งานของ AI application</li> 
              <li>ใช้ Large Language Models (LLMs) เพื่อพัฒนา AI application</li> 
              <li>ทดสอบการทำงานและประเมินประสิทธิภาพของ AI application</li> 
              <li>ทำงานร่วมกับทีมวิศวกรซอฟต์แวร์อย่างใกล้ชิด เพื่อนำ AI application ไปใช้ในระบบจริง</li> 
            </ul> 
            <h5>Qualifications</h5> 
            <ul> 
              <li>ชำนาญในการเขียนโปรแกรมด้วย Python, prompt engineering, และ context engineering</li> 
              <li>มีทักษะในการคิดวิเคราะห์และแก้ไขปัญหาได้อย่างดีเยี่ยม</li> 
              <li>มีความสนใจในด้าน AI ระบบอัตโนมัติ (automation) และ data-driven solutions</li> 
              <li>มีความเข้าใจพื้นฐานเกี่ยวกับ NLP และ machine learning</li> 
              <li>มีประสบการณ์ในการทำงานกับ API, JSON หรือ automation pipelines</li> 
              <li>หากมีประสบการณ์กับ n8n, SQL, Docker หรือ Cloud platforms จะพิจารณาเป็นพิเศษ</li> 
              </ul>
          </div>

          <form onSubmit={handleSubmit} style={styles.form}>
            <label htmlFor="file">Upload your resume (PDF only):</label>
            <input
              type="file"
              id="file"
              name="file"
              accept=".pdf"
              onChange={(e) => setFile(e.target.files[0])}
              required
              style={styles.input}
            />
            <button type="submit" style={styles.button}>
              Analyze Resume
            </button>
          </form>
        </div>

        <div style={styles.rightSide}>
          <h3>Does your resume match the Job Description?</h3>
          <pre style={styles.pre}>{result}</pre>
        </div>
      </div>
    </div>
  );
}

const styles = {
  container: {
    width: "auto",
    height: "auto",
    margin: "100px 20px",
    padding: "25px",
    fontFamily: "Arial, sans-serif",
    fontSize: "18px",

  },
  contentBox: {
    display: "flex",
    gap: "100px",
    alignItems: "flex-start",
  },
  leftSide: {
    flex: 1,
  },
  rightSide: {
    flex: 1,
    maxWidth: "50%",

  },
  jobBox: {
    padding: "20px",
    borderRadius: "10px",
    border: "1px solid black",
    marginBottom: "20px",
    fontSize:"20px"
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "10px",
    marginBottom: "20px",
    fontSize: "25px",
  },
  input: {
    marginTop: "10px",
    marginBottom: "20px",
    fontSize: "16px",
  },
  button: {
    padding: "10px 20px",
    border: "none",
    background: "#007bff",
    color: "#fff",
    borderRadius: "5px",
    cursor: "pointer",
    fontSize: "16px",
  },
  pre: {
    background: "#eee",
    padding: "20px",
    borderRadius: "5px",
    overflowX: "auto",
    whiteSpace: "pre-wrap",
    wordBreak: "break-word",
    fontSize: "20px",
    
  },
};


//////////////////////////////////

