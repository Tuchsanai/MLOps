
# 🧠 **โจทย์ ML ให้คิดเอง + Git + MLOps เบื้องต้น**

> **นักศึกษาต้องคิดโจทย์ ML เอง** และสร้าง pipeline เปรียบเทียบ **3 Models + Metrics**
> ส่งผลลัพธ์ผ่าน **GitHub Repository (private)**

---

## 🎯 **เป้าหมายของโจทย์**

✔ ฝึกคิดโจทย์ ML
✔ ฝึกใช้ train.py
✔ ฝึกเปรียบเทียบ **3 Models พร้อม metric**
✔ ฝึกใช้ Git + GitHub workflow

---

## 📌 **สิ่งที่ต้องส่ง (เกณฑ์ตรวจ)**

| สิ่งที่ต้องมี | รายละเอียด                            |
| ------------- | ------------------------------------- |
| `README.md`   | อธิบาย **โจทย์ ML ที่คิดเอง**         |
| `train.py`    | โหลด dataset + train **3 models**     |
| `result.txt`  | เปรียบเทียบ accuracy / precision / F1 |
| `git push`    | ต้อง push ขึ้น GitHub (private)       |
| Screenshot    | แสดงผลลัพธ์ & Repo บน GitHub          |

---


## 📁 **โครงสร้าง Repository ที่ต้องมี**

```
mlops-git-lab/
│── README.md
│── train.py            ← train 3 models
│── result.txt          ← metric เปรียบเทียบ
│── model_1.pkl
│── model_2.pkl
│── model_3.pkl
```

---

## 💻 **ตัวอย่าง train.py (ให้แค่ 2 models — 1 model ให้นักศึกษาเพิ่มเอง)**

```python
# train.py: นักศึกษาต้องเพิ่ม Model ที่ 3 เอง!
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
# 👍 ตัวอย่างให้แค่ 2 model อีก 1 model นักศึกษาต้องเพิ่มเอง
import joblib

# 1) Load dataset
data = load_iris()  # นักศึกษาเปลี่ยน dataset เองได้!
X_train, X_test, y_train, y_test = train_test_split(
    data.data, data.target, test_size=0.2, random_state=42
)

# 2) Train 2 Models (ตัวอย่าง)
model1 = RandomForestClassifier()
model2 = LogisticRegression(max_iter=200)
# ===== STUDENT MUST ADD MODEL 3 HERE =====

model1.fit(X_train, y_train)
model2.fit(X_train, y_train)

# ===== STUDENT MUST FIT MODEL 3 HERE =====

# 3) Predict
y_pred1 = model1.predict(X_test)
y_pred2 = model2.predict(X_test)
# ===== STUDENT MUST ADD MODEL 3 HERE =====

# 4) Evaluate
acc1 = accuracy_score(y_test, y_pred1)
acc2 = accuracy_score(y_test, y_pred2)
f1_1 = f1_score(y_test, y_pred1, average='macro')
f1_2 = f1_score(y_test, y_pred2, average='macro')

# ===== STUDENT MUST ADD MODEL 3 HERE =====

# 5) Save models
joblib.dump(model1, "model_rf.pkl")
joblib.dump(model2, "model_lr.pkl")
# joblib.dump(model3, "model_xxx.pkl")  # ← ต้องมี!

# 6) Save result
with open("result.txt", "w") as f:
    f.write("=== ML RESULT ===\n")
    f.write(f"RandomForest: acc={acc1:.4f}, f1={f1_1:.4f}\n")
    f.write(f"LogisticReg:  acc={acc2:.4f}, f1={f1_2:.4f}\n")
    f.write("\nModel ที่ 3 นักศึกษาเติมเอง\n")

print("Training done! Check result.txt")
```

---

## ☁️ **การ Run บน Cloud**

```bash
git clone https://username:YOUR_TOKEN@github.com/username/mlops-git-lab.git
cd mlops-git-lab

python3 train.py
cat result.txt

git add .
git commit -m "Add ML model + result"
git push
```

---

## 📝 **ตัวอย่างการส่งงาน**

```
📌 โจทย์: ทำนายเบาหวาน (Diabetes dataset)

📌 เปรียบเทียบ Model  
RandomForest     → acc=0.82, f1=0.80  
LogisticReg      → acc=0.75, f1=0.72  
SVM (Model 3)    → acc=0.84, f1=0.83  ✔ ดีสุด  

📌 GitHub Repo:
https://github.com/username/mlops-git-lab
```

---

## 🎉 **เมื่อทำ Lab นี้จบ นักศึกษาจะเข้าใจ**

✔ การคิดโจทย์ ML เอง
✔ การ train & เปรียบเทียบ **3 models**
✔ การเก็บ metric ใน `result.txt`
✔ Git clone → status → add → commit → push
✔ ใช้ GitHub เป็น **หลักฐานการบ้านแบบ MLOps จริง** 🚀

