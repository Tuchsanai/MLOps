# %% [markdown]
# # 🚀 LAB: Prompt Optimization using MLflow with Google Gemini
#
# **วิชา:** Machine Learning Operations (MLOps)  
# **เวลา:** 2-3 ชั่วโมง  
# **ระดับ:** Intermediate
#
# ---
#
# ## **ภาพรวมของ Lab (Overview)**
#
# ใน Lab นี้ นักศึกษาจะได้เรียนรู้วิธีการ **ปรับแต่ง Prompt (Prompt Optimization)** อย่างเป็นระบบ
# โดยใช้ **MLflow** ในการติดตาม (Track) และเปรียบเทียบผลลัพธ์จาก Prompt ต่างๆ ที่ส่งไปยัง **Google Gemini API**
#
# ### 🎯 ทำไมต้อง Track Prompt?
#
# เมื่อทำงานกับ LLM (Large Language Model) การเปลี่ยน Prompt เพียงเล็กน้อย
# สามารถทำให้ผลลัพธ์เปลี่ยนแปลงอย่างมาก การบันทึกและติดตาม Prompt อย่างเป็นระบบจะช่วยให้:
#
# 1. **ทำซ้ำได้ (Reproducible)** - สามารถกลับมาใช้ Prompt ที่ดีที่สุดได้
# 2. **เปรียบเทียบได้ (Comparable)** - เห็นความแตกต่างของผลลัพธ์จาก Prompt ต่างๆ
# 3. **วัดผลได้ (Measurable)** - มี Metrics ที่ชัดเจนในการประเมินคุณภาพ
# 4. **ทำงานเป็นทีมได้ (Collaborative)** - แชร์ผลการทดลองกับทีมได้ง่าย
#
# ---

# %% [markdown]
# ## **วัตถุประสงค์การเรียนรู้ (Learning Objectives)**
#
# เมื่อเสร็จสิ้นการปฏิบัติการนี้ นักศึกษาสามารถ:
#
# ### ระดับความรู้และความเข้าใจ (Remember & Understand)
# 1. **อธิบาย** หลักการทำงานของ Google Gemini API และวิธีการเชื่อมต่อเบื้องต้นได้
# 2. **อธิบาย** หลักการของ Prompt Engineering และความสำคัญของการปรับแต่ง Prompt ได้
# 3. **ระบุ** องค์ประกอบสำคัญของ Prompt ที่มีประสิทธิภาพได้
#
# ### ระดับการประยุกต์ใช้ (Apply)
# 4. **เขียน** Prompt ในรูปแบบต่างๆ และส่งคำร้องขอไปยัง Gemini API ได้
# 5. **ใช้งาน** MLflow ในการบันทึก (log) และติดตาม (track) การทดลอง Prompt ต่างๆ ได้
# 6. **กำหนด** Parameters และ Metrics ที่เหมาะสมสำหรับการประเมิน Prompt ได้
#
# ### ระดับการวิเคราะห์และประเมินผล (Analyze & Evaluate)
# 7. **เปรียบเทียบ** ผลลัพธ์จาก Prompt ต่างๆ ผ่าน MLflow UI ได้
# 8. **วิเคราะห์** Metrics เพื่อประเมินคุณภาพของ Prompt แต่ละแบบได้
# 9. **เลือก** Prompt ที่เหมาะสมที่สุดโดยอ้างอิงจากข้อมูลเชิงประจักษ์ได้
#
# ---

# %% [markdown]
# ## **ส่วนที่ 1: ทฤษฎีพื้นฐาน (Theoretical Foundation)**
#
# ### 1.1 Prompt Engineering คืออะไร?
#
# **Prompt Engineering** คือศาสตร์และศิลป์ในการออกแบบคำสั่ง (Prompt) 
# เพื่อให้ได้ผลลัพธ์ที่ต้องการจาก Large Language Model (LLM)
#
# ```
# ┌─────────────────────────────────────────────────────────────┐
# │                    Prompt Engineering Flow                  │
# │                                                             │
# │   [Input Prompt] ──► [LLM Processing] ──► [Output Response] │
# │        │                    │                    │          │
# │        ▼                    ▼                    ▼          │
# │   "วิเคราะห์..."     Model Inference      "ผลการวิเคราะห์..." │
# └─────────────────────────────────────────────────────────────┘
# ```
#
# ### 1.2 องค์ประกอบของ Prompt ที่ดี
#
# | องค์ประกอบ | คำอธิบาย | ตัวอย่าง |
# |-----------|---------|---------|
# | **Context** | บริบทหรือข้อมูลพื้นหลัง | "คุณเป็นผู้เชี่ยวชาญด้านการเงิน..." |
# | **Instruction** | คำสั่งที่ชัดเจน | "วิเคราะห์ข้อมูลต่อไปนี้..." |
# | **Input Data** | ข้อมูลที่ต้องการประมวลผล | "รายได้ Q1: 1M, Q2: 1.2M..." |
# | **Output Format** | รูปแบบผลลัพธ์ที่ต้องการ | "ตอบเป็นรูปแบบ JSON..." |
# | **Constraints** | ข้อจำกัดหรือเงื่อนไข | "ตอบไม่เกิน 100 คำ..." |
#
# ### 1.3 MLflow สำหรับ Prompt Tracking
#
# **MLflow** เป็น Platform สำหรับจัดการ Machine Learning Lifecycle
# ซึ่งสามารถนำมาใช้ติดตาม Prompt Experiments ได้อย่างมีประสิทธิภาพ:
#
# ```
# ┌─────────────────────────────────────────────────────────────┐
# │                     MLflow Components                       │
# │                                                             │
# │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
# │  │   Tracking   │  │   Projects   │  │    Models    │      │
# │  │  (Logging)   │  │ (Packaging)  │  │  (Registry)  │      │
# │  └──────────────┘  └──────────────┘  └──────────────┘      │
# │         │                                                   │
# │         ▼                                                   │
# │  • Parameters (prompt_template, temperature)                │
# │  • Metrics (response_time, token_count, quality_score)      │
# │  • Artifacts (prompts.txt, responses.json)                  │
# └─────────────────────────────────────────────────────────────┘
# ```
#
# ---

# %% [markdown]
# ## **ส่วนที่ 2: การติดตั้งและเตรียมสภาพแวดล้อม (Setup)**
#
# ### 2.1 ติดตั้ง Library ที่จำเป็น
#
# **หมายเหตุสำคัญ:** เราใช้ `google-genai` ซึ่งเป็น package ใหม่ล่าสุด
# แทน `google-generativeai` ที่ถูก deprecated ไปแล้ว

# %%
# ติดตั้ง Libraries ที่จำเป็น
# รันเพียงครั้งเดียว แล้ว Restart Kernel

# !pip install mlflow google-genai python-dotenv

# %% [markdown]
# ### 2.2 Import Libraries

# %%
# Import Libraries ที่จำเป็น
import mlflow
from google import genai
from google.genai import types
import time
import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional

# สำหรับการวิเคราะห์ข้อความ
import re

print("✅ Import Libraries สำเร็จ!")
print(f"📦 MLflow Version: {mlflow.__version__}")

# %% [markdown]
# ### 2.3 Configuration Setup
#
# **สำคัญ:** ก่อนรันต้องตั้งค่า API Key ของ Google Gemini
#
# วิธีการขอ API Key:
# 1. ไปที่ https://aistudio.google.com/app/apikey
# 2. สร้าง API Key ใหม่
# 3. คัดลอก API Key มาใส่ในตัวแปร `GOOGLE_API_KEY`

# %%
# ===========================================
# ⚙️ CONFIGURATION - แก้ไขค่าตามความเหมาะสม
# ===========================================

# Google Gemini API Key
# ⚠️ แก้ไขเป็น API Key ของนักศึกษาเอง
GOOGLE_API_KEY = "YOUR_API_KEY_HERE"

# MLflow Configuration
MLFLOW_TRACKING_URI = "http://localhost:5000"
EXPERIMENT_NAME = "prompt-optimization-lab"

# Model Configuration
MODEL_NAME = "gemini-2.0-flash"

print("✅ Configuration พร้อมใช้งาน")

# %% [markdown]
# ### 2.4 Initialize Services
#
# ขั้นตอนนี้จะเชื่อมต่อกับ Google Gemini API และ MLflow Server
#
# **การใช้งาน google-genai package ใหม่:**
# - ใช้ `genai.Client()` แทน `genai.configure()`
# - API เปลี่ยนเป็น object-oriented มากขึ้น

# %%
# สร้าง Gemini Client (วิธีใหม่)
client = genai.Client(api_key=GOOGLE_API_KEY)

# เชื่อมต่อ MLflow Server
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# สร้างหรือเลือก Experiment
mlflow.set_experiment(EXPERIMENT_NAME)

# แสดงข้อมูล Experiment
experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
print(f"✅ MLflow Experiment: {experiment.name}")
print(f"📁 Experiment ID: {experiment.experiment_id}")
print(f"🔗 MLflow UI: {MLFLOW_TRACKING_URI}")

# %% [markdown]
# ### 2.5 ทดสอบการเชื่อมต่อ Gemini API

# %%
# ทดสอบเรียกใช้งาน Gemini API (วิธีใหม่)
test_response = client.models.generate_content(
    model=MODEL_NAME,
    contents="สวัสดี บอกชื่อของคุณหน่อย"
)

print("✅ การเชื่อมต่อ Gemini API สำเร็จ!")
print(f"📝 Response: {test_response.text[:200]}...")

# %% [markdown]
# ---
# ## **ส่วนที่ 3: Helper Functions สำหรับการทดลอง**
#
# ### 3.1 ทฤษฎี: Metrics สำหรับประเมิน Prompt
#
# การประเมินคุณภาพของ Prompt สามารถวัดได้จากหลาย Metrics:
#
# | Metric | คำอธิบาย | การคำนวณ |
# |--------|---------|---------|
# | **Response Time** | เวลาที่ใช้ในการตอบ | end_time - start_time |
# | **Token Count** | จำนวน Token ที่ใช้ | len(response.text.split()) * 1.3 (ประมาณ) |
# | **Response Length** | ความยาวของคำตอบ | len(response.text) |
# | **Completeness** | ความครบถ้วน | มี element ที่ต้องการหรือไม่ |
# | **Format Compliance** | ตรงตาม Format หรือไม่ | JSON valid? มี header? |

# %%
def call_gemini_with_tracking(
    prompt: str,
    gemini_client: genai.Client,
    model_name: str = MODEL_NAME,
    temperature: float = 0.7,
    max_output_tokens: int = 1024
) -> Dict[str, Any]:
    """
    เรียกใช้ Gemini API และเก็บ Metrics ต่างๆ
    
    Parameters:
    -----------
    prompt : str
        Prompt ที่ต้องการส่ง
    gemini_client : genai.Client
        Client instance ของ Gemini
    model_name : str
        ชื่อ Model ที่ต้องการใช้
    temperature : float
        ค่า Temperature (0.0 - 1.0)
    max_output_tokens : int
        จำนวน Token สูงสุดของ Output
    
    Returns:
    --------
    dict : ผลลัพธ์พร้อม Metrics
    """
    # สร้าง Generation Config
    config = types.GenerateContentConfig(
        temperature=temperature,
        max_output_tokens=max_output_tokens
    )
    
    # บันทึกเวลาเริ่มต้น
    start_time = time.time()
    
    # เรียก API (วิธีใหม่)
    response = gemini_client.models.generate_content(
        model=model_name,
        contents=prompt,
        config=config
    )
    
    # บันทึกเวลาสิ้นสุด
    end_time = time.time()
    
    # คำนวณ Metrics
    response_time = end_time - start_time
    response_text = response.text
    response_length = len(response_text)
    word_count = len(response_text.split())
    estimated_tokens = int(word_count * 1.3)  # ประมาณการ
    
    return {
        "response_text": response_text,
        "response_time": round(response_time, 3),
        "response_length": response_length,
        "word_count": word_count,
        "estimated_tokens": estimated_tokens,
        "timestamp": datetime.now().isoformat()
    }

print("✅ สร้าง Function call_gemini_with_tracking สำเร็จ!")

# %%
def calculate_quality_metrics(
    response_text: str,
    expected_elements: List[str] = None,
    expected_format: str = None
) -> Dict[str, float]:
    """
    คำนวณ Quality Metrics สำหรับ Response
    
    Parameters:
    -----------
    response_text : str
        ข้อความตอบกลับจาก Model
    expected_elements : list, optional
        รายการ Keywords ที่คาดว่าจะมีใน Response
    expected_format : str, optional
        รูปแบบที่คาดหวัง ('json', 'markdown', 'bullet_points')
    
    Returns:
    --------
    dict : Quality Metrics
    """
    metrics = {}
    
    # 1. Element Coverage Score (0-1)
    if expected_elements:
        found_count = sum(
            1 for elem in expected_elements 
            if elem.lower() in response_text.lower()
        )
        metrics["element_coverage"] = round(
            found_count / len(expected_elements), 2
        )
    
    # 2. Format Compliance Score (0-1)
    if expected_format:
        if expected_format == "json":
            try:
                json.loads(response_text)
                metrics["format_compliance"] = 1.0
            except:
                # ลองหา JSON ใน response
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    try:
                        json.loads(json_match.group())
                        metrics["format_compliance"] = 0.8
                    except:
                        metrics["format_compliance"] = 0.0
                else:
                    metrics["format_compliance"] = 0.0
                    
        elif expected_format == "markdown":
            has_headers = bool(re.search(r'^#+\s', response_text, re.MULTILINE))
            has_formatting = any(x in response_text for x in ['**', '*', '`', '```'])
            metrics["format_compliance"] = (has_headers * 0.5) + (has_formatting * 0.5)
            
        elif expected_format == "bullet_points":
            bullet_count = len(re.findall(r'^[\-\*\•]\s', response_text, re.MULTILINE))
            metrics["format_compliance"] = min(1.0, bullet_count / 5)  # คาดหวัง 5+ bullets
    
    # 3. Readability Score (based on sentence structure)
    sentences = re.split(r'[.!?]', response_text)
    sentences = [s.strip() for s in sentences if s.strip()]
    if sentences:
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
        # Optimal: 15-20 words per sentence
        if 10 <= avg_sentence_length <= 25:
            metrics["readability_score"] = 1.0
        elif 5 <= avg_sentence_length <= 35:
            metrics["readability_score"] = 0.7
        else:
            metrics["readability_score"] = 0.4
    
    return metrics

print("✅ สร้าง Function calculate_quality_metrics สำเร็จ!")

# %% [markdown]
# ---
# ## **ส่วนที่ 4: การทดลองที่ 1 - Basic Prompt Comparison**
#
# ### 4.1 ทฤษฎี: Zero-shot vs Few-shot Prompting
#
# ```
# ┌────────────────────────────────────────────────────────────────┐
# │                    Prompting Strategies                        │
# │                                                                │
# │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐│
# │  │   Zero-shot     │  │    One-shot     │  │    Few-shot     ││
# │  │  (ไม่มีตัวอย่าง) │  │ (1 ตัวอย่าง)    │  │ (หลายตัวอย่าง) ││
# │  └─────────────────┘  └─────────────────┘  └─────────────────┘│
# │         │                     │                     │          │
# │         ▼                     ▼                     ▼          │
# │   "จัดหมวดหมู่:       "ตัวอย่าง:            "ตัวอย่าง 1:...   │
# │    ข้อความนี้"        'ดีมาก' → บวก          ตัวอย่าง 2:...   │
# │                       จัดหมวดหมู่:..."        จัดหมวดหมู่:..."  │
# └────────────────────────────────────────────────────────────────┘
# ```
#
# **ข้อดี-ข้อเสีย:**
#
# | Strategy | ข้อดี | ข้อเสีย |
# |----------|------|--------|
# | Zero-shot | ง่าย, เร็ว, ประหยัด Token | อาจไม่เข้าใจ Task |
# | Few-shot | แม่นยำกว่า, เข้าใจ Context | ใช้ Token มากกว่า |

# %% [markdown]
# ### 4.2 กำหนด Task: Sentiment Analysis
#
# เราจะทดลองเปรียบเทียบ Prompt สำหรับการวิเคราะห์ความรู้สึก (Sentiment Analysis)

# %%
# ข้อมูลทดสอบสำหรับ Sentiment Analysis
test_reviews = [
    "สินค้าดีมาก ส่งเร็ว ประทับใจครับ จะกลับมาซื้ออีก",
    "แย่มาก สินค้าไม่ตรงปก รอนานมาก ไม่แนะนำ",
    "พอใช้ได้ ราคาถูก แต่คุณภาพก็งั้นๆ",
    "ชอบมากค่ะ สีสวย ใส่สบาย คุ้มราคา",
    "ผิดหวังมาก สั่งไซส์ L มาเป็น M ติดต่อร้านก็ไม่ตอบ"
]

# Expected Labels สำหรับการประเมิน
expected_sentiments = ["positive", "negative", "neutral", "positive", "negative"]

print("📋 ข้อมูลทดสอบ:")
for i, review in enumerate(test_reviews):
    print(f"  {i+1}. {review[:50]}... → {expected_sentiments[i]}")

# %% [markdown]
# ### 4.3 Prompt Variations
#
# เราจะสร้าง 3 รูปแบบ Prompt ที่แตกต่างกัน:

# %%
# Prompt 1: Zero-shot Simple
prompt_zero_shot = """วิเคราะห์ความรู้สึกของข้อความต่อไปนี้:

ข้อความ: "{text}"

ตอบเพียง: positive, negative, หรือ neutral"""

# Prompt 2: Zero-shot with Context
prompt_zero_shot_context = """คุณเป็นผู้เชี่ยวชาญด้านการวิเคราะห์ความรู้สึกจากข้อความรีวิวสินค้า

วิเคราะห์ความรู้สึกของรีวิวต่อไปนี้:
- positive: แสดงความพอใจ ชื่นชม แนะนำ
- negative: แสดงความไม่พอใจ ตำหนิ ไม่แนะนำ  
- neutral: ไม่มีความรู้สึกชัดเจน หรือมีทั้งบวกและลบ

ข้อความ: "{text}"

ตอบเป็นคำเดียว: positive, negative, หรือ neutral"""

# Prompt 3: Few-shot with Examples
prompt_few_shot = """วิเคราะห์ความรู้สึกจากรีวิวสินค้า

ตัวอย่าง:
1. "สินค้าสวยมาก ชอบเลย" → positive
2. "ห่วยแตก ไม่ซื้ออีกแล้ว" → negative
3. "ก็โอเคนะ ไม่ได้แย่แต่ก็ไม่ได้ดีมาก" → neutral

ข้อความ: "{text}"

ตอบ:"""

# เก็บ Prompts ทั้งหมดใน Dictionary
prompt_variations = {
    "zero_shot_simple": prompt_zero_shot,
    "zero_shot_context": prompt_zero_shot_context,
    "few_shot": prompt_few_shot
}

print("📝 สร้าง Prompt Variations สำเร็จ!")
for name in prompt_variations.keys():
    print(f"  • {name}")

# %% [markdown]
# ### 4.4 รันการทดลองและบันทึกด้วย MLflow

# %%
def run_sentiment_experiment(
    prompt_name: str,
    prompt_template: str,
    test_texts: List[str],
    expected_labels: List[str],
    gemini_client: genai.Client,
    model_name: str = MODEL_NAME,
    temperature: float = 0.3
) -> Dict[str, Any]:
    """
    รันการทดลอง Sentiment Analysis และบันทึกผลด้วย MLflow
    """
    
    # เริ่ม MLflow Run
    with mlflow.start_run(run_name=f"sentiment_{prompt_name}"):
        
        # Log Parameters
        mlflow.log_param("prompt_name", prompt_name)
        mlflow.log_param("prompt_template", prompt_template[:500])  # จำกัดความยาว
        mlflow.log_param("temperature", temperature)
        mlflow.log_param("model", model_name)
        mlflow.log_param("num_samples", len(test_texts))
        
        # เก็บผลลัพธ์
        results = []
        total_time = 0
        correct_count = 0
        
        print(f"\n🔄 Running: {prompt_name}")
        print("-" * 50)
        
        for i, (text, expected) in enumerate(zip(test_texts, expected_labels)):
            # สร้าง Prompt
            full_prompt = prompt_template.format(text=text)
            
            # เรียก API
            response_data = call_gemini_with_tracking(
                full_prompt,
                gemini_client,
                model_name=model_name,
                temperature=temperature,
                max_output_tokens=50
            )
            
            # ดึงผลลัพธ์
            predicted = response_data["response_text"].strip().lower()
            
            # ตรวจสอบความถูกต้อง
            is_correct = expected.lower() in predicted
            if is_correct:
                correct_count += 1
            
            # เก็บผลลัพธ์
            results.append({
                "input": text[:50] + "...",
                "expected": expected,
                "predicted": predicted[:20],
                "correct": is_correct,
                "response_time": response_data["response_time"]
            })
            
            total_time += response_data["response_time"]
            
            # แสดงผล
            status = "✅" if is_correct else "❌"
            print(f"  {i+1}. {status} Expected: {expected}, Got: {predicted[:15]}")
        
        # คำนวณ Metrics รวม
        accuracy = correct_count / len(test_texts)
        avg_response_time = total_time / len(test_texts)
        
        # Log Metrics
        mlflow.log_metric("accuracy", round(accuracy, 3))
        mlflow.log_metric("avg_response_time", round(avg_response_time, 3))
        mlflow.log_metric("total_time", round(total_time, 3))
        mlflow.log_metric("correct_count", correct_count)
        
        # Log Artifacts (บันทึกผลลัพธ์เป็นไฟล์)
        results_filename = f"results_{prompt_name}.json"
        with open(results_filename, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        mlflow.log_artifact(results_filename)
        os.remove(results_filename)  # ลบไฟล์ temp
        
        print("-" * 50)
        print(f"📊 Results: Accuracy = {accuracy:.1%}, Avg Time = {avg_response_time:.2f}s")
        
        return {
            "prompt_name": prompt_name,
            "accuracy": accuracy,
            "avg_response_time": avg_response_time,
            "results": results
        }

print("✅ สร้าง Function run_sentiment_experiment สำเร็จ!")

# %% [markdown]
# ### 4.5 รันการทดลองทั้งหมด

# %%
# รันการทดลองสำหรับทุก Prompt Variation
experiment_results = []

for prompt_name, prompt_template in prompt_variations.items():
    result = run_sentiment_experiment(
        prompt_name=prompt_name,
        prompt_template=prompt_template,
        test_texts=test_reviews,
        expected_labels=expected_sentiments,
        gemini_client=client,
        model_name=MODEL_NAME,
        temperature=0.3
    )
    experiment_results.append(result)
    
    # หยุดพักเล็กน้อยเพื่อไม่ให้ถูก Rate Limit
    time.sleep(1)

print("\n" + "=" * 50)
print("🏆 สรุปผลการทดลอง:")
print("=" * 50)

# %% [markdown]
# ### 4.6 เปรียบเทียบผลลัพธ์

# %%
# สร้างตารางเปรียบเทียบ
print("\n📊 Comparison Table:")
print("-" * 60)
print(f"{'Prompt Name':<25} {'Accuracy':<12} {'Avg Time (s)':<12}")
print("-" * 60)

best_accuracy = 0
best_prompt = ""

for result in experiment_results:
    accuracy_pct = f"{result['accuracy']:.1%}"
    print(f"{result['prompt_name']:<25} {accuracy_pct:<12} {result['avg_response_time']:<12.3f}")
    
    if result['accuracy'] > best_accuracy:
        best_accuracy = result['accuracy']
        best_prompt = result['prompt_name']

print("-" * 60)
print(f"\n🥇 Best Prompt: {best_prompt} (Accuracy: {best_accuracy:.1%})")

# %% [markdown]
# ### 🔍 ไปดูผลลัพธ์ใน MLflow UI
#
# เปิด Browser แล้วไปที่: **http://localhost:5000**
#
# 1. เลือก Experiment: `prompt-optimization-lab`
# 2. ดู Runs ทั้ง 3 และเปรียบเทียบ Metrics
# 3. กดปุ่ม "Compare" เพื่อเปรียบเทียบแบบ side-by-side
#
# ---

# %% [markdown]
# ## **ส่วนที่ 5: การทดลองที่ 2 - Temperature Optimization**
#
# ### 5.1 ทฤษฎี: Temperature Parameter
#
# **Temperature** คือ Parameter ที่ควบคุมความ "สุ่ม" ของ Output:
#
# ```
# ┌─────────────────────────────────────────────────────────────┐
# │                  Temperature Effect                         │
# │                                                             │
# │   Temperature = 0.0          Temperature = 1.0              │
# │   ┌─────────────────┐        ┌─────────────────┐           │
# │   │  Deterministic  │        │    Creative     │           │
# │   │   Consistent    │   ──►  │    Diverse      │           │
# │   │   Predictable   │        │   Unpredictable │           │
# │   └─────────────────┘        └─────────────────┘           │
# │                                                             │
# │   Use cases:                 Use cases:                     │
# │   • Classification          • Creative writing              │
# │   • Extraction              • Brainstorming                 │
# │   • Summarization           • Story generation              │
# └─────────────────────────────────────────────────────────────┘
# ```
#
# | Temperature | ลักษณะ Output | เหมาะกับงาน |
# |-------------|--------------|------------|
# | 0.0 - 0.3 | แม่นยำ คงที่ | Classification, Extraction |
# | 0.4 - 0.7 | สมดุล | General Q&A, Summarization |
# | 0.8 - 1.0 | สร้างสรรค์ หลากหลาย | Creative Writing |

# %%
# กำหนด Task: Creative Text Generation
creative_prompt = """เขียนโฆษณาสั้นๆ สำหรับร้านกาแฟชื่อ "Morning Brew"
- ความยาว 2-3 ประโยค
- เน้นบรรยากาศอบอุ่น และกาแฟรสเข้ม
- ใช้ภาษาที่ดึงดูดใจลูกค้า"""

# Temperature values ที่จะทดสอบ
temperatures = [0.1, 0.5, 0.7, 0.9]

print("🎯 Task: Creative Text Generation")
print(f"📝 Prompt: {creative_prompt[:100]}...")

# %% [markdown]
# ### 5.2 รันการทดลอง Temperature

# %%
def run_temperature_experiment(
    prompt: str,
    temperatures: List[float],
    gemini_client: genai.Client,
    model_name: str = MODEL_NAME,
    runs_per_temp: int = 3
) -> List[Dict]:
    """
    ทดสอบผลกระทบของ Temperature ต่อ Output
    """
    all_results = []
    
    for temp in temperatures:
        print(f"\n🌡️ Testing Temperature = {temp}")
        print("-" * 50)
        
        with mlflow.start_run(run_name=f"temp_{temp}"):
            
            # Log Parameters
            mlflow.log_param("temperature", temp)
            mlflow.log_param("prompt", prompt[:300])
            mlflow.log_param("runs_per_temp", runs_per_temp)
            
            responses = []
            total_time = 0
            
            for run_num in range(runs_per_temp):
                # เรียก API
                response_data = call_gemini_with_tracking(
                    prompt,
                    gemini_client,
                    model_name=model_name,
                    temperature=temp,
                    max_output_tokens=200
                )
                
                responses.append(response_data["response_text"])
                total_time += response_data["response_time"]
                
                print(f"  Run {run_num + 1}: {response_data['response_text'][:80]}...")
                
                # หยุดพักเล็กน้อย
                time.sleep(0.5)
            
            # คำนวณ Diversity Score (ความหลากหลายของ Output)
            # ใช้ Jaccard Similarity
            def jaccard_similarity(text1, text2):
                set1 = set(text1.lower().split())
                set2 = set(text2.lower().split())
                intersection = len(set1.intersection(set2))
                union = len(set1.union(set2))
                return intersection / union if union > 0 else 0
            
            # คำนวณความคล้ายคลึงเฉลี่ย
            similarities = []
            for i in range(len(responses)):
                for j in range(i + 1, len(responses)):
                    sim = jaccard_similarity(responses[i], responses[j])
                    similarities.append(sim)
            
            avg_similarity = sum(similarities) / len(similarities) if similarities else 1
            diversity_score = 1 - avg_similarity  # Diversity = 1 - Similarity
            
            # Log Metrics
            mlflow.log_metric("diversity_score", round(diversity_score, 3))
            mlflow.log_metric("avg_response_time", round(total_time / runs_per_temp, 3))
            mlflow.log_metric("avg_similarity", round(avg_similarity, 3))
            
            # เก็บผลลัพธ์
            result = {
                "temperature": temp,
                "diversity_score": round(diversity_score, 3),
                "avg_similarity": round(avg_similarity, 3),
                "responses": responses
            }
            all_results.append(result)
            
            print(f"  📊 Diversity Score: {diversity_score:.3f}")
    
    return all_results

# รันการทดลอง
temp_results = run_temperature_experiment(
    prompt=creative_prompt,
    temperatures=temperatures,
    gemini_client=client,
    model_name=MODEL_NAME,
    runs_per_temp=3
)

# %% [markdown]
# ### 5.3 วิเคราะห์ผลการทดลอง Temperature

# %%
print("\n" + "=" * 60)
print("📊 Temperature Experiment Results")
print("=" * 60)
print(f"{'Temperature':<15} {'Diversity Score':<18} {'Avg Similarity':<15}")
print("-" * 60)

for result in temp_results:
    print(f"{result['temperature']:<15} {result['diversity_score']:<18.3f} {result['avg_similarity']:<15.3f}")

print("-" * 60)
print("\n💡 Insights:")
print("  • Low Temperature (0.1-0.3): Output คล้ายกัน เหมาะกับงานที่ต้องการความแม่นยำ")
print("  • High Temperature (0.7-0.9): Output หลากหลาย เหมาะกับงานสร้างสรรค์")

# %% [markdown]
# ---
# ## **ส่วนที่ 6: การทดลองที่ 3 - System Prompt Optimization**
#
# ### 6.1 ทฤษฎี: Role-based Prompting
#
# การกำหนด Role ให้กับ LLM สามารถเปลี่ยนสไตล์และมุมมองของคำตอบได้:
#
# ```
# ┌─────────────────────────────────────────────────────────────┐
# │                    Role-based Prompting                     │
# │                                                             │
# │   "คุณเป็นผู้เชี่ยวชาญด้าน..."                              │
# │                │                                            │
# │                ▼                                            │
# │   ┌─────────────────────────────────────────────────────┐  │
# │   │  • Expert Vocabulary                                 │  │
# │   │  • Domain-specific Knowledge                        │  │
# │   │  • Professional Tone                                │  │
# │   │  • Relevant Examples                                │  │
# │   └─────────────────────────────────────────────────────┘  │
# └─────────────────────────────────────────────────────────────┘
# ```

# %%
# กำหนด Task: Technical Explanation
task_question = "อธิบายว่า Machine Learning คืออะไร"

# System Prompts ต่างๆ
system_prompts = {
    "no_role": {
        "description": "ไม่กำหนด Role",
        "prompt": f"{task_question}\n\nอธิบายสั้นๆ ใน 3-4 ประโยค"
    },
    "teacher": {
        "description": "เป็นครูสอนเด็ก",
        "prompt": f"""คุณเป็นครูสอนวิทยาศาสตร์ที่อธิบายเรื่องยากให้เข้าใจง่าย
ใช้ภาษาที่เด็กอายุ 10 ขวบเข้าใจได้

{task_question}

อธิบายสั้นๆ ใน 3-4 ประโยค ใช้ตัวอย่างที่เด็กเข้าใจได้"""
    },
    "professor": {
        "description": "เป็นศาสตราจารย์",
        "prompt": f"""คุณเป็นศาสตราจารย์ด้าน Computer Science ที่มีความเชี่ยวชาญด้าน AI
ใช้ภาษาทางวิชาการที่แม่นยำ

{task_question}

อธิบายสั้นๆ ใน 3-4 ประโยค เน้นความถูกต้องทางเทคนิค"""
    },
    "entrepreneur": {
        "description": "เป็นนักธุรกิจ",
        "prompt": f"""คุณเป็น CEO ของบริษัท Tech Startup ที่ประสบความสำเร็จ
เน้นมุมมองด้านธุรกิจและการนำไปใช้จริง

{task_question}

อธิบายสั้นๆ ใน 3-4 ประโยค เน้นประโยชน์ทางธุรกิจ"""
    }
}

print("🎭 System Prompts ที่จะทดสอบ:")
for name, config in system_prompts.items():
    print(f"  • {name}: {config['description']}")

# %% [markdown]
# ### 6.2 รันการทดลอง System Prompts

# %%
def run_system_prompt_experiment(
    system_prompts: Dict[str, Dict],
    gemini_client: genai.Client,
    model_name: str = MODEL_NAME,
    temperature: float = 0.5
) -> List[Dict]:
    """
    ทดสอบ System Prompts ต่างๆ
    """
    results = []
    
    for role_name, config in system_prompts.items():
        print(f"\n🎭 Testing Role: {role_name} - {config['description']}")
        print("-" * 50)
        
        with mlflow.start_run(run_name=f"role_{role_name}"):
            
            # Log Parameters
            mlflow.log_param("role_name", role_name)
            mlflow.log_param("role_description", config["description"])
            mlflow.log_param("prompt", config["prompt"][:300])
            mlflow.log_param("temperature", temperature)
            
            # เรียก API
            response_data = call_gemini_with_tracking(
                config["prompt"],
                gemini_client,
                model_name=model_name,
                temperature=temperature,
                max_output_tokens=300
            )
            
            response_text = response_data["response_text"]
            
            # วิเคราะห์ Response
            word_count = len(response_text.split())
            
            # ตรวจสอบว่ามีคำศัพท์เฉพาะทางหรือไม่
            technical_terms = ["algorithm", "data", "model", "training", "neural", 
                            "อัลกอริทึม", "ข้อมูล", "โมเดล", "เรียนรู้", "ฝึก"]
            technical_count = sum(1 for term in technical_terms 
                                if term.lower() in response_text.lower())
            
            # Log Metrics
            mlflow.log_metric("response_time", response_data["response_time"])
            mlflow.log_metric("word_count", word_count)
            mlflow.log_metric("technical_terms_count", technical_count)
            mlflow.log_metric("response_length", response_data["response_length"])
            
            # Log Response as Artifact
            response_filename = f"response_{role_name}.txt"
            with open(response_filename, "w", encoding="utf-8") as f:
                f.write(f"Role: {config['description']}\n")
                f.write(f"Prompt:\n{config['prompt']}\n\n")
                f.write(f"Response:\n{response_text}")
            mlflow.log_artifact(response_filename)
            os.remove(response_filename)
            
            print(f"📝 Response:\n{response_text}\n")
            print(f"📊 Word Count: {word_count}, Technical Terms: {technical_count}")
            
            results.append({
                "role_name": role_name,
                "description": config["description"],
                "response": response_text,
                "word_count": word_count,
                "technical_count": technical_count,
                "response_time": response_data["response_time"]
            })
        
        time.sleep(1)
    
    return results

# รันการทดลอง
role_results = run_system_prompt_experiment(
    system_prompts=system_prompts,
    gemini_client=client,
    model_name=MODEL_NAME,
    temperature=0.5
)

# %% [markdown]
# ### 6.3 วิเคราะห์ผลการทดลอง System Prompts

# %%
print("\n" + "=" * 70)
print("📊 System Prompt Experiment Results")
print("=" * 70)
print(f"{'Role':<15} {'Description':<20} {'Words':<10} {'Tech Terms':<12} {'Time(s)':<10}")
print("-" * 70)

for result in role_results:
    print(f"{result['role_name']:<15} {result['description']:<20} "
          f"{result['word_count']:<10} {result['technical_count']:<12} "
          f"{result['response_time']:<10.3f}")

print("-" * 70)
print("\n💡 Insights:")
print("  • Teacher Role: ใช้ภาษาง่าย มีตัวอย่างที่เข้าใจได้")
print("  • Professor Role: ใช้ศัพท์เทคนิคมากกว่า เนื้อหาเชิงวิชาการ")
print("  • Entrepreneur Role: เน้นประโยชน์และการนำไปใช้งานจริง")

# %% [markdown]
# ---
# ## **ส่วนที่ 7: การทดลองที่ 4 - Output Format Optimization**
#
# ### 7.1 ทฤษฎี: Output Format Control
#
# การกำหนดรูปแบบ Output ช่วยให้ได้ข้อมูลที่พร้อมใช้งานทันที:
#
# ```
# ┌─────────────────────────────────────────────────────────────┐
# │                   Output Format Types                       │
# │                                                             │
# │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
# │  │ Plain   │  │  JSON   │  │Markdown │  │  Table  │        │
# │  │  Text   │  │         │  │         │  │         │        │
# │  └─────────┘  └─────────┘  └─────────┘  └─────────┘        │
# │       │            │            │            │              │
# │       ▼            ▼            ▼            ▼              │
# │   "สรุป..."    {"title":    "# หัวข้อ    | Col1 | Col2 |  │
# │                "xxx"}      **bold**"    |------|------|   │
# └─────────────────────────────────────────────────────────────┘
# ```

# %%
# Task: Product Analysis
product_info = """
ชื่อสินค้า: iPhone 15 Pro Max
ราคา: 48,900 บาท
จุดเด่น: ชิป A17 Pro, กล้อง 48MP, USB-C, Titanium Design
จุดด้อย: ราคาสูง, น้ำหนักเพิ่มขึ้นเล็กน้อย
"""

# Output Format Prompts
format_prompts = {
    "plain_text": {
        "description": "ข้อความธรรมดา",
        "prompt": f"""วิเคราะห์สินค้าต่อไปนี้:
{product_info}

สรุปเป็นข้อความ 3-4 ประโยค"""
    },
    
    "json_format": {
        "description": "JSON Format",
        "prompt": f"""วิเคราะห์สินค้าต่อไปนี้:
{product_info}

ตอบเป็น JSON format ตามโครงสร้างนี้:
{{
  "product_name": "...",
  "price": "...",
  "pros": ["...", "..."],
  "cons": ["...", "..."],
  "recommendation": "...",
  "rating": 1-5
}}

ตอบเฉพาะ JSON เท่านั้น ไม่ต้องมีข้อความอื่น"""
    },
    
    "markdown_format": {
        "description": "Markdown Format",
        "prompt": f"""วิเคราะห์สินค้าต่อไปนี้:
{product_info}

สรุปเป็น Markdown format ดังนี้:
## [ชื่อสินค้า]
**ราคา:** ...
### ข้อดี
- ...
### ข้อเสีย
- ...
### สรุป
..."""
    },
    
    "bullet_points": {
        "description": "Bullet Points",
        "prompt": f"""วิเคราะห์สินค้าต่อไปนี้:
{product_info}

สรุปเป็น bullet points:
• ชื่อสินค้า: ...
• ราคา: ...
• ข้อดี: ...
• ข้อเสีย: ...
• คำแนะนำ: ..."""
    }
}

print("📋 Output Formats ที่จะทดสอบ:")
for name, config in format_prompts.items():
    print(f"  • {name}: {config['description']}")

# %% [markdown]
# ### 7.2 รันการทดลอง Output Format

# %%
def run_format_experiment(
    format_prompts: Dict[str, Dict],
    gemini_client: genai.Client,
    model_name: str = MODEL_NAME,
    temperature: float = 0.3
) -> List[Dict]:
    """
    ทดสอบ Output Formats ต่างๆ
    """
    results = []
    
    for format_name, config in format_prompts.items():
        print(f"\n📄 Testing Format: {format_name} - {config['description']}")
        print("-" * 50)
        
        with mlflow.start_run(run_name=f"format_{format_name}"):
            
            # Log Parameters
            mlflow.log_param("format_name", format_name)
            mlflow.log_param("format_description", config["description"])
            mlflow.log_param("temperature", temperature)
            
            # เรียก API
            response_data = call_gemini_with_tracking(
                config["prompt"],
                gemini_client,
                model_name=model_name,
                temperature=temperature,
                max_output_tokens=500
            )
            
            response_text = response_data["response_text"]
            
            # คำนวณ Quality Metrics
            expected_format = format_name.replace("_format", "").replace("_points", "_points")
            if format_name == "json_format":
                expected_format = "json"
            elif format_name == "markdown_format":
                expected_format = "markdown"
            elif format_name == "bullet_points":
                expected_format = "bullet_points"
            else:
                expected_format = None
            
            quality_metrics = calculate_quality_metrics(
                response_text,
                expected_elements=["iPhone", "48,900", "A17", "กล้อง"],
                expected_format=expected_format
            )
            
            # Log Metrics
            mlflow.log_metric("response_time", response_data["response_time"])
            mlflow.log_metric("response_length", response_data["response_length"])
            
            for metric_name, metric_value in quality_metrics.items():
                mlflow.log_metric(metric_name, metric_value)
            
            print(f"📝 Response:\n{response_text[:300]}...\n")
            print(f"📊 Quality Metrics: {quality_metrics}")
            
            results.append({
                "format_name": format_name,
                "description": config["description"],
                "response": response_text,
                "response_time": response_data["response_time"],
                **quality_metrics
            })
        
        time.sleep(1)
    
    return results

# รันการทดลอง
format_results = run_format_experiment(
    format_prompts=format_prompts,
    gemini_client=client,
    model_name=MODEL_NAME,
    temperature=0.3
)

# %% [markdown]
# ### 7.3 วิเคราะห์ผลการทดลอง Output Format

# %%
print("\n" + "=" * 80)
print("📊 Output Format Experiment Results")
print("=" * 80)
print(f"{'Format':<18} {'Description':<18} {'Time(s)':<10} {'Coverage':<12} {'Format OK':<12}")
print("-" * 80)

for result in format_results:
    coverage = result.get('element_coverage', 'N/A')
    format_ok = result.get('format_compliance', 'N/A')
    
    if isinstance(coverage, float):
        coverage = f"{coverage:.2f}"
    if isinstance(format_ok, float):
        format_ok = f"{format_ok:.2f}"
    
    print(f"{result['format_name']:<18} {result['description']:<18} "
          f"{result['response_time']:<10.3f} {coverage:<12} {format_ok:<12}")

print("-" * 80)

# %% [markdown]
# ---
# ## **ส่วนที่ 8: การทดลองที่ 5 - Chain-of-Thought Prompting**
#
# ### 8.1 ทฤษฎี: Chain-of-Thought (CoT)
#
# **Chain-of-Thought** คือเทคนิคที่ให้ Model แสดงขั้นตอนการคิดก่อนให้คำตอบ:
#
# ```
# ┌─────────────────────────────────────────────────────────────┐
# │              Chain-of-Thought Prompting                     │
# │                                                             │
# │   Direct Answer          vs    Chain-of-Thought             │
# │   ┌───────────────┐           ┌───────────────┐            │
# │   │ Q: 15+27=?    │           │ Q: 15+27=?    │            │
# │   │               │           │               │            │
# │   │ A: 42         │           │ A: Let me     │            │
# │   └───────────────┘           │ think step    │            │
# │                               │ by step...    │            │
# │                               │ 15+27         │            │
# │                               │ = 15+20+7     │            │
# │                               │ = 35+7        │            │
# │                               │ = 42          │            │
# │                               └───────────────┘            │
# └─────────────────────────────────────────────────────────────┘
# ```
#
# **ประโยชน์ของ CoT:**
# - ลดข้อผิดพลาดในการคำนวณ
# - เข้าใจเหตุผลของคำตอบ
# - แก้ปัญหาที่ซับซ้อนได้ดีขึ้น

# %%
# Task: Math Word Problem
math_problems = [
    {
        "question": "ร้านค้าขายเสื้อผ้าราคาตัวละ 250 บาท ถ้าลูกค้าซื้อ 3 ตัวขึ้นไปจะได้ส่วนลด 10% ลูกค้าคนหนึ่งซื้อเสื้อ 5 ตัว ต้องจ่ายเงินเท่าไหร่?",
        "answer": 1125
    },
    {
        "question": "รถไฟขบวนหนึ่งออกจากสถานี A เวลา 9:00 น. ด้วยความเร็ว 60 กม./ชม. อีก 30 นาทีต่อมา รถไฟอีกขบวนออกจากสถานี B ซึ่งอยู่ห่างจาก A 150 กม. มุ่งหน้ามาหากัน ด้วยความเร็ว 90 กม./ชม. รถสองขบวนจะพบกันเวลาใด?",
        "answer": "10:00"
    },
    {
        "question": "มีเงิน 1,000 บาท ฝากธนาคารได้ดอกเบี้ย 3% ต่อปี ถ้าฝากครบ 2 ปี (คิดดอกเบี้ยทบต้น) จะได้เงินรวมเท่าไหร่?",
        "answer": 1060.9
    }
]

# Prompt Variants
cot_prompts = {
    "direct": {
        "description": "ตอบตรงๆ",
        "template": """ตอบคำถามต่อไปนี้:

{question}

ตอบเป็นตัวเลขหรือเวลาเท่านั้น"""
    },
    
    "cot_basic": {
        "description": "CoT พื้นฐาน",
        "template": """ตอบคำถามต่อไปนี้ โดยแสดงขั้นตอนการคิด:

{question}

คิดทีละขั้นตอน แล้วให้คำตอบสุดท้าย"""
    },
    
    "cot_structured": {
        "description": "CoT แบบมีโครงสร้าง",
        "template": """ตอบคำถามต่อไปนี้ โดยใช้โครงสร้างดังนี้:

{question}

1. ข้อมูลที่มี: [ระบุข้อมูลสำคัญ]
2. สิ่งที่ต้องหา: [ระบุคำถาม]
3. วิธีการแก้: [อธิบายทีละขั้นตอน]
4. การคำนวณ: [แสดงการคำนวณ]
5. คำตอบ: [ตัวเลขหรือเวลา]"""
    }
}

print("📐 Math Problems ที่จะทดสอบ:")
for i, prob in enumerate(math_problems):
    print(f"  {i+1}. {prob['question'][:50]}...")

# %% [markdown]
# ### 8.2 รันการทดลอง Chain-of-Thought

# %%
def run_cot_experiment(
    problems: List[Dict],
    cot_prompts: Dict[str, Dict],
    gemini_client: genai.Client,
    model_name: str = MODEL_NAME,
    temperature: float = 0.2
) -> Dict[str, List]:
    """
    ทดสอบ Chain-of-Thought Prompting
    """
    all_results = {}
    
    for prompt_name, prompt_config in cot_prompts.items():
        print(f"\n🧠 Testing: {prompt_name} - {prompt_config['description']}")
        print("=" * 60)
        
        results = []
        correct_count = 0
        
        with mlflow.start_run(run_name=f"cot_{prompt_name}"):
            
            # Log Parameters
            mlflow.log_param("cot_type", prompt_name)
            mlflow.log_param("description", prompt_config["description"])
            mlflow.log_param("temperature", temperature)
            mlflow.log_param("num_problems", len(problems))
            
            for i, problem in enumerate(problems):
                # สร้าง Full Prompt
                full_prompt = prompt_config["template"].format(
                    question=problem["question"]
                )
                
                # เรียก API
                response_data = call_gemini_with_tracking(
                    full_prompt,
                    gemini_client,
                    model_name=model_name,
                    temperature=temperature,
                    max_output_tokens=500
                )
                
                response_text = response_data["response_text"]
                
                # ตรวจสอบความถูกต้อง (อย่างง่าย)
                expected = str(problem["answer"])
                is_correct = expected in response_text
                if is_correct:
                    correct_count += 1
                
                status = "✅" if is_correct else "❌"
                print(f"\n  Problem {i+1}: {status}")
                print(f"  Expected: {expected}")
                print(f"  Response: {response_text[:200]}...")
                
                results.append({
                    "problem_num": i + 1,
                    "expected": expected,
                    "response": response_text,
                    "correct": is_correct,
                    "response_time": response_data["response_time"]
                })
                
                time.sleep(0.5)
            
            # คำนวณ Accuracy
            accuracy = correct_count / len(problems)
            avg_time = sum(r["response_time"] for r in results) / len(results)
            
            # Log Metrics
            mlflow.log_metric("accuracy", round(accuracy, 3))
            mlflow.log_metric("correct_count", correct_count)
            mlflow.log_metric("avg_response_time", round(avg_time, 3))
            
            print(f"\n📊 {prompt_name}: Accuracy = {accuracy:.1%}")
            
            all_results[prompt_name] = {
                "accuracy": accuracy,
                "correct_count": correct_count,
                "avg_time": avg_time,
                "results": results
            }
    
    return all_results

# รันการทดลอง
cot_results = run_cot_experiment(
    problems=math_problems,
    cot_prompts=cot_prompts,
    gemini_client=client,
    model_name=MODEL_NAME,
    temperature=0.2
)

# %% [markdown]
# ### 8.3 วิเคราะห์ผลการทดลอง CoT

# %%
print("\n" + "=" * 60)
print("📊 Chain-of-Thought Experiment Results")
print("=" * 60)
print(f"{'Method':<20} {'Accuracy':<15} {'Correct':<12} {'Avg Time(s)':<12}")
print("-" * 60)

for method_name, result in cot_results.items():
    print(f"{method_name:<20} {result['accuracy']:.1%}{'':<10} "
          f"{result['correct_count']}/{len(math_problems):<9} "
          f"{result['avg_time']:.3f}")

print("-" * 60)
print("\n💡 Insights:")
print("  • Direct prompting อาจพลาดในปัญหาที่ซับซ้อน")
print("  • CoT ช่วยให้ Model คิดอย่างเป็นระบบ")
print("  • Structured CoT ช่วยจัดการข้อมูลได้ดี")

# %% [markdown]
# ---
# ## **ส่วนที่ 9: Best Practices และ Tips**
#
# ### 9.1 สรุป Best Practices สำหรับ Prompt Optimization
#
# จากการทดลองทั้งหมด เราได้เรียนรู้:
#
# | หัวข้อ | Best Practice |
# |-------|--------------|
# | **Clarity** | เขียน Prompt ให้ชัดเจน ระบุสิ่งที่ต้องการ |
# | **Context** | ให้บริบทและ Role ที่เหมาะสม |
# | **Examples** | ใช้ Few-shot เมื่อ Task ซับซ้อน |
# | **Format** | กำหนด Output Format ที่ชัดเจน |
# | **Temperature** | ใช้ค่าต่ำสำหรับงานแม่นยำ ค่าสูงสำหรับงานสร้างสรรค์ |
# | **CoT** | ใช้ Chain-of-Thought สำหรับปัญหาที่ต้องการเหตุผล |

# %%
# แสดงสรุปการทดลองทั้งหมดจาก MLflow
experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
runs = mlflow.search_runs(experiment_ids=[experiment.experiment_id])

print("📊 สรุป Runs ทั้งหมดใน Experiment:")
print("-" * 80)
print(f"จำนวน Runs ทั้งหมด: {len(runs)}")

if not runs.empty:
    # แสดง Columns ที่สำคัญ
    important_cols = ['run_id', 'status', 'start_time']
    metric_cols = [col for col in runs.columns if col.startswith('metrics.')]
    param_cols = [col for col in runs.columns if col.startswith('params.')]
    
    print(f"\nMetrics ที่บันทึก: {[col.replace('metrics.', '') for col in metric_cols[:5]]}")
    print(f"Parameters ที่บันทึก: {[col.replace('params.', '') for col in param_cols[:5]]}")

print("-" * 80)
print(f"\n🔗 เปิด MLflow UI เพื่อดูรายละเอียด: {MLFLOW_TRACKING_URI}")

# %% [markdown]
# ### 9.2 Prompt Template Library
#
# สร้าง Library ของ Prompt Templates ที่ใช้ซ้ำได้:

# %%
# Prompt Template Library
PROMPT_LIBRARY = {
    "sentiment_analysis": {
        "description": "วิเคราะห์ความรู้สึกจากข้อความ",
        "template": """คุณเป็นผู้เชี่ยวชาญด้านการวิเคราะห์ความรู้สึก

วิเคราะห์ความรู้สึกของข้อความต่อไปนี้:
- positive: แสดงความพอใจ ชื่นชม
- negative: แสดงความไม่พอใจ ตำหนิ
- neutral: ไม่มีความรู้สึกชัดเจน

ข้อความ: "{text}"

ตอบเป็น JSON: {{"sentiment": "...", "confidence": 0.0-1.0, "reason": "..."}}""",
        "recommended_temp": 0.3
    },
    
    "summarization": {
        "description": "สรุปเนื้อหา",
        "template": """สรุปเนื้อหาต่อไปนี้ให้กระชับ:

{content}

สรุป:
- ประเด็นหลัก: [1-2 ประโยค]
- ประเด็นรอง: [bullet points]
- ข้อสรุป: [1 ประโยค]""",
        "recommended_temp": 0.5
    },
    
    "code_explanation": {
        "description": "อธิบาย Code",
        "template": """คุณเป็นโปรแกรมเมอร์ผู้เชี่ยวชาญ

อธิบาย Code ต่อไปนี้:
```
{code}
```

อธิบาย:
1. หน้าที่หลัก: ...
2. ทำงานอย่างไร: ...
3. Input/Output: ...
4. ข้อควรระวัง: ...""",
        "recommended_temp": 0.3
    },
    
    "creative_writing": {
        "description": "เขียนเชิงสร้างสรรค์",
        "template": """คุณเป็นนักเขียนมืออาชีพ

เขียน {content_type} เกี่ยวกับ: {topic}

ข้อกำหนด:
- ความยาว: {length}
- โทน: {tone}
- กลุ่มเป้าหมาย: {audience}""",
        "recommended_temp": 0.8
    }
}

print("📚 Prompt Template Library:")
print("-" * 50)
for name, config in PROMPT_LIBRARY.items():
    print(f"• {name}: {config['description']}")
    print(f"  Temperature แนะนำ: {config['recommended_temp']}")
print("-" * 50)

# %% [markdown]
# ---
# ## **ส่วนที่ 10: แบบฝึกหัด (Exercises)**
#
# ### Exercise 1: Custom Sentiment Prompt
# ให้นักศึกษาสร้าง Prompt ใหม่สำหรับ Sentiment Analysis
# ที่รองรับภาษาไทยและ Emoji

# %%
# TODO: Exercise 1 - สร้าง Prompt ที่รองรับ Emoji
# ตัวอย่าง Input: "สินค้าดีมาก 😍👍 รักเลย"

exercise1_prompt = """
# แก้ไข Prompt นี้ให้รองรับ Emoji
# Hint: เพิ่มคำอธิบายเกี่ยวกับการตีความ Emoji

YOUR_PROMPT_HERE = '''
...
'''
"""

# %% [markdown]
# ### Exercise 2: Temperature Experiment
# ทดลองหา Temperature ที่เหมาะสมที่สุดสำหรับ Task ต่อไปนี้

# %%
# TODO: Exercise 2 - หา Temperature ที่เหมาะสม
# Task: เขียนบทกวีสั้นๆ

exercise2_task = """
1. กำหนด Prompt สำหรับเขียนบทกวี
2. ทดลอง Temperature: 0.3, 0.5, 0.7, 0.9, 1.0
3. บันทึกผลลัพธ์ด้วย MLflow
4. เลือก Temperature ที่ให้ผลดีที่สุด
"""

# %% [markdown]
# ### Exercise 3: Chain-of-Thought for Your Domain
# สร้าง CoT Prompt สำหรับปัญหาในสาขาของนักศึกษา

# %%
# TODO: Exercise 3 - สร้าง CoT Prompt สำหรับปัญหาเฉพาะทาง
# เช่น: การวิเคราะห์งบการเงิน, การวินิจฉัยโรค, การแก้ปัญหา Code Bug

exercise3_template = """
# ตัวอย่างโครงสร้าง CoT Prompt

YOUR_COT_PROMPT = '''
คุณเป็น [บทบาท]

ปัญหา: {problem}

ขั้นตอนการวิเคราะห์:
1. [ขั้นตอนที่ 1]: ...
2. [ขั้นตอนที่ 2]: ...
3. [ขั้นตอนที่ 3]: ...

สรุป: ...
'''
"""

# %% [markdown]
# ---
# ## **ส่วนที่ 11: สรุปและทบทวน (Summary)**
#
# ### Key Takeaways
#
# 1. **Prompt Engineering เป็นทั้งศาสตร์และศิลป์** - ต้องทดลองและวัดผลอย่างเป็นระบบ
#
# 2. **MLflow ช่วยให้การทดลอง Prompt เป็นระบบ** - บันทึก Parameters, Metrics, และ Artifacts
#
# 3. **องค์ประกอบสำคัญของ Prompt:**
#    - Context/Role
#    - Clear Instructions
#    - Examples (Few-shot)
#    - Output Format
#    - Constraints
#
# 4. **Temperature มีผลต่อความหลากหลาย** - ต่ำ = แม่นยำ, สูง = สร้างสรรค์
#
# 5. **Chain-of-Thought ช่วยงานที่ต้องการเหตุผล** - เหมาะกับ Math, Logic, Analysis
#
# ### Next Steps
#
# - ทดลองกับ Task จริงในงานของคุณ
# - สร้าง Prompt Library ส่วนตัว
# - ใช้ MLflow ติดตามการเปลี่ยนแปลง
# - แชร์ผลการทดลองกับทีม

# %%
print("=" * 60)
print("🎉 ยินดีด้วย! คุณเสร็จสิ้น Lab แล้ว")
print("=" * 60)
print("\n📌 สิ่งที่ได้เรียนรู้:")
print("  ✅ การใช้งาน Google Gemini API (google-genai package ใหม่)")
print("  ✅ การ Track Experiments ด้วย MLflow")
print("  ✅ Prompt Engineering Techniques")
print("  ✅ การวิเคราะห์และเปรียบเทียบ Prompts")
print("\n🔗 Resources:")
print(f"  • MLflow UI: {MLFLOW_TRACKING_URI}")
print("  • Google AI Studio: https://aistudio.google.com")
print("  • MLflow Docs: https://mlflow.org/docs")
print("  • Google GenAI Docs: https://ai.google.dev/gemini-api/docs")
print("\n👨‍🏫 อย่าลืมตรวจสอบผลลัพธ์ใน MLflow UI!")

# %% [markdown]
# ---
# ## **Appendix: Troubleshooting**
#
# ### ปัญหาที่พบบ่อยและวิธีแก้ไข
#
# | ปัญหา | สาเหตุ | วิธีแก้ |
# |-------|-------|-------|
# | API Key Invalid | API Key ไม่ถูกต้อง | ตรวจสอบและสร้าง Key ใหม่ |
# | Rate Limit | เรียก API ถี่เกินไป | เพิ่ม time.sleep() |
# | MLflow Connection Error | Server ไม่ทำงาน | รัน `mlflow server` ก่อน |
# | Empty Response | Prompt ไม่ชัดเจน | ปรับปรุง Prompt |
# | JSON Parse Error | Output ไม่เป็น JSON | ใช้ Prompt ที่เข้มงวดกว่า |
# | Import Error (google.generativeai) | ใช้ package เก่า | เปลี่ยนเป็น google-genai |
#
# ### คำสั่งที่ใช้บ่อย
#
# ```bash
# # ติดตั้ง package ใหม่
# pip install google-genai
#
# # เริ่ม MLflow Server
# mlflow server --host 0.0.0.0 --port 5000
#
# # ดู Experiments ทั้งหมด
# mlflow experiments search
#
# # Export Results
# mlflow experiments csv -e "prompt-optimization-lab"
# ```
#
# ### การ Migrate จาก google-generativeai (เก่า) ไป google-genai (ใหม่)
#
# ```python
# # เก่า (Deprecated)
# import google.generativeai as genai
# genai.configure(api_key="...")
# model = genai.GenerativeModel("gemini-1.5-flash")
# response = model.generate_content("Hello")
#
# # ใหม่ (Recommended)
# from google import genai
# from google.genai import types
# client = genai.Client(api_key="...")
# response = client.models.generate_content(
#     model="gemini-2.0-flash",
#     contents="Hello",
#     config=types.GenerateContentConfig(temperature=0.7)
# )
# ```

# %% [markdown]
# ---
# **End of Lab**
#
# 📧 หากมีข้อสงสัย ติดต่อผู้สอนได้ที่ [อีเมล/ช่องทางติดต่อ]
