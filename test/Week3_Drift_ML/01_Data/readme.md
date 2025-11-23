
# 🔬 เครื่องมือสำหรับตรวจสอบ Data Drift

---

## 1. **Kolmogorov–Smirnov (KS) Test**

📌 ใช้สำหรับ: **ข้อมูลเชิงตัวเลข (continuous features)**

* หลักการ: ทดสอบว่า distribution ของ **Reference (Train Data)** และ **Current (Production Data)** ต่างกันหรือไม่
* Output:

  * **p-value < 0.05** → มีความแตกต่าง (Drift)
  * **p-value ≥ 0.05** → distribution ใกล้เคียงกัน (No Drift)

```python
from scipy.stats import ks_2samp

ks_stat, p_value = ks_2samp(df_ref["age"], df_cur["age"])
print("KS Test p-value:", p_value)
```

---

## 2. **Chi-Square Test**

📌 ใช้สำหรับ: **ข้อมูลเชิงหมวดหมู่ (categorical features)**

* หลักการ: สร้างตาราง cross-tab (contingency table) แล้ววัดว่าการแจกแจงของ category เปลี่ยนไปหรือไม่
* Output:

  * **p-value < 0.05** → distribution ของหมวดหมู่เปลี่ยนไป (Drift)
  * **p-value ≥ 0.05** → ยังเหมือนเดิม

```python
from scipy.stats import chi2_contingency
import pandas as pd

contingency = pd.crosstab(df_ref["gender"], df_cur["gender"])
chi2, p_value, dof, expected = chi2_contingency(contingency)
print("Chi-Square p-value:", p_value)
```

---

## 3. **Jensen–Shannon Divergence (JSD)**

📌 ใช้สำหรับ: **วัดความแตกต่างระหว่าง distribution สองชุด** (ต่อเนื่องหรือตัวเลขที่ discretize ได้)

* ค่าอยู่ระหว่าง **0 ถึง 1**

  * **ใกล้ 0** → distribution คล้ายกัน
  * **ใกล้ 1** → distribution แตกต่างมาก
  * **ใช้เกณฑ์แนะนำ** > 0.10 ถือว่ามี drift เชิงปฏิบัติ

```python
from scipy.spatial.distance import jensenshannon
import numpy as np

# Histogram normalization
ref_hist, _ = np.histogram(df_ref["age"], bins=20, density=True)
cur_hist, _ = np.histogram(df_cur["age"], bins=20, density=True)

jsd = jensenshannon(ref_hist, cur_hist)
print("Jensen-Shannon Divergence:", jsd)
```

---

## 4. **Population Stability Index (PSI)**

📌 ใช้สำหรับ: **งานด้านการเงิน/การธนาคาร** เพื่อตรวจจับการเปลี่ยน distribution ของ feature สำคัญ (เช่น credit score)

* ค่า interpretation:

  * **PSI < 0.1** → Stable (ไม่มี drift)
  * **0.1 ≤ PSI < 0.25** → Moderate drift
  * **PSI ≥ 0.25** → Significant drift

```python
def calculate_psi(expected, actual, buckets=10):
    import numpy as np
    breakpoints = np.linspace(0, 100, buckets + 1)
    expected_percents = np.histogram(expected, bins=np.percentile(expected, breakpoints))[0] / len(expected)
    actual_percents = np.histogram(actual, bins=np.percentile(expected, breakpoints))[0] / len(actual)
    psi = np.sum((expected_percents - actual_percents) * np.log(expected_percents / actual_percents))
    return psi

psi_value = calculate_psi(df_ref["age"], df_cur["age"])
print("PSI:", psi_value)
```

---

# ✅ สรุปการใช้งาน

| เครื่องมือ     | ใช้กับ                           | ผลลัพธ์    | การตีความ                 |
| -------------- | -------------------------------- | ---------- | ------------------------- |
| **KS Test**    | ตัวเลข (continuous)              | p-value    | p < 0.05 → Drift          |
| **Chi-Square** | หมวดหมู่ (categorical)           | p-value    | p < 0.05 → Drift          |
| **JSD**        | Distribution (ต่อเนื่อง/ดิสกรีต) | ค่า 0–1    | 0 = คล้ายกัน, 1 = ต่างกัน |
| **PSI**        | การเงิน / credit scoring         | ค่า > 0.25 | Drift รุนแรง              |

