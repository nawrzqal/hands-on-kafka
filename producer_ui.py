import requests
import streamlit as st

PRODUCER_API_URL = "http://localhost:5001"

st.set_page_config(page_title="Likes Producer", layout="centered")
st.title("Likes Producer")

col1, col2 = st.columns(2)

with col1:
    if st.button("Health Check"):
        try:
            r = requests.get(f"{PRODUCER_API_URL}/health", timeout=1)
            r.raise_for_status()
            st.success("Producer is healthy")
            st.json(r.json())
        except requests.RequestException as exc:
            st.error(f"Health check failed: {exc}")

with col2:
    if st.button("Like", type="primary"):
        try:
            r = requests.post(f"{PRODUCER_API_URL}/like", timeout=1)
            r.raise_for_status()
            st.success("Like sent")
            st.json(r.json())
        except requests.RequestException as exc:
            st.error(f"Failed to send like: {exc}")
