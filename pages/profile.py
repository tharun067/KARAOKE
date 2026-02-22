import streamlit as st
from shared_config import apply_page_config, apply_custom_css
from auth.auth_utils import is_authenticated, current_user, is_admin
from services.song_service import get_all_songs

# Apply configuration
apply_page_config()
apply_custom_css()

if not is_authenticated():
    st.markdown(
        """
        <div style='text-align:center; padding:2rem; background:linear-gradient(135deg, rgba(102, 126, 234, 0.15), rgba(118, 75,162, 0.15)); 
                    border-radius:16px; border:2px solid rgba(102, 126, 234, 0.3);'>
            <div style='font-size:3rem; margin-bottom:1rem;'>🔒</div>
            <h3 style='color:#667eea;'>Access Restricted</h3>
            <p style='color:#ccc;'>Please log in to view your profile.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.stop()

user = current_user()

# Header
st.markdown(
    """
    <div style='text-align:center; padding:1.5rem 0; margin-bottom:2rem;'>
        <h1 style='font-size:2.5rem; color:#667eea; font-weight:800;'>
            👤 My Profile
        </h1>
        <p style='color:#ccc; font-size:1rem;'>Manage your account and view your activity</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Profile Card
col1, col2 = st.columns([1, 2])

with col1:
    # Avatar with gradient
    initial = user['name'][0].upper()
    st.markdown(
        f"""
        <div style='text-align:center;'>
            <div style='
                background: linear-gradient(135deg, #667eea, #764ba2);
                border-radius: 50%;
                width: 150px; 
                height: 150px;
                display: flex; 
                align-items: center; 
                justify-content: center;
                font-size: 4rem; 
                font-weight: 700;
                margin: auto;
                color: white;
                box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
            '>
                {initial}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    role_emoji = "🛡️" if is_admin() else "🎵"
    role_text = "Admin" if is_admin() else "User"
    role_color = "#667eea" if is_admin() else "#f093fb"
    
    st.markdown(
        f"""
        <div style='padding:1.5rem; background:linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1)); 
                    border-radius:16px; border:2px solid rgba(102, 126, 234, 0.3);'>
            <h2 style='margin:0; color:#667eea; font-size:2rem;'>{user['name']}</h2>
            <div style='margin-top:1rem; font-size:1.1rem;'>
                <div style='display:flex; align-items:center; gap:0.5rem; margin-bottom:0.8rem;'>
                    <span style='font-size:1.3rem;'>📧</span>
                    <span style='color:#ccc;'>{user['email']}</span>
                </div>
                <div style='display:flex; align-items:center; gap:0.5rem; margin-bottom:0.8rem;'>
                    <span style='font-size:1.3rem;'>{role_emoji}</span>
                    <span style='background:rgba(102, 126, 234, 0.2); padding:0.3rem 0.8rem; border-radius:8px; color:{role_color}; font-weight:600;'>{role_text}</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Member since
joined = user.get("created_at", "")[:10]
if joined:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style='text-align:center; padding:1rem; background:rgba(240, 147, 251, 0.05); 
                    border-radius:12px; border:2px solid rgba(240, 147, 251, 0.2);'>
            <span style='color:#ccc;'>Member since</span>
            <span style='color:#f093fb; font-weight:600; margin-left:0.5rem;'>{joined}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br><br>", unsafe_allow_html=True)

# Activity Stats
st.markdown("### 📊 Your Activity")
all_songs = get_all_songs()
my_songs = [s for s in all_songs if s.get("uploaded_by") == user["id"]]

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        f"""
        <div style='text-align:center; padding:2rem; background:linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(102, 126, 234, 0.05)); 
                    border-radius:16px; border:2px solid rgba(102, 126, 234, 0.3);'>
            <div style='font-size:3rem; margin-bottom:0.5rem;'>🎵</div>
            <div style='font-size:2.5rem; font-weight:700; color:#667eea;'>{len(my_songs)}</div>
            <div style='color:#ccc; margin-top:0.5rem; font-size:1rem;'>Songs Uploaded</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div style='text-align:center; padding:2rem; background:linear-gradient(135deg, rgba(118, 75, 162, 0.2), rgba(118, 75, 162, 0.05)); 
                    border-radius:16px; border:2px solid rgba(118, 75, 162, 0.3);'>
            <div style='font-size:3rem; margin-bottom:0.5rem;'>📚</div>
            <div style='font-size:2.5rem; font-weight:700; color:#764ba2;'>{len(all_songs)}</div>
            <div style='color:#ccc; margin-top:0.5rem; font-size:1rem;'>Total Library Songs</div>
        </div>
        """,
        unsafe_allow_html=True
    )

if my_songs:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🎼 My Uploads")
    st.markdown("<br>", unsafe_allow_html=True)
    
    for s in my_songs:
        st.markdown(
            f"""
            <div style='padding:1rem 1.5rem; background:linear-gradient(135deg, #1e1e30, #2a2a40); 
                        border-radius:12px; border:2px solid rgba(102, 126, 234, 0.2); 
                        margin-bottom:0.8rem; display:flex; justify-content:space-between; align-items:center;'>
                <div style='flex:1;'>
                    <div style='font-size:1.1rem; font-weight:600; color:#f0f0f0;'>{s['title']}</div>
                    <div style='color:#ccc; margin-top:0.3rem;'>🎤 {s['artist']}</div>
                </div>
                <div style='background:rgba(102, 126, 234, 0.2); padding:0.5rem 1rem; border-radius:8px;'>
                    <span style='color:#667eea; font-weight:600;'>{s.get('genre', 'Other')}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
else:
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("📭 You haven't uploaded any songs yet. If you're an admin, visit the Upload page!")
