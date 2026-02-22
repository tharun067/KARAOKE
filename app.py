import streamlit as st
from shared_config import apply_page_config, apply_custom_css
from auth.auth_utils import current_user, is_admin
from services.song_service import get_all_songs

# Apply configuration
apply_page_config()
apply_custom_css()

# Main content
user = current_user()
songs = get_all_songs()

# Hero section with gradient background
st.markdown(
    """
    <div style='text-align:center; padding: 3rem 0 2rem; 
                background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
                border-radius: 20px; margin-bottom: 2rem;'>
        <h1 style='font-size:3.5rem; margin-bottom:0.5rem; color:#667eea; font-weight:800;'>
            🎤 KARAOKE MUSIC
        </h1>
        <p style='font-size:1.3rem; color:#ccc; font-weight:300;'>
            Your Personal Cloud Music Player
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Enhanced Stats row with icons and colors
st.markdown("### 📊 Library Statistics")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div style='text-align:center; padding:1.5rem; background:linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(102, 126, 234, 0.05)); 
                    border-radius:16px; border:2px solid rgba(102, 126, 234, 0.3);'>
            <div style='font-size:3rem;'>🎵</div>
            <div style='font-size:2.5rem; font-weight:700; color:#667eea;'>{len(songs)}</div>
            <div style='color:#ccc; margin-top:0.5rem;'>Total Songs</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    artists = {s["artist"] for s in songs if s.get("artist")}
    st.markdown(
        f"""
        <div style='text-align:center; padding:1.5rem; background:linear-gradient(135deg, rgba(118, 75, 162, 0.2), rgba(118, 75, 162, 0.05)); 
                    border-radius:16px; border:2px solid rgba(118, 75, 162, 0.3);'>
            <div style='font-size:3rem;'>🎸</div>
            <div style='font-size:2.5rem; font-weight:700; color:#764ba2;'>{len(artists)}</div>
            <div style='color:#ccc; margin-top:0.5rem;'>Artists</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    genres = {s["genre"] for s in songs if s.get("genre")}
    st.markdown(
        f"""
        <div style='text-align:center; padding:1.5rem; background:linear-gradient(135deg, rgba(240, 147, 251, 0.2), rgba(240, 147, 251, 0.05)); 
                    border-radius:16px; border:2px solid rgba(240, 147, 251, 0.3);'>
            <div style='font-size:3rem;'>🎼</div>
            <div style='font-size:2.5rem; font-weight:700; color:#f093fb;'>{len(genres)}</div>
            <div style='color:#ccc; margin-top:0.5rem;'>Genres</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)

if not user:
    st.markdown(
        """
        <div style='text-align:center; padding:2rem; background:linear-gradient(135deg, rgba(102, 126, 234, 0.15), rgba(118, 75, 162, 0.15)); 
                    border-radius:16px; border:2px solid rgba(102, 126, 234, 0.3); margin:2rem 0;'>
            <div style='font-size:2rem; margin-bottom:1rem;'>👋</div>
            <h3 style='color:#667eea;'>Get Started Today!</h3>
            <p style='color:#ccc; font-size:1.1rem;'>Log in or create an account to access your music library and start listening to amazing karaoke tracks.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.stop()

# Welcome message for logged-in users
admin_badge = " 🛡️" if is_admin() else ""
st.markdown(
    f"""
    <div style='padding:1.5rem; background:linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1)); 
                border-radius:16px; border-left:4px solid #667eea; margin:2rem 0;'>
        <h3 style='margin:0; color:#667eea;'>👋 Welcome back, {user['name']}!{admin_badge}</h3>
        <p style='color:#ccc; font-size:1.1rem;'>Ready to enjoy some karaoke music?</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if is_admin():
    st.info("🛡️ You have **Admin** access — you can upload songs from the Upload page.")

if songs:
    st.markdown("### 🆕 Recently Added Tracks")
    st.markdown("<br>", unsafe_allow_html=True)
    
    for song in songs[:5]:
        st.markdown(
            f"""
            <div style='padding:1rem 1.5rem; background:linear-gradient(135deg, #1e1e30, #2a2a40); 
                        border-radius:12px; border:2px solid rgba(102, 126, 234, 0.2); 
                        margin-bottom:1rem; display:flex; justify-content:space-between; align-items:center;'>
                <div style='flex:1;'>
                    <div style='font-size:1.1rem; font-weight:600; color:#f0f0f0;'>{song['title']}</div>
                    <div style='color:#ccc; margin-top:0.3rem;'>🎤 {song['artist']}</div>
                </div>
                <div style='background:rgba(102, 126, 234, 0.2); padding:0.5rem 1rem; border-radius:8px;'>
                    <span style='color:#667eea; font-weight:600;'>{song.get('genre','Other')}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("💡 **Tip:** Visit the Library page to browse and play all available songs!")
else:
    st.warning("📭 No songs in the library yet. Check back soon!")
