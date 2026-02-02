# %% [markdown]
# # 🚀 Lab: Prompt Optimization using MLflow
#
# **วัตถุประสงค์การเรียนรู้ (Learning Objectives)**
# - เข้าใจหลักการของ Prompt Engineering และ Optimization
# - ใช้ MLflow ในการ track และเปรียบเทียบ prompts ต่างๆ
# - วิเคราะห์ metrics เพื่อเลือก prompt ที่ดีที่สุด
# - สร้าง systematic approach ในการทดสอบ prompts
#
# **เครื่องมือที่ใช้:** Python, MLflow, OpenAI/Ollama API
#
# ---

# %% [markdown]
# ## 📦 Part 1: Environment Setup
#
# ติดตั้ง libraries ที่จำเป็น

# %%
# Install required packages (run once)
# !pip install mlflow openai tiktoken pandas numpy scikit-learn

# %%
# Import libraries
import mlflow
import mlflow.pyfunc
from mlflow.tracking import MlflowClient
import json
import time
import hashlib
from datetime import datetime
from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np

# For LLM interaction
import os
from openai import OpenAI

# For evaluation metrics
from sklearn.metrics import accuracy_score
import re

print("✅ Libraries imported successfully!")

# %% [markdown]
# ## ⚙️ Part 2: Configuration
#
# ตั้งค่า MLflow และ LLM API

# %%
# MLflow Configuration
MLFLOW_TRACKING_URI = "http://localhost:5000"  # หรือใช้ local: "mlruns"
EXPERIMENT_NAME = "prompt-optimization-lab"

# Set tracking URI
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# Create or get experiment
experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
if experiment is None:
    experiment_id = mlflow.create_experiment(
        EXPERIMENT_NAME,
        tags={"project": "prompt-engineering", "version": "1.0"}
    )
    print(f"✅ Created new experiment: {EXPERIMENT_NAME} (ID: {experiment_id})")
else:
    experiment_id = experiment.experiment_id
    print(f"✅ Using existing experiment: {EXPERIMENT_NAME} (ID: {experiment_id})")

mlflow.set_experiment(EXPERIMENT_NAME)

# %%
# LLM Configuration
# Option 1: OpenAI
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# MODEL_NAME = "gpt-3.5-turbo"

# Option 2: Ollama (Local)
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # Ollama doesn't need real API key
)
MODEL_NAME = "llama3.2"  # หรือ model ที่คุณมี

print(f"✅ LLM configured: {MODEL_NAME}")

# %% [markdown]
# ## 📝 Part 3: Define Test Dataset
#
# สร้างชุดข้อมูลสำหรับทดสอบ prompts
#
# **Task: Sentiment Classification**

# %%
# Test dataset for sentiment classification
test_data = [
    {
        "text": "สินค้าคุณภาพดีมาก ส่งเร็ว ประทับใจมากครับ",
        "expected": "positive"
    },
    {
        "text": "แย่มาก รอนานมาก สินค้าไม่ตรงปก",
        "expected": "negative"
    },
    {
        "text": "สินค้าก็โอเคนะ ไม่ได้ดีไม่ได้แย่",
        "expected": "neutral"
    },
    {
        "text": "ชอบมากเลย จะกลับมาซื้อใหม่แน่นอน!",
        "expected": "positive"
    },
    {
        "text": "ผิดหวังมาก คุณภาพไม่คุ้มราคา",
        "expected": "negative"
    },
    {
        "text": "ธรรมดา ใช้ได้",
        "expected": "neutral"
    },
    {
        "text": "บริการดีเยี่ยม แนะนำเลยครับ",
        "expected": "positive"
    },
    {
        "text": "ไม่ซื้ออีกแล้ว เสียเงินเปล่า",
        "expected": "negative"
    },
    {
        "text": "ราคาพอรับได้ คุณภาพก็งั้นๆ",
        "expected": "neutral"
    },
    {
        "text": "ของแท้ 100% คุณภาพเกินราคา สุดยอด!",
        "expected": "positive"
    }
]

print(f"✅ Test dataset loaded: {len(test_data)} samples")
print(f"   - Positive: {sum(1 for d in test_data if d['expected'] == 'positive')}")
print(f"   - Negative: {sum(1 for d in test_data if d['expected'] == 'negative')}")
print(f"   - Neutral: {sum(1 for d in test_data if d['expected'] == 'neutral')}")

# %% [markdown]
# ## 🎯 Part 4: Define Prompt Templates
#
# สร้าง prompt templates หลายแบบเพื่อเปรียบเทียบประสิทธิภาพ

# %%
# Prompt templates for comparison
prompt_templates = {
    "v1_basic": {
        "name": "Basic Prompt",
        "description": "Simple instruction without examples",
        "template": """Classify the sentiment of the following Thai text as positive, negative, or neutral.

Text: {text}

Respond with only one word: positive, negative, or neutral"""
    },
    
    "v2_detailed": {
        "name": "Detailed Instruction",
        "description": "More detailed instructions with criteria",
        "template": """You are a sentiment analysis expert for Thai language.

Analyze the sentiment of the given text and classify it into one of three categories:
- positive: The text expresses satisfaction, happiness, or recommendation
- negative: The text expresses dissatisfaction, complaint, or disappointment  
- neutral: The text is neither clearly positive nor negative

Text to analyze: {text}

Important: Respond with exactly one word (positive, negative, or neutral)."""
    },
    
    "v3_few_shot": {
        "name": "Few-Shot Learning",
        "description": "Prompt with examples (few-shot)",
        "template": """Classify Thai text sentiment. Here are examples:

Example 1: "สินค้าดีมาก ชอบมาก" → positive
Example 2: "แย่มาก ไม่ประทับใจเลย" → negative  
Example 3: "ก็พอใช้ได้" → neutral

Now classify this text: {text}

Answer (one word only):"""
    },
    
    "v4_cot": {
        "name": "Chain-of-Thought",
        "description": "Prompt encouraging step-by-step reasoning",
        "template": """Analyze the sentiment of this Thai text step by step.

Text: {text}

Step 1: Identify key sentiment words or phrases
Step 2: Determine if overall tone is positive, negative, or neutral
Step 3: Give final classification

Final answer (one word: positive/negative/neutral):"""
    },
    
    "v5_role_play": {
        "name": "Role-Play Expert",
        "description": "Persona-based prompt",
        "template": """You are a senior Thai language analyst at a leading e-commerce company. 
You have 10 years of experience analyzing customer reviews.

Your task: Classify the sentiment of this customer review.

Review: {text}

Based on your expertise, what is the sentiment? (Answer: positive, negative, or neutral)"""
    }
}

print(f"✅ Defined {len(prompt_templates)} prompt templates:")
for key, value in prompt_templates.items():
    print(f"   - {key}: {value['name']}")

# %% [markdown]
# ## 🔧 Part 5: Helper Functions
#
# สร้าง functions สำหรับการทดสอบและวัดผล

# %%
def call_llm(prompt: str, temperature: float = 0.0) -> Dict[str, Any]:
    """
    เรียกใช้ LLM และคืนค่า response พร้อม metadata
    """
    start_time = time.time()
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=100
        )
        
        latency = time.time() - start_time
        
        return {
            "success": True,
            "response": response.choices[0].message.content.strip(),
            "latency": latency,
            "tokens_used": response.usage.total_tokens if response.usage else 0,
            "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
            "completion_tokens": response.usage.completion_tokens if response.usage else 0
        }
    except Exception as e:
        return {
            "success": False,
            "response": str(e),
            "latency": time.time() - start_time,
            "tokens_used": 0,
            "prompt_tokens": 0,
            "completion_tokens": 0
        }

# %%
def extract_sentiment(response: str) -> str:
    """
    ดึง sentiment จาก LLM response
    """
    response_lower = response.lower()
    
    # ลำดับความสำคัญ: ถ้าพบคำสุดท้ายใน response
    for sentiment in ["positive", "negative", "neutral"]:
        if sentiment in response_lower:
            # หา occurrence สุดท้าย
            last_pos = response_lower.rfind(sentiment)
            if last_pos != -1:
                return sentiment
    
    return "unknown"

# %%
def calculate_metrics(predictions: List[str], ground_truth: List[str]) -> Dict[str, float]:
    """
    คำนวณ metrics สำหรับการประเมินผล
    """
    # Accuracy
    correct = sum(1 for p, g in zip(predictions, ground_truth) if p == g)
    accuracy = correct / len(ground_truth)
    
    # Per-class metrics
    classes = ["positive", "negative", "neutral"]
    metrics = {"accuracy": accuracy}
    
    for cls in classes:
        # True Positives, False Positives, False Negatives
        tp = sum(1 for p, g in zip(predictions, ground_truth) if p == cls and g == cls)
        fp = sum(1 for p, g in zip(predictions, ground_truth) if p == cls and g != cls)
        fn = sum(1 for p, g in zip(predictions, ground_truth) if p != cls and g == cls)
        
        # Precision, Recall, F1
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        
        metrics[f"{cls}_precision"] = precision
        metrics[f"{cls}_recall"] = recall
        metrics[f"{cls}_f1"] = f1
    
    # Macro F1
    metrics["macro_f1"] = np.mean([metrics[f"{cls}_f1"] for cls in classes])
    
    return metrics

# %%
def get_prompt_hash(prompt_template: str) -> str:
    """
    สร้าง hash สำหรับ prompt template (ใช้ track versions)
    """
    return hashlib.md5(prompt_template.encode()).hexdigest()[:8]

print("✅ Helper functions defined!")

# %% [markdown]
# ## 🧪 Part 6: Run Prompt Optimization Experiment
#
# ทดสอบแต่ละ prompt template และ log ผลลัพธ์ไปยัง MLflow

# %%
def run_prompt_experiment(
    prompt_key: str,
    prompt_config: Dict[str, str],
    test_data: List[Dict],
    temperature: float = 0.0
) -> Dict[str, Any]:
    """
    รัน experiment สำหรับ prompt template หนึ่งตัว
    """
    template = prompt_config["template"]
    results = []
    predictions = []
    ground_truth = []
    total_latency = 0
    total_tokens = 0
    
    print(f"\n🔄 Testing: {prompt_config['name']}")
    print("-" * 50)
    
    for i, sample in enumerate(test_data):
        # สร้าง prompt จาก template
        prompt = template.format(text=sample["text"])
        
        # เรียก LLM
        llm_result = call_llm(prompt, temperature)
        
        if llm_result["success"]:
            # Extract sentiment
            predicted = extract_sentiment(llm_result["response"])
            predictions.append(predicted)
            ground_truth.append(sample["expected"])
            
            # Collect stats
            total_latency += llm_result["latency"]
            total_tokens += llm_result["tokens_used"]
            
            # Store result
            results.append({
                "text": sample["text"][:50] + "...",
                "expected": sample["expected"],
                "predicted": predicted,
                "correct": predicted == sample["expected"],
                "latency": llm_result["latency"],
                "raw_response": llm_result["response"][:100]
            })
            
            status = "✓" if predicted == sample["expected"] else "✗"
            print(f"  [{i+1}/{len(test_data)}] {status} Expected: {sample['expected']}, Got: {predicted}")
        else:
            print(f"  [{i+1}/{len(test_data)}] ❌ Error: {llm_result['response']}")
            predictions.append("error")
            ground_truth.append(sample["expected"])
    
    # Calculate metrics
    metrics = calculate_metrics(predictions, ground_truth)
    metrics["avg_latency"] = total_latency / len(test_data)
    metrics["total_tokens"] = total_tokens
    metrics["avg_tokens_per_request"] = total_tokens / len(test_data)
    
    return {
        "prompt_key": prompt_key,
        "config": prompt_config,
        "results": results,
        "metrics": metrics,
        "predictions": predictions,
        "ground_truth": ground_truth
    }

# %%
# Run experiments for all prompt templates
all_experiments = {}

print("=" * 60)
print("🚀 STARTING PROMPT OPTIMIZATION EXPERIMENTS")
print("=" * 60)

for prompt_key, prompt_config in prompt_templates.items():
    
    # Start MLflow run
    with mlflow.start_run(run_name=f"prompt_{prompt_key}") as run:
        
        # Log parameters
        mlflow.log_param("prompt_version", prompt_key)
        mlflow.log_param("prompt_name", prompt_config["name"])
        mlflow.log_param("prompt_description", prompt_config["description"])
        mlflow.log_param("prompt_hash", get_prompt_hash(prompt_config["template"]))
        mlflow.log_param("model_name", MODEL_NAME)
        mlflow.log_param("temperature", 0.0)
        mlflow.log_param("test_samples", len(test_data))
        
        # Log prompt template as artifact
        mlflow.log_text(prompt_config["template"], "prompt_template.txt")
        
        # Run experiment
        experiment_result = run_prompt_experiment(
            prompt_key, 
            prompt_config, 
            test_data
        )
        
        # Log metrics
        for metric_name, metric_value in experiment_result["metrics"].items():
            mlflow.log_metric(metric_name, metric_value)
        
        # Log detailed results as artifact
        results_df = pd.DataFrame(experiment_result["results"])
        results_df.to_csv("/tmp/results.csv", index=False)
        mlflow.log_artifact("/tmp/results.csv", "evaluation")
        
        # Store for comparison
        all_experiments[prompt_key] = {
            "run_id": run.info.run_id,
            "metrics": experiment_result["metrics"],
            "results": experiment_result["results"]
        }
        
        print(f"\n📊 Results for {prompt_config['name']}:")
        print(f"   Accuracy: {experiment_result['metrics']['accuracy']:.2%}")
        print(f"   Macro F1: {experiment_result['metrics']['macro_f1']:.2%}")
        print(f"   Avg Latency: {experiment_result['metrics']['avg_latency']:.3f}s")
        print(f"   Run ID: {run.info.run_id}")

print("\n" + "=" * 60)
print("✅ ALL EXPERIMENTS COMPLETED!")
print("=" * 60)

# %% [markdown]
# ## 📊 Part 7: Compare Results
#
# เปรียบเทียบผลลัพธ์ของ prompt templates ทั้งหมด

# %%
# Create comparison dataframe
comparison_data = []

for prompt_key, exp_data in all_experiments.items():
    row = {
        "Prompt Version": prompt_key,
        "Name": prompt_templates[prompt_key]["name"],
        "Accuracy": exp_data["metrics"]["accuracy"],
        "Macro F1": exp_data["metrics"]["macro_f1"],
        "Avg Latency (s)": exp_data["metrics"]["avg_latency"],
        "Total Tokens": exp_data["metrics"]["total_tokens"],
        "Run ID": exp_data["run_id"][:8]
    }
    comparison_data.append(row)

comparison_df = pd.DataFrame(comparison_data)
comparison_df = comparison_df.sort_values("Accuracy", ascending=False)

print("\n📈 PROMPT COMPARISON RESULTS")
print("=" * 80)
print(comparison_df.to_string(index=False))

# %%
# Find best prompt
best_prompt = comparison_df.iloc[0]
print("\n" + "=" * 60)
print("🏆 BEST PERFORMING PROMPT")
print("=" * 60)
print(f"Version: {best_prompt['Prompt Version']}")
print(f"Name: {best_prompt['Name']}")
print(f"Accuracy: {best_prompt['Accuracy']:.2%}")
print(f"Macro F1: {best_prompt['Macro F1']:.2%}")
print(f"Avg Latency: {best_prompt['Avg Latency (s)']:.3f}s")

# %%
# Detailed per-class performance
print("\n📊 PER-CLASS PERFORMANCE (Best Prompt)")
print("-" * 50)

best_key = best_prompt['Prompt Version']
best_metrics = all_experiments[best_key]["metrics"]

for cls in ["positive", "negative", "neutral"]:
    print(f"\n{cls.upper()}:")
    print(f"  Precision: {best_metrics[f'{cls}_precision']:.2%}")
    print(f"  Recall: {best_metrics[f'{cls}_recall']:.2%}")
    print(f"  F1-Score: {best_metrics[f'{cls}_f1']:.2%}")

# %% [markdown]
# ## 📦 Part 8: Register Best Model in MLflow
#
# ลงทะเบียน prompt ที่ดีที่สุดเป็น model ใน MLflow Model Registry

# %%
# Create a custom MLflow model for the best prompt
class PromptModel(mlflow.pyfunc.PythonModel):
    """
    Custom MLflow model that wraps a prompt template
    """
    
    def __init__(self, prompt_template: str, model_name: str):
        self.prompt_template = prompt_template
        self.model_name = model_name
    
    def predict(self, context, model_input):
        """
        Run prediction using the prompt template
        """
        # model_input should be a DataFrame with 'text' column
        results = []
        
        for idx, row in model_input.iterrows():
            prompt = self.prompt_template.format(text=row['text'])
            
            # Note: In production, you'd call the actual LLM here
            # For demo, we'll just return the prompt
            results.append({
                "input": row['text'],
                "prompt": prompt
            })
        
        return results

# %%
# Register the best prompt as a model
best_prompt_key = best_prompt['Prompt Version']
best_template = prompt_templates[best_prompt_key]["template"]

with mlflow.start_run(run_name=f"register_best_prompt_{best_prompt_key}") as run:
    
    # Log the prompt model
    prompt_model = PromptModel(
        prompt_template=best_template,
        model_name=MODEL_NAME
    )
    
    # Log model
    mlflow.pyfunc.log_model(
        artifact_path="prompt_model",
        python_model=prompt_model,
        registered_model_name="sentiment_prompt_model"
    )
    
    # Log additional metadata
    mlflow.log_param("prompt_version", best_prompt_key)
    mlflow.log_param("accuracy", best_prompt['Accuracy'])
    mlflow.log_param("macro_f1", best_prompt['Macro F1'])
    
    # Log prompt template
    mlflow.log_text(best_template, "best_prompt_template.txt")
    
    print(f"✅ Registered model: sentiment_prompt_model")
    print(f"   Run ID: {run.info.run_id}")

# %% [markdown]
# ## 🔬 Part 9: Advanced - A/B Testing Configuration
#
# เตรียม configuration สำหรับ A/B testing ระหว่าง prompts

# %%
# Create A/B test configuration
ab_test_config = {
    "experiment_name": "prompt_ab_test",
    "variants": [
        {
            "name": "control",
            "prompt_version": "v1_basic",
            "traffic_percentage": 50
        },
        {
            "name": "treatment",
            "prompt_version": best_prompt_key,
            "traffic_percentage": 50
        }
    ],
    "success_metrics": ["accuracy", "macro_f1"],
    "guardrail_metrics": ["avg_latency"],
    "min_sample_size": 1000,
    "confidence_level": 0.95
}

# Save configuration
with mlflow.start_run(run_name="ab_test_config"):
    mlflow.log_dict(ab_test_config, "ab_test_config.json")
    print("✅ A/B Test configuration logged to MLflow")

print("\n📋 A/B Test Configuration:")
print(json.dumps(ab_test_config, indent=2))

# %% [markdown]
# ## 📈 Part 10: Visualize Results
#
# สร้าง visualization สำหรับเปรียบเทียบ prompts

# %%
# Simple text-based visualization
print("\n" + "=" * 70)
print("📊 ACCURACY COMPARISON CHART")
print("=" * 70)

max_acc = comparison_df['Accuracy'].max()

for _, row in comparison_df.iterrows():
    bar_length = int(row['Accuracy'] / max_acc * 40)
    bar = "█" * bar_length
    spaces = " " * (40 - bar_length)
    print(f"{row['Prompt Version']:15} |{bar}{spaces}| {row['Accuracy']:.1%}")

# %%
# Latency vs Accuracy trade-off
print("\n" + "=" * 70)
print("⚡ LATENCY vs ACCURACY TRADE-OFF")
print("=" * 70)

for _, row in comparison_df.iterrows():
    acc = row['Accuracy']
    lat = row['Avg Latency (s)']
    
    # Simple efficiency score (accuracy / latency)
    efficiency = acc / lat if lat > 0 else 0
    
    print(f"{row['Prompt Version']:15} | Acc: {acc:.1%} | Lat: {lat:.2f}s | Efficiency: {efficiency:.2f}")

# %% [markdown]
# ## 🎯 Part 11: Exercise - Create Your Own Prompt
#
# **แบบฝึกหัด:** สร้าง prompt template ของคุณเองและทดสอบ

# %%
# TODO: สร้าง prompt template ของคุณเอง
my_custom_prompt = {
    "name": "My Custom Prompt",
    "description": "Your custom prompt description",
    "template": """
[เขียน prompt template ของคุณที่นี่]

Text: {text}

Answer:
"""
}

# Uncomment to test your prompt:
# prompt_templates["v6_custom"] = my_custom_prompt
# 
# with mlflow.start_run(run_name="prompt_v6_custom"):
#     result = run_prompt_experiment("v6_custom", my_custom_prompt, test_data)
#     for metric_name, metric_value in result["metrics"].items():
#         mlflow.log_metric(metric_name, metric_value)

# %% [markdown]
# ## 📝 Summary & Key Takeaways
#
# ### สิ่งที่เรียนรู้ในแลบนี้:
#
# 1. **Prompt Engineering Techniques**
#    - Basic prompts
#    - Detailed instructions
#    - Few-shot learning
#    - Chain-of-thought reasoning
#    - Role-playing/Persona
#
# 2. **MLflow for Prompt Tracking**
#    - Log prompt templates as parameters และ artifacts
#    - Track performance metrics (accuracy, F1, latency)
#    - Compare multiple prompt versions
#    - Register best prompts as models
#
# 3. **Systematic Evaluation**
#    - สร้าง test dataset ที่ครอบคลุม
#    - วัดผลด้วย metrics หลายตัว
#    - พิจารณา trade-offs (accuracy vs latency)
#
# 4. **Best Practices**
#    - Version control สำหรับ prompts
#    - Reproducible experiments
#    - Documentation และ metadata
#
# ---
#
# ### 🔗 Useful Resources:
# - [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
# - [Prompt Engineering Guide](https://www.promptingguide.ai/)
# - [OpenAI Best Practices](https://platform.openai.com/docs/guides/prompt-engineering)

# %%
print("\n" + "=" * 60)
print("🎉 LAB COMPLETED!")
print("=" * 60)
print(f"\nMLflow UI: {MLFLOW_TRACKING_URI}")
print(f"Experiment: {EXPERIMENT_NAME}")
print(f"\nTo view results, run: mlflow ui --port 5000")
