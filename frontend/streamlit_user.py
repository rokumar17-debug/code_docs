# =========================================================
# frontend/streamlit_user.py
# User-facing Streamlit UI
# =========================================================

import streamlit as st
import requests
import time

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="CodeDoc AI", layout="wide")

# -----------------------------
# AUTH SECTION
# -----------------------------
st.title("📘 CodeDoc AI – Intelligent Codebase Documentation")

st.sidebar.header("🔐 Authentication")

token = st.sidebar.text_input("JWT Token", type="password")
headers = {"Authorization": f"Bearer {token}"} if token else {}

if not token:
    st.info("Please login via backend and paste your JWT token here.")
    st.stop()

# -----------------------------
# PROJECT CREATION
# -----------------------------
st.header("📦 Create New Project")

with st.form("create_project"):
    project_name = st.text_input("Project Name")
    persona = st.selectbox("Target Persona", ["SDE", "PM", "BOTH"])
    uploaded_file = st.file_uploader("Upload ZIP Codebase", type=["zip"])
    submit = st.form_submit_button("Start Analysis")

if submit:
    if not project_name or not uploaded_file:
        st.error("Project name and ZIP file are required")
    else:
        files = {"file": uploaded_file}
        data = {"name": project_name, "persona": persona}

        res = requests.post(
            f"{API_BASE}/projects",
            headers=headers,
            files=files,
            data=data
        )

        if res.status_code == 200:
            st.success("Analysis started successfully")
            project_id = res.json()["project_id"]
            st.session_state["project_id"] = project_id
        else:
            st.error(res.text)

# -----------------------------
# PROGRESS MONITORING
# -----------------------------
if "project_id" in st.session_state:
    st.header("⏳ Analysis Progress")
    project_id = st.session_state["project_id"]

    progress_bar = st.progress(0)
    status_text = st.empty()

    for _ in range(100):
        res = requests.get(
            f"{API_BASE}/progress/{project_id}",
            headers=headers
        )
        if res.status_code == 200:
            data = res.json()
            progress_bar.progress(data.get("progress", 0))
            status_text.info(data.get("message", "Processing..."))

            if data.get("progress") >= 100:
                st.success("Analysis complete")
                break
        time.sleep(2)

    # Pause / Resume
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⏸ Pause"):
            requests.post(f"{API_BASE}/control/pause/{project_id}", headers=headers)
    with col2:
        if st.button("▶ Resume"):
            requests.post(f"{API_BASE}/control/resume/{project_id}", headers=headers)

# -----------------------------
# DOCUMENTATION VIEW
# -----------------------------
if "project_id" in st.session_state:
    st.header("📄 Documentation")
    project_id = st.session_state["project_id"]

    doc_type = st.radio("View Documentation", ["SDE", "PM"])

    if st.button("Load Documentation"):
        res = requests.get(
            f"{API_BASE}/docs/{project_id}/{doc_type.lower()}",
            headers=headers
        )
        if res.status_code == 200:
            report = res.json()["report"]
            diagrams = res.json().get("diagrams", [])

            st.subheader(report["title"])
            for section, content in report["sections"].items():
                st.markdown(f"### {section}")
                st.write(content)

            st.subheader("📊 Diagrams")
            for d in diagrams:
                st.markdown(d)
        else:
            st.error(res.text)

# -----------------------------
# SEMANTIC SEARCH
# -----------------------------
if "project_id" in st.session_state:
    st.header("🔎 Semantic Code Search")
    query = st.text_input("Ask about the codebase")

    if st.button("Search"):
        res = requests.get(
            f"{API_BASE}/search",
            params={"project_id": st.session_state["project_id"], "q": query},
            headers=headers
        )
        if res.status_code == 200:
            for r in res.json():
                st.code(r["file"])
                st.write(r["snippet"])
        else:
            st.error(res.text)

st.sidebar.markdown("---")
st.sidebar.caption("CodeDoc AI – User Interface")
