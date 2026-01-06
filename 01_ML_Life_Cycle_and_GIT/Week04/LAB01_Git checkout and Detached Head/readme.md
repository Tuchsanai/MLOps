# 🔬 Lab: Git Checkout และ Detached HEAD State

## สำหรับนักศึกษา MLOps

---

## 📚 วัตถุประสงค์การเรียนรู้

เมื่อจบ Lab นี้ นักศึกษาจะสามารถ:

1. เข้าใจการทำงานของ `git checkout` ในบริบทต่างๆ
2. เข้าใจว่า **Detached HEAD** คืออะไร และเกิดขึ้นเมื่อใด
3. รู้วิธีจัดการและออกจากสถานะ Detached HEAD อย่างปลอดภัย
4. ประยุกต์ใช้ในการทดลอง ML Model versions ต่างๆ

---

## 🎯 สถานการณ์จำลอง

สมมติว่าเราเป็น ML Engineer ที่กำลังพัฒนาโมเดล Classification สำหรับจำแนกดอกไม้ Iris โดยเราได้พัฒนาโมเดลมาเรื่อยๆ ผ่านหลาย versions:

| Version | Model | รายละเอียด |
|---------|-------|------------|
| v1.0 | Logistic Regression | โมเดลพื้นฐาน เริ่มต้นโปรเจค |
| v2.0 | Random Forest | เปลี่ยนอัลกอริทึมเพื่อเพิ่มประสิทธิภาพ |
| v3.0 | Random Forest (Tuned) | ปรับ hyperparameters ให้ดีขึ้น |

### ปัญหาที่เจอในการทำงานจริง

ในการพัฒนา ML Model มักจะเจอสถานการณ์เหล่านี้:

1. **ต้องการดูโค้ดเก่า** - หัวหน้าถามว่า "โมเดล v1.0 เขียนยังไง?" เราต้องย้อนกลับไปดู
2. **ต้องการเปรียบเทียบ** - อยากรู้ว่า v1.0 กับ v2.0 ต่างกันตรงไหน
3. **ต้องการทดลอง** - อยากลองแก้โค้ดเก่าดูว่าผลลัพธ์จะดีขึ้นไหม
4. **ต้องการกู้โค้ด** - โค้ดใหม่พัง อยากเอาบางส่วนจากเวอร์ชันเก่ากลับมา

### สิ่งที่จะได้เรียนรู้ใน Lab นี้

```
                                Flow ของ Lab
                                
    [สร้าง v1.0] --> [สร้าง v2.0] --> [สร้าง v3.0] --> [ย้อนกลับไป v1.0]
         |               |               |                    |
    Logistic        Random Forest   RF Tuned           Detached HEAD!
    Regression                                               |
                                                             v
                                                    [ทดลองแก้โค้ด]
                                                             |
                                                             v
                                                    [สร้าง Branch เก็บ]
```

เราจะจำลองการทำงานจริงโดย:
1. สร้าง commits 3 ตัว แทน 3 versions ของโมเดล
2. ใช้ `git checkout` ย้อนกลับไปดู commit เก่า
3. เข้าสู่สถานะ **Detached HEAD** และเรียนรู้วิธีจัดการ
4. ทดลองแก้ไขโค้ดและบันทึกการทดลองอย่างปลอดภัย

---

## 📋 สิ่งที่ต้องเตรียม

```bash
# ตรวจสอบว่ามี Git และ Python
git --version
python3 --version

# ติดตั้ง scikit-learn (ถ้ายังไม่มี)
pip install scikit-learn pandas
```

### ตั้งค่า Git User (ถ้ายังไม่ได้ตั้ง)

```bash
git config --global user.name "นักศึกษา MLOps"
git config --global user.email "student@example.com"
```

---

## 🚀 ขั้นตอนปฏิบัติ

### ขั้นตอนที่ 1: สร้าง Project และ Initialize Git

> 📌 **จุดประสงค์:** เตรียม working directory และเริ่มต้น Git repository เปล่า
> 
> ขั้นตอนนี้เหมือนกับการสร้างโฟลเดอร์โปรเจคใหม่และบอก Git ว่า "ช่วย track การเปลี่ยนแปลงในโฟลเดอร์นี้ด้วย"

```bash
# สร้างโฟลเดอร์โปรเจค
mkdir ml-classification-project
cd ml-classification-project

# เริ่มต้น Git repository
git init
```

---

### ขั้นตอนที่ 2: สร้าง Version 1.0 - Logistic Regression

> 📌 **จุดประสงค์:** สร้าง commit แรก เป็นจุดเริ่มต้นของโปรเจค
> 
> เราจะสร้างโมเดล ML อย่างง่ายด้วย **Logistic Regression** ซึ่งเป็นอัลกอริทึมพื้นฐานสำหรับ classification แล้ว commit เป็น version แรก
>
> **สิ่งที่จะเกิดขึ้น:** Git จะบันทึก snapshot ของโค้ดนี้ไว้ เราสามารถกลับมาดูได้ตลอด

```bash
cat > train_model.py << 'EOF'
# train_model.py - Version 1.0: Logistic Regression
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import json

def train():
    # โหลดข้อมูล Iris dataset
    iris = load_iris()
    X, y = iris.data, iris.target
    
    # แบ่งข้อมูล
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # สร้างและ train โมเดล Logistic Regression
    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)
    
    # ประเมินผล
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    # บันทึกผลลัพธ์
    result = {
        "model": "LogisticRegression",
        "version": "1.0",
        "accuracy": round(accuracy, 4)
    }
    
    print(f"Model: {result['model']}")
    print(f"Version: {result['version']}")
    print(f"Accuracy: {result['accuracy']}")
    
    return result

if __name__ == "__main__":
    train()
EOF
```

**Commit Version 1.0:**

```bash
# เพิ่มไฟล์และ commit
git add train_model.py
git commit -m "v1.0: Initial Logistic Regression model"
```

**ทดสอบรัน:**

```bash
python train_model.py
```

**ผลลัพธ์ที่คาดหวัง:**
```
Model: LogisticRegression
Version: 1.0
Accuracy: 1.0
```

---

### ขั้นตอนที่ 3: สร้าง Version 2.0 - Random Forest

> 📌 **จุดประสงค์:** สร้าง commit ที่สอง แสดงการพัฒนาต่อยอดจาก version แรก
> 
> เราจะ **เปลี่ยนอัลกอริทึม** จาก Logistic Regression เป็น **Random Forest** ซึ่งมักให้ผลลัพธ์ที่ดีกว่า
>
> **ความแตกต่างจาก v1.0:**
> - เปลี่ยน import จาก `LogisticRegression` เป็น `RandomForestClassifier`
> - เพิ่ม parameter `n_estimators=10` (จำนวน trees)

```bash
cat > train_model.py << 'EOF'
# train_model.py - Version 2.0: Random Forest
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import json

def train():
    # โหลดข้อมูล Iris dataset
    iris = load_iris()
    X, y = iris.data, iris.target
    
    # แบ่งข้อมูล
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # สร้างและ train โมเดล Random Forest
    model = RandomForestClassifier(n_estimators=10, random_state=42)
    model.fit(X_train, y_train)
    
    # ประเมินผล
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    # บันทึกผลลัพธ์
    result = {
        "model": "RandomForestClassifier",
        "version": "2.0",
        "n_estimators": 10,
        "accuracy": round(accuracy, 4)
    }
    
    print(f"Model: {result['model']}")
    print(f"Version: {result['version']}")
    print(f"n_estimators: {result['n_estimators']}")
    print(f"Accuracy: {result['accuracy']}")
    
    return result

if __name__ == "__main__":
    train()
EOF
```

**Commit Version 2.0:**

```bash
git add train_model.py
git commit -m "v2.0: Switch to Random Forest model"
```

**ทดสอบรัน:**

```bash
python train_model.py
```

---

### ขั้นตอนที่ 4: สร้าง Version 3.0 - Tuned Random Forest

> 📌 **จุดประสงค์:** สร้าง commit ที่สาม แสดงการ tune hyperparameters
> 
> เราจะ **ปรับ hyperparameters** ของ Random Forest เพื่อให้โมเดลดีขึ้น
>
> **ความแตกต่างจาก v2.0:**
> - เพิ่ม `n_estimators` จาก 10 เป็น 100 (ใช้ trees มากขึ้น)
> - เพิ่ม `max_depth=5` (จำกัดความลึกของ tree)
> - เพิ่ม `min_samples_split=2`

```bash
cat > train_model.py << 'EOF'
# train_model.py - Version 3.0: Tuned Random Forest
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import json

def train():
    # โหลดข้อมูล Iris dataset
    iris = load_iris()
    X, y = iris.data, iris.target
    
    # แบ่งข้อมูล
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # สร้างและ train โมเดล Random Forest (Tuned)
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=5,
        min_samples_split=2,
        random_state=42
    )
    model.fit(X_train, y_train)
    
    # ประเมินผล
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    # บันทึกผลลัพธ์
    result = {
        "model": "RandomForestClassifier",
        "version": "3.0",
        "n_estimators": 100,
        "max_depth": 5,
        "accuracy": round(accuracy, 4)
    }
    
    print(f"Model: {result['model']}")
    print(f"Version: {result['version']}")
    print(f"n_estimators: {result['n_estimators']}")
    print(f"max_depth: {result['max_depth']}")
    print(f"Accuracy: {result['accuracy']}")
    
    return result

if __name__ == "__main__":
    train()
EOF
```

**Commit Version 3.0:**

```bash
git add train_model.py
git commit -m "v3.0: Tuned Random Forest with more trees"
```

---

### ขั้นตอนที่ 5: ดู History ของโปรเจค

> 📌 **จุดประสงค์:** ดูภาพรวมของ commits ทั้งหมดที่สร้างมา
> 
> คำสั่ง `git log` จะแสดง commits ทั้งหมด พร้อม **commit hash** (รหัสเฉพาะของแต่ละ commit)
>
> **สิ่งสำคัญ:** จด commit hash ไว้ เพราะเราจะใช้มันใน checkout ขั้นตอนถัดไป

```bash
# ดู log แบบสวยงาม
git log --oneline --graph --all
```

**ผลลัพธ์จะประมาณนี้:**
```
* abc1234 (HEAD -> main) v3.0: Tuned Random Forest with more trees
* def5678 v2.0: Switch to Random Forest model  
* ghi9012 v1.0: Initial Logistic Regression model
```

---

## 🔍 ทำความเข้าใจ Git Checkout

### Git Checkout คืออะไร?

`git checkout` เป็นคำสั่งที่ใช้สำหรับ:

1. **สลับ branch** - `git checkout <branch-name>`
2. **ย้อนกลับไปดู commit เก่า** - `git checkout <commit-hash>`
3. **กู้คืนไฟล์** - `git checkout <commit> -- <file>`

---

## ⚠️ Detached HEAD State

### ขั้นตอนที่ 6: เข้าสู่ Detached HEAD State

> 📌 **จุดประสงค์:** ทดลองย้อนกลับไปดู commit เก่า และเข้าใจ Detached HEAD
> 
> เมื่อเรา checkout ไปที่ **commit โดยตรง** (ไม่ใช่ branch) Git จะเข้าสู่สถานะพิเศษที่เรียกว่า **Detached HEAD**
>
> **ทำไมต้องทำ:** ในการทำงานจริง เราอาจต้องย้อนกลับไปดูโค้ดเก่า เช่น "v1.0 เขียนยังไงนะ?"

ลองย้อนกลับไปดู Commit แรก (v1.0):

```bash
# ดู commit hash ก่อน
git log --oneline

# checkout ไปที่ commit แรก (ใส่ hash ที่ได้จาก git log เช่น ghi9012)
git checkout ghi9012
```

**⚠️ คุณจะเห็นข้อความเตือน:**

```
Note: switching to 'ghi9012'.

You are in 'detached HEAD' state. You can look around, make experimental
changes and commit them, and you can discard any commits you make in this
state without impacting any branches by switching back to a branch.

If you want to create a new branch to retain commits you create, you may
do so (now or later) by using -c with the switch command. Example:

  git switch -c <new-branch-name>

Or undo this operation with:

  git switch -

HEAD is now at ghi9012 v1.0: Initial Logistic Regression model
```

---

### 📖 Detached HEAD หมายความว่าอย่างไร?

```
ปกติ (HEAD ชี้ไปที่ Branch):
                                    
    main (branch)
       ↓
    [v1.0] --- [v2.0] --- [v3.0]
                             ↑
                           HEAD
                           
Detached HEAD (HEAD ชี้ตรงไปที่ Commit):

    main (branch)
                             ↓
    [v1.0] --- [v2.0] --- [v3.0]
       ↑
     HEAD (detached!)
```

**สรุปง่ายๆ:**
- **ปกติ**: HEAD → Branch → Commit
- **Detached**: HEAD → Commit (ไม่ผ่าน Branch)

---

### ขั้นตอนที่ 7: ตรวจสอบสถานะ Detached HEAD

> 📌 **จุดประสงค์:** ยืนยันว่าเราอยู่ในสถานะ Detached HEAD จริง
> 
> คำสั่ง `git status` จะบอกว่าเราอยู่ที่ไหน ถ้าเห็น "HEAD detached at ..." แสดงว่าเราไม่ได้อยู่บน branch ใดๆ
>
> **ลองรันโค้ด:** เมื่อ checkout ไป commit เก่า ไฟล์ทั้งหมดจะกลับไปเป็นเหมือนตอนนั้น!

```bash
# ตรวจสอบสถานะ
git status
```

**ผลลัพธ์:**
```
HEAD detached at ghi9012
nothing to commit, working tree clean
```

```bash
# ดูว่า HEAD ชี้ไปที่ไหน
git log --oneline -1

# ทดสอบรันโค้ด v1.0
python train_model.py
# จะเห็น Logistic Regression
```

---

### ขั้นตอนที่ 8: ทดลองแก้ไขในสถานะ Detached HEAD

> 📌 **จุดประสงค์:** ทดลองแก้ไขโค้ดและ commit ในสถานะ Detached HEAD
> 
> นี่คือสถานการณ์จริงที่เจอบ่อย: "อยากลองแก้โค้ดเก่าดูว่าผลลัพธ์จะดีขึ้นไหม"
>
> **สิ่งที่จะเกิดขึ้น:** เราสามารถแก้ไขและ commit ได้ แต่ commit นั้นจะ **ไม่อยู่บน branch ใดเลย!**
>
> **การทดลอง:** เราจะลองเปลี่ยน solver ของ Logistic Regression จาก default เป็น 'saga'

ลองแก้ไขโค้ดขณะอยู่ใน Detached HEAD:

```bash
cat > train_model.py << 'EOF'
# train_model.py - Experimental: Logistic Regression with different solver
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

def train():
    iris = load_iris()
    X, y = iris.data, iris.target
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # ทดลองใช้ solver อื่น
    model = LogisticRegression(solver='saga', max_iter=500)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"Experimental Model: LogisticRegression (saga solver)")
    print(f"Accuracy: {round(accuracy, 4)}")
    
    return accuracy

if __name__ == "__main__":
    train()
EOF
```

```bash
# ทดสอบการทดลอง
python train_model.py

# Commit การทดลอง
git add train_model.py
git commit -m "Experiment: Try saga solver"
```

---

### ขั้นตอนที่ 9: ดู History หลังจาก Commit ใน Detached HEAD

> 📌 **จุดประสงค์:** เห็นปัญหาของการ commit ใน Detached HEAD
> 
> เมื่อดู graph จะเห็นว่า commit ใหม่ **แยกออกมาจาก main** และไม่ได้อยู่บน branch ใด
>
> **⚠️ อันตราย:** ถ้าเรา checkout ไปที่อื่นโดยไม่สร้าง branch เก็บไว้ commit นี้อาจหายได้!

```bash
git log --oneline --all --graph
```

**ผลลัพธ์:**

```
* xyz7890 (HEAD) Experiment: Try saga solver
| * abc1234 (main) v3.0: Tuned Random Forest with more trees
| * def5678 v2.0: Switch to Random Forest model
|/
* ghi9012 v1.0: Initial Logistic Regression model
```

**สังเกต:** Commit ใหม่ไม่ได้อยู่บน branch ใดเลย!

---

## 🆘 วิธีจัดการกับ Detached HEAD

> 📌 **ปัญหา:** เรา commit ไปแล้วในสถานะ Detached HEAD ถ้าไม่ทำอะไร commit นี้อาจหายได้
>
> **ทางออก:** สร้าง branch ใหม่เพื่อ "จับ" commit นี้ไว้ ทำให้มันปลอดภัยและสามารถกลับมาดูได้ตลอด

### สร้าง Branch เก็บการทดลอง (Recommended)

ถ้าต้องการเก็บการทดลองไว้:

```bash
# สร้าง branch ใหม่จากตำแหน่งปัจจุบัน
git checkout -b experiment/saga-solver

# ตอนนี้การทดลองจะถูกเก็บไว้อย่างปลอดภัย
git log --oneline -3
```

**กลับไป main:**

```bash
git checkout main
```

---

## 🧪 แบบฝึกหัดเพิ่มเติม

### แบบฝึกหัดที่ 1: เปรียบเทียบ Model Versions

```bash
# ดู commit hash ทั้งหมดก่อน
git log --oneline

# ดูความแตกต่างระหว่าง commit (ใส่ hash จริงที่ได้)
# เช่น เปรียบเทียบ commit แรก กับ commit ที่สอง
git diff ghi9012 def5678 -- train_model.py

# เปรียบเทียบ commit ที่สอง กับ commit ที่สาม
git diff def5678 abc1234 -- train_model.py
```

---

### แบบฝึกหัดที่ 2: กู้ไฟล์จาก Commit เก่า

```bash
# กู้เฉพาะไฟล์ train_model.py จาก commit แรก โดยไม่ต้อง checkout ทั้งหมด
# (ใส่ hash ของ commit แรก)
git checkout ghi9012 -- train_model.py

# ดูว่าไฟล์เปลี่ยนแปลง
git status
```

**ถ้าต้องการยกเลิก:**

```bash
git checkout main -- train_model.py
```

---

## 📝 สรุปคำสั่งสำคัญ

| คำสั่ง | การใช้งาน |
|--------|-----------|
| `git checkout <branch>` | สลับไปยัง branch |
| `git checkout <commit-hash>` | ไปดู commit เฉพาะ (Detached HEAD) |
| `git checkout HEAD~N` | ไปดู N commits ก่อนหน้า (Detached HEAD) |
| `git checkout -b <new-branch>` | สร้าง branch ใหม่จากตำแหน่งปัจจุบัน |
| `git checkout <commit> -- <file>` | กู้ไฟล์จาก commit เก่า |
| `git switch -` | กลับไป branch ก่อนหน้า |
| `git status` | ตรวจสอบสถานะ (รวมถึง Detached HEAD) |

---

## ⚡ เคล็ดลับสำหรับ MLOps

1. **ใช้ Commit Message ที่มีความหมาย**: ระบุ version และการเปลี่ยนแปลงชัดเจน
2. **อย่า Commit บน Detached HEAD**: ควรสร้าง branch ก่อน
3. **ใช้ Branch สำหรับ Experiments**: แยกการทดลองออกจาก main
4. **รวม Git กับ MLflow**: Track ทั้งโค้ดและ metrics

---

## ❓ คำถามทบทวน

1. Detached HEAD state เกิดขึ้นเมื่อใด?
2. จะเกิดอะไรขึ้นถ้าเรา commit ใน Detached HEAD แล้วสลับไป branch อื่น?
3. วิธีใดที่ปลอดภัยที่สุดในการทดลองโค้ดเก่า?
4. `HEAD~2` หมายถึงอะไร?

---

## 📚 แหล่งเรียนรู้เพิ่มเติม

- [Git Documentation - git-checkout](https://git-scm.com/docs/git-checkout)
- [Atlassian - Git Checkout](https://www.atlassian.com/git/tutorials/using-branches/git-checkout)
- [Pro Git Book (ฟรี)](https://git-scm.com/book/en/v2)

---
