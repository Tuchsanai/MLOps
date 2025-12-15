
# 🧪 **Lab: Git + MLOps พื้นฐาน สำหรับผู้เริ่มต้น**

## 🎯 **วัตถุประสงค์ของ Lab**

* เข้าใจการใช้งาน Git เบื้องต้น
* รู้จักการใช้ **git clone จาก private repository**
* ฝึกสร้างไฟล์ `train.py` และ **train model บน cloud**
* นำผลลัพธ์จาก model มา push กลับขึ้น GitHub
* ใช้ Git repo เป็นหลักฐานตอบการบ้าน / ส่งงาน

---

## 📌 **สิ่งที่ต้องทำ (สรุปกระบวนการ)**

1. สร้าง **Private Repository** พร้อม `README.md`
2. สร้างไฟล์ `train.py` บน GitHub
3. ใช้ Cloud  เพื่อ `git clone`
4. Train model → เก็บผลลัพธ์
5. Push ผลลัพธ์ขึ้น GitHub
6. นำผลลัพธ์ใน repo ไปตอบการบ้าน

---

## 🧭 **Part 1: สร้าง Private Repository**

1. เข้า GitHub → กด **New Repository**
2. ตั้งชื่อ repo เช่น `mlops-git-lab`
3. เลือก `Private`
4. ติ๊ก ✔️ `Add README.md`
5. กด **Create Repository**

---

## 🧾 **Part 2: สร้างไฟล์ train.py**

ให้สร้างไฟล์ผ่านหน้าเว็บ GitHub
**File → Create new file**
ตั้งชื่อ: `train.py`

ตัวอย่างโค้ดง่าย ๆ:

```python
# train.py : ตัวอย่าง ML ง่ายที่สุด
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# 1) Load data
data = load_iris()
X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.2)

# 2) Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# 3) Save model + accuracy
acc = model.score(X_test, y_test)
joblib.dump(model, "model.pkl")

with open("result.txt", "w") as f:
    f.write(f"Accuracy = {acc}")

print("Training completed! Accuracy =", acc)
```

> 💾 เมื่อ save แล้วจะเห็นไฟล์ใน GitHub repository

---

## ☁️ **Part 3: clone บน Cloud**

หลังจากสร้าง **GitHub token** แล้วให้ใช้คำสั่งนี้ (เปลี่ยน username/token/repo ตามจริง):

```bash
git clone https://username:YOUR_TOKEN@github.com/username/mlops-git-lab.git
cd mlops-git-lab
```

---

## ⚙️ **Part 4: Train model**

```bash
python3 train.py
```

หลังจากรัน จะได้ไฟล์:

```
model.pkl
result.txt
```

---

## ⬆️ **Part 5: Push ผลลัพธ์ขึ้น GitHub**

```bash
git add .
git commit -m "Add model and result"
git push
```

---

## 📝 **Part 6: ตอบการบ้าน**

ให้ส่ง **ลิงก์ repo** พร้อม capture ผลลัพธ์ใน `result.txt`
เช่น:

```
ผลลัพธ์ model:
Accuracy = 0.95
GitHub Repo: https://github.com/username/mlops-git-lab
```

---

## 🎉 **จบ Lab แล้ว! นักศึกษาควรรู้**

✔ การสร้าง private repo
✔ การ clone ด้วย token
✔ การ train model บน cloud
✔ การ push ผลลัพธ์ขึ้น GitHub
✔ การใช้ Git repo เป็นหลักฐานการบ้าน

