# 🏦 Loan Approval Prediction — ML Project

[![Live App](https://img.shields.io/badge/🚀%20Live%20App-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)](https://loan-approved-prediction-ml-project.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.6.1-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

> A machine learning web application that predicts whether a loan application will be **approved or rejected** based on applicant information — helping financial institutions make faster, data-driven decisions.

---

## 🌐 Live Demo

👉 **[Try the App Here](https://loan-approved-prediction-ml-project.streamlit.app/)**

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Dataset](#-dataset)
- [ML Pipeline](#-ml-pipeline)
- [Getting Started](#-getting-started)
- [Usage](#-usage)
- [Results](#-results)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🔍 Overview

This end-to-end machine learning project automates loan approval decisions. Given an applicant's demographic and financial details, the model predicts the likelihood of their loan being approved. The trained pipeline is served through an interactive **Streamlit** web app, making it accessible without any coding knowledge.

---

## ✨ Features

- 📊 **Exploratory Data Analysis (EDA)** — Visual insights into loan data distributions and correlations
- 🔧 **Automated Preprocessing** — Handles missing values, categorical encoding, and feature scaling in a unified `sklearn` pipeline
- 🤖 **Classification Model** — Trained on real-world loan applicant data
- 🌐 **Interactive Web App** — Real-time predictions via a clean Streamlit UI
- 📦 **Reproducible Pipeline** — Serialized model for consistent, portable inference

---

## 🛠 Tech Stack

| Category | Tools |
|---|---|
| Language | Python 3.10+ |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| Machine Learning | scikit-learn |
| Web App | Streamlit |
| Model Persistence | Pickle |
| Dataset Source | Kaggle |

---

## 📁 Project Structure

```
Loan-Approved-Prediction-ML-Project/
│
├── Streamlit/
│   └── loan.py                  # Streamlit app — UI and prediction logic
│
├── notebooks/
│   └── loan_prediction.ipynb    # EDA, preprocessing, model training & evaluation
│
├── model/
│   └── model.pkl                # Trained scikit-learn pipeline (serialized)
│
├── data/
│   └── loan_approval_dataset.csv  # Dataset used for training
│
├── requirements.txt             # Python dependencies
├── pyproject.toml               # Project metadata
└── README.md
```

---

## 📂 Dataset

- **Source:** [Kaggle — Loan Approval Prediction Dataset](https://www.kaggle.com/datasets/muhammadmusharraf444/loan-approval-dataset)
- **Type:** Tabular, Binary Classification
- **Domain:** Lending / Finance

### Key Features

| Feature | Description |
|---|---|
| `person_age` | Age of the applicant |
| `person_income` | Annual income |
| `person_emp_length` | Employment length (years) |
| `loan_amnt` | Loan amount requested |
| `loan_int_rate` | Loan interest rate |
| `loan_percent_income` | Loan amount as % of income |
| `cb_person_cred_hist_length` | Credit history length (years) |
| `person_home_ownership` | Home ownership status |
| `loan_intent` | Purpose of the loan |
| `loan_grade` | Loan grade assigned |
| `cb_person_default_on_file` | Historical default on file |
| `loan_status` | **Target** — 0 = Rejected, 1 = Approved |

---

## ⚙️ ML Pipeline

The model is wrapped in a scikit-learn `Pipeline` with the following stages:

```
Raw Input
    │
    ▼
ColumnTransformer
    ├── OneHotEncoder   (nominal categorical features)
    ├── OrdinalEncoder  (ordinal categorical features)
    └── StandardScaler  (numerical features)
    │
    ▼
Classifier
    │
    ▼
Prediction (Approved / Rejected)
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Muhammad-Musharraf/Loan-Approved-Prediction-ML-Project.git
cd Loan-Approved-Prediction-ML-Project

# 2. Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the Streamlit app
streamlit run Streamlit/loan.py
```

The app will open at `http://localhost:8501` in your browser.

---

## 🖥 Usage

1. Open the live app or run it locally.
2. Fill in the applicant details in the sidebar or form (income, loan amount, credit history, etc.).
3. Click **Predict**.
4. The model instantly returns whether the loan would be **Approved ✅** or **Rejected ❌**.

---

## 📈 Results

The model was evaluated on a held-out test set using standard classification metrics:

| Metric | Score |
|---|---|
| Accuracy | — |
| Precision | — |
| Recall | — |
| F1-Score | — |

> 📝 See the full evaluation in [`notebooks/loan_prediction.ipynb`](notebooks/)

---

## 🐛 Troubleshooting

### `AttributeError: module 'sklearn.compose._column_transformer' has no attribute '_RemainderColsList'`

This happens when the model was saved with **scikit-learn 1.6.1** but the runtime has a newer version.

**Fix:** Pin the scikit-learn version in `requirements.txt`:

```
scikit-learn==1.6.1
```

Then redeploy. See [scikit-learn model persistence docs](https://scikit-learn.org/stable/model_persistence.html) for more details.

---

## 🤝 Contributing

Contributions are welcome! To get started:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Muhammad Musharraf**
- GitHub: [@Muhammad-Musharraf](https://github.com/Muhammad-Musharraf)
- Dataset: [Kaggle Profile](https://www.kaggle.com/muhammadmusharraf444)

---

<p align="center">
  Made with ❤️ using Python & Streamlit
</p>
---
## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.
