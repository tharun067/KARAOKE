import streamlit as st
from shared_config import apply_page_config, apply_custom_css
from services.user_service import register_user
from auth.auth_utils import login_user

# Apply configuration
apply_page_config()
apply_custom_css()

st.markdown(
    """
    <div style='text-align:center; padding:1.5rem 0; margin-bottom:2rem;'>
        <h1 style='font-size:2.5rem; color:#667eea; font-weight:800;'>
            📝 Create Your Account
        </h1>
        <p style='color:#ccc; font-size:1rem;'>Join the karaoke community today!</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.form("register_form"):
    name = st.text_input("👤 Full Name", placeholder="Jane Doe")
    email = st.text_input("📧 Email", placeholder="jane@example.com")
    password = st.text_input("🔑 Password", type="password")
    confirm = st.text_input("🔒 Confirm Password", type="password")
    # First registered user becomes admin
    admin_code = st.text_input(
        "🛡️ Admin Code (optional)",
        placeholder="Leave blank for regular account",
        help="Enter the admin code if you have one.",
    )
    submitted = st.form_submit_button("✨ Create Account", use_container_width=True, type="primary")

if submitted:
    if not all([name, email, password, confirm]):
        st.error("⚠️ All fields are required.")
        st.stop()
    if password != confirm:
        st.error("❌ Passwords do not match.")
        st.stop()
    if len(password) < 6:
        st.error("❌ Password must be at least 6 characters.")
        st.stop()

    role = "admin" if admin_code == st.secrets.get("ADMIN_CODE", "karaoke-admin-2024") else "user"

    try:
        with st.spinner("🛠️ Creating account…"):
            user = register_user(name, email.strip().lower(), password, role)
        login_user(user)
        st.session_state["page"] = "home"
        st.success("✅ Account created! Welcome 🎉")
        st.rerun()
    except ValueError as e:
        st.error(f"❌ {str(e)}")
    except Exception as e:
        st.error(f"❌ Registration failed: {e}")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    """
    <div style='text-align:center; padding:1rem; background:rgba(240, 147, 251, 0.05); 
                border-radius:12px; border:2px solid rgba(240, 147, 251, 0.2);'>
        <span style='color:#ccc;'>Already have an account?</span>
        <span style='color:#f093fb; font-weight:600; margin-left:0.5rem;'>Use the Login option in the sidebar.</span>
    </div>
    """,
    unsafe_allow_html=True
)
