import streamlit as st
import pandas as pd
import requests

st.title("Upload CSV and Get Predictions")

st.header("Inference")
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    # Read CSV
    df = pd.read_csv(uploaded_file)
    st.write("Uploaded Data:")
    st.dataframe(df.head())

    # Send to FastAPI backend
    if st.button("Get Predictions"):
        # Convert dataframe to JSON
        payload = df.to_dict(orient="records")
        response = requests.post("http://localhost:8000/predict", json=payload)

        if response.status_code == 200:
            predictions = response.json()
            st.write("Predictions:")
            st.dataframe(pd.DataFrame(predictions))
        else:
            st.error(f"Error: {response.status_code} - {response.text}")

st.header("Submit Jobs")
iters = st.number_input("Iterations?", min_value=1, value=1)
input_val = st.number_input("Input value?", min_value=1, max_value=100, value=10)
if st.button("Submit"):
    response = requests.post("http://localhost:8000/submit_jobs", json={"iterations": iters, "input": input_val})
    if response.status_code == 200:
        job_ids = response.json().get("job_ids", [])
        st.write("Submitted Job IDs:")
        st.write(job_ids)
    else:
        st.error(f"Error: {response.status_code} - {response.text}")

st.header("Check jobs")
job_id = st.text_input("Enter Job ID to check status")
if st.button("Check Job Status"):
    response = requests.get(f"http://localhost:8000/job_status/{job_id}")
    if response.status_code == 200:
        status = response.json()
        st.write("Job Status:")
        st.json(status)
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
