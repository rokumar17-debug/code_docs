import streamlit as st
import requests
import time

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="CodeDoc AI", layout="centered")

# -----------------------------
# SESSION STATE
# -----------------------------
if "token" not in st.session_state:
    st.session_state.token = None

if "page" not in st.session_state:
    st.session_state.page = "auth"

if "project_id" not in st.session_state:
    st.session_state.project_id = None


# -----------------------------
# AUTH PAGE
# -----------------------------
if st.session_state.page == "auth":
    st.title("🔐 CodeDoc AI")

    tab1, tab2 = st.tabs(["Login", "Signup"])

    # -------- LOGIN --------
    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            r = requests.post(
                f"{API_BASE}/auth/login",
                json={"email": email, "password": password},
            )

            if r.status_code == 200:
                st.session_state.token = r.json()["access_token"]
                st.session_state.page = "dashboard"
                st.success("Logged in")
                st.rerun()
            else:
                st.error(r.text)

    # -------- SIGNUP --------
    with tab2:
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_pass")

        if st.button("Create Account"):
            r = requests.post(
                f"{API_BASE}/auth/signup",
                json={"email": email, "password": password},
            )

            if r.status_code == 200:
                st.success("Account created. Please login.")
            else:
                st.error(r.text)


# -----------------------------
# DASHBOARD
# -----------------------------
if st.session_state.page == "dashboard":
    headers = {"Authorization": f"Bearer {st.session_state.token}"}

    st.sidebar.success("Logged in")

    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

    st.title("📘 CodeDoc AI Dashboard")

    # -----------------------------
    # CREATE PROJECT
    # -----------------------------
    st.header("📦 New Project")

    with st.form("create_project"):
        name = st.text_input("Project Name")
        persona = st.selectbox("Persona", ["SDE", "PM", "BOTH"])
        zip_file = st.file_uploader("Upload ZIP", type=["zip"])
        submit = st.form_submit_button("Start Analysis")

    if submit:
        if not name or not zip_file:
            st.error("All fields required")
        else:
            r = requests.post(
                f"{API_BASE}/projects",
                headers=headers,
                data={"name": name, "persona": persona},
                files={"file": zip_file},
            )

            if r.status_code == 200:
                st.session_state.project_id = r.json()["project_id"]
                st.success("Analysis started")
            else:
                st.error(r.text)

    # -----------------------------
    # PROJECT CONTROLS
    # -----------------------------
    if st.session_state.project_id:
        pid = st.session_state.project_id
        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            if st.button("⏸ Pause"):
                requests.post(
                    f"{API_BASE}/analysis/pause/{pid}",
                    headers=headers
                )

        with col2:
            if st.button("▶ Resume"):
                requests.post(
                    f"{API_BASE}/analysis/resume/{pid}",
                    headers=headers
                )

        # -----------------------------
        # PROGRESS
        # -----------------------------
        st.header("📊 Analysis Progress")
        progress_bar = st.progress(0)
        status = st.empty()

        r = requests.get(
            f"{API_BASE}/progress/{pid}",
            headers=headers
        )

        if r.status_code == 200:
            data = r.json()
            progress_bar.progress(data["progress"] / 100)
            status.info(
                f"Stage: {data['stage']} | {data['message']}"
            )

        # -----------------------------
        # DOCUMENTATION
        # -----------------------------
        st.divider()
        st.header("📄 Documentation")

        doc_type = st.radio("Select View", ["SDE", "PM"])

        if st.button("Load Docs"):
            r = requests.get(
                f"{API_BASE}/docs/{pid}/{doc_type.lower()}",
                headers=headers
            )

            if r.status_code == 200:
                report = r.json()["report"]
                st.subheader(report["title"])

                for sec, content in report["sections"].items():
                    st.markdown(f"### {sec}")
                    st.write(content)
            else:
                st.error(r.text)

        # -----------------------------
        # SEMANTIC SEARCH (IF ENABLED)
        # -----------------------------
        st.divider()
        st.header("🔎 Semantic Search")

        q = st.text_input("Ask a question about code")

        if st.button("Search"):
            r = requests.get(
                f"{API_BASE}/search",
                params={"project_id": pid, "q": q},
                headers=headers
            )

            if r.status_code == 200:
                for res in r.json():
                    st.code(res["file"])
                    st.write(res["snippet"])
            else:
                st.error(r.text)

    st.sidebar.caption("CodeDoc AI Rohit Kumar © 2026")
