# SalaryValidator

A Python tool for validating and cleaning salary datasets. It checks for missing values, duplicates, invalid experience levels, and salary outliers, and generates a summary report with statistics and basic visualizations.

---

## Dataset

This script is tested against a dataset from **Kaggle**:  
[Kaggle – Salary Insights by Job Role](https://www.kaggle.com/datasets/zahranusrat/salary)  

⚠️ This repository does **not** include the full dataset (due to size and licensing).  
To run the validation yourself, download the dataset from Kaggle and place it in the same directory as `salary_validator.py`.

---

## Features

- Load CSV datasets.  
- Select relevant columns (`work_year`, `experience_level`, `employment_type`, `job_title`, `salary_in_usd`).  
- Detect and remove duplicate rows.  
- Check for missing values and validate experience-level values (`EN`, `MI`, `SE`, `EX`).  
- Identify salary outliers using the IQR method.  
- Generate visualizations:
  - Experience level distribution  
  - Salary distribution (histogram + boxplot)  
- Output a JSON report summarizing findings.

---

## Usage

1. Clone this repository:  
   ```bash
   git clone https://github.com/wherethecrawdadssing/SalaryValidator.git
