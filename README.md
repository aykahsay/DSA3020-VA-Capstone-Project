## **DSA3020 VA Capstone Project**
### Project Overview

This project aims to **predict weekly average maize prices** in selected counties in Kenya using historical retail and wholesale price data. The project applies **machine learning** to forecast prices, helping farmers, traders, and policymakers make informed decisions.

The project uses the **CRISP-DM methodology** and follows an end-to-end ML pipeline—from problem definition and data collection to model deployment and evaluation.


![Python](https://img.shields.io/badge/python-3.10-blue) ![License](https://img.shields.io/badge/license-MIT-green)

### Table of Contents

1. [Project Overview](#project-overview)
2. [Problem Statement](#problem-statement)
3. [Data Description](#data-description)
4. [Methodology](#methodology)
5. [Model Development & Evaluation](#model-development--evaluation)
6. [Results and Discussion](#results-and-discussion)
7. [Conclusion & Future Work](#conclusion--future-work)
8. [Folder Structure](#folder-structure)
9. [Getting Started](#getting-started)
10. [References](#references)

---

## Problem Statement

Smallholder farmers across Africa often face **price volatility** and **post-harvest losses** of up to 40%. **agriBORA**, a Kenyan agri-tech startup, provides certified warehouses where farmers can safely store maize, obtain digital warehouse certificates, access loans, and choose the optimal selling time. Accurate market price information is crucial for farmers to make informed decisions and maximize returns.

This project focuses on using **historical maize prices in Kenya** to develop a **machine learning solution** for forecasting weekly market prices. The solution aims to support farmers in counties including **Kiambu, Kirinyaga, Mombasa, Nairobi, and Uasin-Gishu**.

**Objective:**

* Predict **average weekly prices of dry maize** using historical data and relevant external features (e.g., weather, NDVI).
* Generate forecasts for **two consecutive weeks** at each prediction step.
* Forecasting period: **6 consecutive weeks from November 17, 2025, to January 10, 2026**.

**Impact:**
Accurate forecasts will help farmers:

* Time their maize sales effectively.
* Increase earnings.
* Strengthen agriBORA’s integrated storage, credit, and market intelligence services.
---

### Datasets

#### Primary Sources

1. **KAMIS Data:** Historical wholesale and retail prices of white, yellow, and mixed-traditional maize (2021–2025).
2. **agriBORA Data:** Transaction-level weekly wholesale prices (main dataset for forecasting).

#### Features

| Feature                  | Description                                              |
| ------------------------ | -------------------------------------------------------- |
| Commodity_Classification | Type of maize (Dry_White, Dry_Yellow, Mixed_Traditional) |
| Commodity                | High-level classification (Dry_Maize)                    |
| Classification           | Sub-type (White, Yellow, Mixed)                          |
| County                   | County where market is located                           |
| Market                   | Market name                                              |
| Date                     | Transaction date                                         |
| Year, Month, WeekofYear  | Time features                                            |
| SupplyVolume             | Quantity supplied                                        |
| Retail                   | Retail price per Kg                                      |
| Wholesale                | Wholesale price per Kg                                   |
| Unit                     | Unit of measurement                                      |

Here’s a polished and professional **README** draft for your GitHub project, incorporating the information you provided and structuring it in a way that’s clear, informative, and appealing to potential users or collaborators:

---

### Methodology

The project follows the **CRISP-DM (Cross-Industry Standard Process for Data Mining)** framework:

1. **Business Understanding:**

   * Identify price prediction as a regression problem.
   * Clearly define objectives to forecast maize prices for targeted counties.

2. **Data Understanding & Preprocessing:**

   * Clean, merge, and explore KAMIS and agriBORA datasets.
   * Handle missing values, anomalies, and outliers.
   * Add time-based features (week of year, month, etc.).

3. **Modeling:**

   * Compare multiple regression models (e.g., Linear Regression, Random Forest, Gradient Boosting, LSTM for time series).
   * Feature engineering to improve predictive power.
     
4. **Evaluation & Tuning:**

   * Use cross-validation and appropriate regression metrics (RMSE, MAE, R²).
   * This project uses multi-metric evaluation. There are two error metrics: Mean Absolute Error (MAE) and Root Mean Square Error (RMSE).
   * MAE (50%): measures the average magnitude of errors between predicted and actual values. This metric is less sensitive to outliers compared to other error metrics such as Mean Squared Error (MSE). It is a suitable choice for financial forecasting.
RMSE (50%): measures the deviation of your predictions from the actual values, but penalises large errors more heavily.
   * Fine-tune hyperparameters and interpret results in a business context.
   
This project forecasts weekly white maize prices in selected Kenyan counties (Kiambu, Kirinyaga, Mombasa, Nairobi, Uasin-Gishu) using KAMIS and AgriBORA datasets. Historical prices were aggregated weekly, and lag features were created to improve predictions.

## Modeling Approach

* **Linear Regression (LR):** Captures overall price trends using lag features.
* **Random Forest (RF):** Captures short-term fluctuations but may **overfit**, performing exceptionally on training data but less accurately on unseen weeks.

## Model Performance

| Model | Training MAE | Test MAE | Training R² | Test R² |
| ----- | ------------ | -------- | ----------- | ------- |
| LR    | 3.41         | 2.39     | 0.91        | 0.78    |
| RF    | 1.75         | 4.14     | 0.98        | 0.67    |

> **Overfitting and under Fitting :** Random Forest fits the training data closely, capturing every fluctuation. This can lead to poor generalization on new or unseen data, as reflected in the higher test MAE and lower test R².

## Insights

* Lag features are strong predictors of weekly prices.
* LR is more stable for general trends, while RF is better at modeling volatility but requires careful tuning.
* Forecasting 6 weeks ahead is feasible using the trained models.
5. **Deployment:**

   * Save final model using `joblib` or `pickle`.
   * Deploy via a simple **web app** or **dashboard** (Streamlit, Flask, or FastAPI) for interactive forecasts.

---

## Folder Structure

```
DSA3020-VA-Capstone-Project/
│
├─ DATA/
│   ├─ raw/
│   │   ├─ agribora_maize_prices.csv
│   │   ├─ kamis_maize_prices_raw.csv
│   │   └─ kamis_maize_prices.csv
│   └─ database/
│       └─ crop_data.db
│
├─ src/
│   ├─ data_collection.py
│   ├─ config.py
│   └─ utils.py
│
├─ notebooks/
│   └─ EDA_and_Modeling.ipynb
│
├─ models/
│   └─ trained_model.pkl
│
├─ README.md
└─ requirements.txt
```

---

## Getting Started

**Installation:**

```bash
git clone https://github.com/<your-username>/DSA3020-VA-Capstone-Project.git
cd DSA3020-VA-Capstone-Project
pip install -r requirements.txt
```

**Usage:**

```python
from src.data_collection import MaizeDataHandler

handler = MaizeDataHandler()
df = handler.load_combined_data()  # Load and combine KAMIS + agriBORA data
df = handler.add_time_features(df)  # Add useful features

# Train and evaluate model
from src.utils import train_model
model, metrics = train_model(df, target='Wholesale')
```

---

## Deliverables

1. **Technical Report**: Includes problem statement, literature review, methodology, data description, model development, evaluation, results, discussion, and future work.
2. **Presentation/Demo**: 10–15 minute walkthrough of the solution with slides and live demo.
3. **GitHub Repository**: Well-structured code, evidence of individual contributions, and documentation.

---

## References

* KAMIS – Kenya Agricultural Market Information System
* agriBORA Data API
* Relevant academic papers on commodity price prediction and time-series forecasting
