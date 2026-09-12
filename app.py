import streamlit as st
import pandas as pd
import joblib
import numpy as np

# --------------------------------------------------
# Load trained model
# --------------------------------------------------

model = joblib.load("models/isolation_forest_model.pkl")


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Network Anomaly Detection",
    page_icon="🔍",
    layout="wide"
)


# --------------------------------------------------
# App Title
# --------------------------------------------------

st.title("🔍 AI-Based Network Anomaly Detection")

st.write(
    "Upload network traffic data to detect unusual patterns "
    "using an Isolation Forest machine learning model."
)

st.success("Model loaded successfully!")


# --------------------------------------------------
# File Upload
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload a CSV file",
    type=["csv"]
)


if uploaded_file is not None:

    # Read uploaded CSV
    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")

    st.dataframe(
        df.head(),
        use_container_width=True
    )

    st.write(
        "Dataset Shape:",
        df.shape
    )


    # --------------------------------------------------
    # Prepare Features
    # --------------------------------------------------

    columns_to_remove = [
        "Attack Type",
        "Prediction",
        "Anomaly_Score"
    ]

    X = df.drop(
        columns=[
            col
            for col in columns_to_remove
            if col in df.columns
        ],
        errors="ignore"
    )

    # Keep only numeric features
    X = X.select_dtypes(
        include=[np.number]
    )

    st.write(
        "Features used for prediction:",
        X.shape[1]
    )


    # --------------------------------------------------
    # Check Feature Count
    # --------------------------------------------------

    if X.shape[1] != 52:

        st.error(
            f"Expected 52 features, but found {X.shape[1]} numeric features."
        )

        st.stop()


    # --------------------------------------------------
    # Detect Anomalies
    # --------------------------------------------------

    if st.button(
        "🔍 Detect Anomalies",
        type="primary"
    ):

        # Model prediction
        predictions = model.predict(X)

        # Anomaly scores
        anomaly_scores = model.decision_function(X)


        # Convert predictions
        result = np.where(
            predictions == -1,
            "Anomaly",
            "Normal"
        )


        # Create result dataframe
        result_df = df.copy()

        result_df["Prediction"] = result

        result_df["Anomaly_Score"] = anomaly_scores


        # --------------------------------------------------
        # Calculate Metrics
        # --------------------------------------------------

        total_records = len(result_df)

        anomaly_count = (
            result == "Anomaly"
        ).sum()

        normal_count = (
            result == "Normal"
        ).sum()

        anomaly_percentage = (
            anomaly_count / total_records
        ) * 100


        # --------------------------------------------------
        # Dashboard Metrics
        # --------------------------------------------------

        st.subheader("Detection Summary")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total Records",
            f"{total_records:,}"
        )

        col2.metric(
            "Normal",
            f"{normal_count:,}"
        )

        col3.metric(
            "Anomalies",
            f"{anomaly_count:,}"
        )

        col4.metric(
            "Anomaly %",
            f"{anomaly_percentage:.2f}%"
        )


        # --------------------------------------------------
        # Anomaly Distribution
        # --------------------------------------------------

        st.subheader("Anomaly Distribution")

        chart_data = pd.DataFrame(
            {
                "Status": [
                    "Normal",
                    "Anomaly"
                ],
                "Count": [
                    normal_count,
                    anomaly_count
                ]
            }
        )

        st.bar_chart(
            chart_data.set_index("Status")
        )


        # --------------------------------------------------
        # Anomaly Score Distribution
        # --------------------------------------------------

        st.subheader("Anomaly Score Distribution")

        score_data = pd.DataFrame(
            {
                "Anomaly Score": anomaly_scores
            }
        )

        st.line_chart(
            score_data
        )


        # --------------------------------------------------
        # Detection Results
        # --------------------------------------------------

        st.subheader("Detection Results")

        st.dataframe(
            result_df.head(100),
            use_container_width=True
        )


        # --------------------------------------------------
        # Show Only Anomalies
        # --------------------------------------------------

        st.subheader("Detected Anomalies")

        anomaly_df = result_df[
            result_df["Prediction"] == "Anomaly"
        ]

        st.dataframe(
            anomaly_df.head(100),
            use_container_width=True
        )


        # --------------------------------------------------
        # Download Results
        # --------------------------------------------------

        csv = result_df.to_csv(
            index=False
        )

        st.download_button(
            label="⬇️ Download Results CSV",
            data=csv,
            file_name="anomaly_detection_results.csv",
            mime="text/csv"
        )