# =========================================================
# frontend/streamlit_admin.py
# Admin Login / Signup + Dashboard
# =========================================================

import streamlit as st
import requests

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="Admin | CodeDoc AI", layout="wide")

# -----------------------------
# SESSION STATE
# -----------------------------
if "admin_token" not in st.session_state:
    st.session_state.admin_token = None

if "admin_page" not in st.session_state:
    st.session_state.admin_page = "auth"  # auth | dashboard


# =========================================================
# AUTH PAGE (LOGIN / SIGNUP)
# =========================================================
if st.session_state.admin_page == "auth":
    st.title("🛠️ CodeDoc AI – Admin Portal")

    tab1, tab2 = st.tabs(["Admin Login", "Admin Signup"])

    # ---------- LOGIN ----------
    with tab1:
        email = st.text_input("Admin Email", key="admin_login_email")
        password = st.text_input("Password", type="password", key="admin_login_pass")

        if st.button("Login as Admin"):
            res = requests.post(
                f"{API_BASE}/auth/login",
                json={"email": email, "password": password}
            )

            if res.status_code == 200:
                token = res.json()["access_token"]

                # Quick admin check
                headers = {"Authorization": f"Bearer {token}"}
                test = requests.get(f"{API_BASE}/admin/metrics", headers=headers)

                if test.status_code == 200:
                    st.session_state.admin_token = token
                    st.session_state.admin_page = "dashboard"
                    st.success("Admin login successful")
                    st.rerun()
                else:
                    st.error("❌ Not an admin account")
            else:
                st.error(res.text)

    # ---------- SIGNUP ----------
    with tab2:
        email = st.text_input("Admin Email", key="admin_signup_email")
        password = st.text_input("Password", type="password", key="admin_signup_pass")

        if st.button("Create Admin Account"):
            res = requests.post(
                f"{API_BASE}/auth/signup",
                json={
                    "email": email,
                    "password": password,
                    "is_admin": True
                }
            )

            if res.status_code == 200:
                st.success("Admin account created. Please login.")
            else:
                st.error(res.text)


# =========================================================
# ADMIN DASHBOARD
# =========================================================
if st.session_state.admin_page == "dashboard":
    headers = {
        "Authorization": f"Bearer {st.session_state.admin_token}"
    }

    st.sidebar.success("Admin Logged In")

    if st.sidebar.button("Logout"):
        st.session_state.admin_token = None
        st.session_state.admin_page = "auth"
        st.rerun()

    st.title("📊 Admin Dashboard")

    # -----------------------------
    # METRICS
    # -----------------------------
    metrics_res = requests.get(f"{API_BASE}/admin/metrics", headers=headers)

    if metrics_res.status_code != 200:
        st.error("Unauthorized or backend error")
        st.stop()

    metrics = metrics_res.json()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Users", metrics["total_users"])
    col2.metric("Total Projects", metrics["total_projects"])
    col3.metric("Active Projects", metrics["active_projects"])

    st.divider()

    # -----------------------------
    # PROJECTS
    # -----------------------------
    st.subheader("📦 Projects")

    projects = requests.get(
        f"{API_BASE}/admin/projects",
        headers=headers
    ).json()

    for p in projects:
        with st.expander(f"#{p['id']} — {p['name']}"):
            st.write(f"Status: **{p['status']}**")
            st.write(f"Owner ID: {p['owner_id']}")

            if st.button("🗑 Delete Project", key=f"del_proj_{p['id']}"):
                requests.delete(
                    f"{API_BASE}/admin/projects/{p['id']}",
                    headers=headers
                )
                st.warning("Project deleted")
                st.rerun()

    st.divider()

    # -----------------------------
    # USERS
    # -----------------------------
    st.subheader("👤 Users")

    users = requests.get(
        f"{API_BASE}/admin/users",
        headers=headers
    ).json()

    for u in users:
        with st.expander(f"{u['email']}"):
            st.write(f"User ID: {u['id']}")
            st.write(f"Admin: {u['is_admin']}")

            if not u["is_admin"]:
                if st.button("❌ Delete User", key=f"del_user_{u['id']}"):
                    requests.delete(
                        f"{API_BASE}/admin/users/{u['id']}",
                        headers=headers
                    )
                    st.warning("User deleted")
                    st.rerun()

    st.sidebar.caption("CodeDoc AI • Admin © 2026")
