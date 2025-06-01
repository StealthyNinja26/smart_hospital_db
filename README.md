# 🏥 Smart Hospital DBMS

A full-stack database management system designed for a modern hospital, featuring an interactive admin dashboard, automated data simulation, and machine learning-driven insights like Length of Stay prediction.

## 📌 Features

- **Relational Database Design**: ER-modeled PostgreSQL schema representing real-world hospital operations.
- **Simulated Data Generation**: Python scripts to populate the database with realistic patient, staff, appointment, and treatment data.
- **Streamlit Dashboard**: A clean, multi-tabbed interface for admin-level visibility across:
  - Hospital overview
  - Patient and staff records
  - Department workloads and room occupancy
  - Length of Stay Estimation using machine learning
- **ML Integration**: Trained regression model to estimate patient length of stay based on admission and clinical features.

## 🚀 Tech Stack

- **Backend**: PostgreSQL
- **Frontend**: Streamlit
- **Data Analysis & ML**: Pandas, scikit-learn, Plotly
- **Python Libraries**: psycopg2, joblib

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/smart-hospital-dbms.git
cd smart-hospital-dbms
````

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install pandas streamlit psycopg2-binary scikit-learn plotly joblib
```

### 3. Set Up PostgreSQL Database

* Ensure PostgreSQL is installed and running.
* Create the database:

```sql
CREATE DATABASE "Smart_Hospital_DB";
```

* Run your schema SQL file or execute the table creation and data simulation scripts.

### 4. Run the Dashboard

```bash
streamlit run dashboard.py
```

## 🔍 ML Model Details

The `Length of Stay Estimator` uses a trained `RandomForestRegressor` model. Key features used:

* Room Type
* Insurance ID
* Number of procedures and diagnoses

Pre-trained model stored in:

* `length_of_stay_model.pkl`

## 📊 Dashboard Preview

Dashboard Overview Screenshot <img width="1247" alt="overview" src="https://github.com/user-attachments/assets/56440b77-8d25-41d0-aa25-045bf2e7b72c" />

Patients Tab Screenshot <img width="1247" alt="patients" src="https://github.com/user-attachments/assets/ff1683dd-e8c0-4085-813a-179147899544" />

Staff Tab Screenshot <img width="1246" alt="staff" src="https://github.com/user-attachments/assets/6fe9db42-3829-4721-acc3-bd165fae1ab9" />

Insights Tab Screenshot ![insights](https://github.com/user-attachments/assets/f5da609b-b7bc-4f01-8538-4ea459eca460)

Length Of Stay Estimator Screenshot <img width="1247" alt="Length_of_stay" src="https://github.com/user-attachments/assets/9590acc7-6fe6-45b4-b5bb-506b79871640" />


## 🤝 Acknowledgements

Built as a portfolio project to demonstrate database architecture, data engineering, and ML integration in a healthcare domain.
