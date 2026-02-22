import streamlit as st
from shared_config import apply_page_config, apply_custom_css
from services.user_service import authenticate_user
from auth.auth_utils import login_user

# Apply configuration
apply_page_config()
apply_custom_css()

st.markdown(
    """
    <div style='text-align:center; padding:1.5rem 0; margin-bottom:2rem;'>
        <h1 style='font-size:2.5rem; color:#667eea; font-weight:800;'>
            🔐 Login to Karaoke
        </h1>
        <p style='color:#ccc; font-size:1rem;'>Access your music library and start singing!</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.form("login_form"):
    email = st.text_input("📧 Email", placeholder="you@example.com")
    password = st.text_input("🔑 Password", type="password")
    submitted = st.form_submit_button("Login 🚀", use_container_width=True, type="primary")

if submitted:
    if not email or not password:
        st.error("⚠️ Please fill in all fields.")
        st.stop()
    with st.spinner("🔓 Authenticating…"):
        user = authenticate_user(email.strip().lower(), password)
    if user:
        login_user(user)
        st.session_state["page"] = "home"
        st.success(f"✅ Welcome back, **{user['name']}**! 🎵")
        st.rerun()
    else:
        st.error("❌ Invalid email or password.")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    """
    <div style='text-align:center; padding:1rem; background:rgba(240, 147, 251, 0.05); 
                border-radius:12px; border:2px solid rgba(240, 147, 251, 0.2);'>
        <span style='color:#ccc;'>Don't have an account?</span>
        <span style='color:#f093fb; font-weight:600; margin-left:0.5rem;'>Use the Register option in the sidebar.</span>
    </div>
    """,
    unsafe_allow_html=True
)
