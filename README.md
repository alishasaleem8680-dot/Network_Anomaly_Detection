# 🔍 AI-Based Network Anomaly Detection

An AI-based network anomaly detection system that uses **Unsupervised Machine Learning** to identify unusual network traffic patterns.

The project uses **Isolation Forest** for anomaly detection and provides an interactive **Streamlit web application** where users can upload network traffic data and view detected anomalies.

---

## 📌 Project Overview

Network traffic datasets can contain both normal and malicious activity.

In this project, an **Isolation Forest** model is trained without using attack labels during training. The model learns patterns from network traffic features and identifies unusual observations as potential anomalies.

The project includes:

- Data preprocessing
- Exploratory data analysis
- Feature preparation
- Unsupervised machine learning
- Isolation Forest model
- Model evaluation
- Anomaly score analysis
- Streamlit web application
- Downloadable detection results

---

## 🎯 Problem Statement

The goal of this project is to detect unusual network traffic patterns using an unsupervised machine learning approach.

Instead of directly training the model to classify known attack types, the model learns the general structure of network traffic and identifies observations that appear different from normal patterns.

---

## 📊 Dataset

The project uses a cleaned version of the **CIC-IDS2017** network traffic dataset.

The dataset contains network flow features such as:

- Destination Port
- Flow Duration
- Total Forward Packets
- Total Backward Packets
- Packet Length Statistics
- Flow Bytes/s
- Flow Packets/s
- TCP Flag Counts
- Active and Idle Time Statistics

### Dataset Statistics

After removing duplicate rows:

- Total Records: 2,520,590
- Features: 52
- Missing Values: 0
- Infinite Values: 0
- Duplicate Rows Removed: 161

The dataset contains normal traffic and multiple attack categories including:

- DoS
- DDoS
- Port Scanning
- Brute Force
- Web Attacks
- Bots

---

## 🧹 Data Preprocessing

The following preprocessing steps were performed:

1. Loaded the cleaned CIC-IDS2017 dataset.
2. Checked missing values.
3. Checked infinite values.
4. Removed duplicate rows.
5. Separated features from the `Attack Type` label.
6. Converted numerical features to `float32`.
7. Prepared the dataset for Isolation Forest.

StandardScaler was not used because Isolation Forest is a tree-based algorithm and does not require feature scaling in the same way as distance-based algorithms.

---

## 🤖 Machine Learning Model

### Isolation Forest

The project uses **Isolation Forest**, an unsupervised machine learning algorithm designed for anomaly detection.

The model was trained using:

- 200,000 randomly selected training samples
- 100 estimators
- `contamination="auto"`
- Random state: 42

The `Attack Type` column was not used during model training.

---

## 📈 Model Evaluation

For evaluation, a separate sample of 100,000 records was used.

Although the model is unsupervised, the available dataset labels were used **after prediction** to compare the detected anomalies with known attack/normal labels.

### Results

| Metric | Score |
|---|---:|
| Accuracy | 82.91% |
| Precision | 49.24% |
| Recall | 32.35% |
| F1 Score | 39.05% |

### Confusion Matrix

- True Negatives: 77,433
- False Positives: 5,645
- False Negatives: 11,447
- True Positives: 5,475

These results represent an initial unsupervised baseline. The relatively low recall shows that the current model does not detect all known attacks and can be improved with further feature engineering and anomaly-threshold tuning.

---

## 📊 Anomaly Detection

The model produces:

- `Normal` predictions
- `Anomaly` predictions
- Anomaly scores

For Isolation Forest:

- `1` = Normal
- `-1` = Anomaly

The `decision_function` produces anomaly scores where lower values indicate observations that are more anomalous.

---

## 🌐 Streamlit Application

The project includes an interactive Streamlit application.

Users can:

1. Upload a CSV file.
2. View the dataset preview.
3. Run anomaly detection.
4. View total records.
5. View normal traffic count.
6. View detected anomaly count.
7. View anomaly percentage.
8. Explore anomaly charts.
9. View detected anomalies.
10. Download the detection results as a CSV file.

The application is designed as a demonstration of the trained machine learning model and is not intended to replace a production network security monitoring system.

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Seaborn
- Joblib
- Streamlit
- Jupyter Notebook
- Git & GitHub

---

## 📁 Project Structure

```text
Network_Anomaly_Detection/
│
├── data/
│   └── cicids2017_cleaned.csv
│
├── notebooks/
│   └── network_anomaly_detection.ipynb
│
├── models/
│   └── isolation_forest_model.pkl
│
├── reports/
│   ├── anomaly_distribution.png
│   ├── anomaly_score_distribution.png
│   ├── confusion_matrix.png
│   └── anomaly_detection_results.csv
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore