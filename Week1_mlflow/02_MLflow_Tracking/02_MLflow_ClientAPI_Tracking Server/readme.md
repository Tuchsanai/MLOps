# 🔬 Lab: ใช้งาน **MLflow Client API** เพื่อเชื่อมต่อ Tracking Server และสำรวจ Experiment


---

## 🎯 วัตถุประสงค์ของแลบ

หลังจบแลบนี้ คุณจะสามารถ:

* เชื่อมต่อ **MLflow Tracking Server** ด้วย `MlflowClient`
* ค้นหาและทำความเข้าใจกับ **Default Experiment**
* ดึง metadata ของ Experiment (เช่น `name`, `lifecycle_stage`)
* เตรียมความพร้อมสำหรับขั้นต่อไป (สร้าง Experiment และเริ่ม Run)

---

## 🧩 โครงสร้างเนื้อหา

1. เตรียมสภาพแวดล้อม
2. เริ่ม MLflow Tracking Server (ทางเลือก)
3. ใช้ **MlflowClient** เชื่อมต่อเซิร์ฟเวอร์
4. สำรวจ **Default Experiment** และค้นหา Experiment
5. แบบฝึกหัดเพิ่มเติม (Exercise)
6. Troubleshooting & Tips

---

## 1) เตรียมสภาพแวดล้อม

ติดตั้ง MLflow เวอร์ชันล่าสุด:

```bash
pip install --upgrade mlflow
```

> อ้างอิงขั้นตอนเริ่มต้นใช้งานจากเอกสาร MLflow: Starting the MLflow Tracking Server. ([MLflow][2])

---

## 2) เริ่ม MLflow Tracking Server (ทางเลือก)

หากคุณยังไม่มี Tracking Server ให้รันแบบ local ชั่วคราว:

```bash
mlflow server --host 127.0.0.1 --port 8080
```

* คำสั่งนี้จะเปิด **MLflow UI** ที่ `http://127.0.0.1:8080`
* ควรปล่อยหน้าต่างเทอร์มินัลนี้ทำงานตลอดระยะเวลาทดลอง (ปิดแล้วเซิร์ฟเวอร์จะหยุด) ([MLflow][2])

> หมายเหตุ: ในระบบจริงอาจใช้ **Managed/Remote Tracking Server** และตั้งค่า `MLFLOW_TRACKING_URI` ชี้ไปยังปลายทางนั้น

---

## 3) ใช้ **MlflowClient** เชื่อมต่อเซิร์ฟเวอร์

สร้างไฟล์ `lab_step2_mlflow_client.py` หรือใช้ใน Jupyter Notebook ก็ได้

```python
from mlflow import MlflowClient
from pprint import pprint

# 3.1 ระบุ URI ของ Tracking Server
# ถ้าใช้ server ที่รันจากข้อ 2:
client = MlflowClient(tracking_uri="http://127.0.0.1:8080")

# หมายเหตุ:
# - หากไม่ได้ระบุ tracking_uri และไม่ได้ตั้ง env MLFLOW_TRACKING_URI
#   MLflow จะใช้ local directory เป็น backend ตามดีฟอลต์ของระบบปัจจุบัน
```

> แนวคิดการตั้งค่า `tracking_uri` และพฤติกรรมดีฟอลต์อ้างอิงจากหน้าคู่มือ “Using the MLflow Client API”. ([MLflow][1])

---

## 4) สำรวจ **Default Experiment** และค้นหา Experiment

เมื่อ Tracking Server เริ่มต้นใหม่ จะมี **Default** experiment ให้เสมอ (id = `0`) เพื่อรองรับกรณีที่เรายังไม่ได้สร้าง experiment ของตัวเอง—ข้อมูล run จะไม่หายไป ([MLflow][1])

```python
# 4.1 ค้นหา experiments ทั้งหมดบน server
all_experiments = client.search_experiments()
print(all_experiments)
```

**ตัวอย่างเอาต์พุตที่คาดหวัง** (จะแตกต่างกันได้ตามระบบ):

```
[<Experiment: artifact_location='./mlruns/0', creation_time=None,
  experiment_id='0', last_update_time=None,
  lifecycle_stage='active', name='Default', tags={}>]
```

ดึงเฉพาะฟิลด์ที่สนใจจากอ็อบเจ็กต์ `Experiment`:

```python
default_experiment = [
    {"name": exp.name, "lifecycle_stage": exp.lifecycle_stage}
    for exp in all_experiments
    if exp.name == "Default"
][0]

pprint(default_experiment)
# ตัวอย่างผลลัพธ์:
# {'name': 'Default', 'lifecycle_stage': 'active'}
```

> เมธอด `search_experiments()` คืนค่าเป็นลิสต์ของอ็อบเจ็กต์ชนิด `Experiment` (ไม่ใช่ dict ธรรมดา) ซึ่งมี metadata ให้เข้าถึงได้สะดวกในเวิร์กโฟลว์ที่ซับซ้อนยิ่งขึ้น ([MLflow][1])

---

## 5) แบบฝึกหัดเพิ่มเติม (Exercises)

1. **เปลี่ยนปลายทาง Tracking Server**

   * ตั้งค่าตัวแปรแวดล้อม (ใน shell)

     ```bash
     export MLFLOW_TRACKING_URI=http://127.0.0.1:8080
     ```
   * แล้วทดสอบสร้าง `MlflowClient()` **โดยไม่** ส่ง `tracking_uri` เพื่อดูว่าคลients์ยังเชื่อมไปที่เซิร์ฟเวอร์เดิมได้หรือไม่

2. **ตรวจสอบ Experiment อื่นๆ**

   * ใช้ MLflow UI เปิดดูรายการ Experiment และลองสร้าง Experiment ใหม่ในขั้นถัดไปของซีรีส์นี้ (เช่นหน้า “Creating Experiments”) เพื่อฝึกการจัดระเบียบงานวิจัย/โปรเจกต์หลายชุด

3. **อ่านเอกสาร API เพิ่มเติม**

   * ศึกษา `mlflow.client.MlflowClient` สำหรับ CRUD ของ Experiments/Runs/Models เพื่อเตรียมต่อยอดไปสู่การ “สร้าง Experiment” และ “เริ่ม Run” ในตอนถัดไปของคอร์สนี้. ([MLflow][3])

---

## 6) Troubleshooting & Tips

* **เชื่อมต่อไม่ได้ / 404 / Connection refused**

  * ตรวจสอบว่า `mlflow server` ยังรันอยู่ที่ `127.0.0.1:8080`
  * พอร์ตชนหรือไม่ (ลองเปลี่ยนเป็น `--port 8081`) ([MLflow][2])

* **ไม่เห็น Default Experiment**

  * ใช้ `client.search_experiments()` อีกครั้ง และตรวจว่าใช่ Tracking URI เดียวกับที่ UI เปิดอยู่หรือไม่ (คำอธิบายพฤติกรรม Default อยู่ในคู่มือส่วน Client) ([MLflow][1])

* **ทางเลือกสำหรับ scikit-learn**

  * ในขั้นต่อไปเมื่อเริ่ม run และ log โมเดล แนะนำทบทวนหน้า `mlflow.sklearn` สำหรับวิธี log/โหลดโมเดล sklearn อย่างเป็นระบบ. ([MLflow][4])

---
