import io
import streamlit as st
from shared_config import apply_page_config, apply_custom_css
from auth.auth_utils import is_authenticated, is_admin, current_user
from services.song_service import upload_audio_file, add_song, get_all_songs, MAX_FILE_MB

# Apply configuration
apply_page_config()
apply_custom_css()

try:
    from mutagen.mp3 import MP3
    from mutagen.easyid3 import EasyID3
    MUTAGEN_OK = True
except ImportError:
    MUTAGEN_OK = False

GENRES = [
    "Pop", "Rock", "Hip-Hop", "R&B", "Jazz", "Classical",
    "Country", "Electronic", "Reggae", "Metal", "Folk", "Other",
]


def _get_duration(file_bytes: bytes) -> float | None:
    if not MUTAGEN_OK:
        return None
    try:
        audio = MP3(io.BytesIO(file_bytes))
        return audio.info.length
    except Exception:
        return None


# Authentication checks
if not is_authenticated():
    st.markdown(
        """
        <div style='text-align:center; padding:2rem; background:linear-gradient(135deg, rgba(102, 126, 234, 0.15), rgba(118, 75, 162, 0.15)); 
                    border-radius:16px; border:2px solid rgba(102, 126, 234, 0.3);'>
            <div style='font-size:3rem; margin-bottom:1rem;'>🔒</div>
            <h3 style='color:#667eea;'>Access Restricted</h3>
            <p style='color:#ccc;'>Please log in to upload songs.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.stop()
    
if not is_admin():
    st.markdown(
        """
        <div style='text-align:center; padding:2rem; background:linear-gradient(135deg, rgba(240, 147, 251, 0.15), rgba(240, 147, 251, 0.05)); 
                    border-radius:16px; border:2px solid rgba(240, 147, 251, 0.3);'>
            <div style='font-size:3rem; margin-bottom:1rem;'>🛡️</div>
            <h3 style='color:#f093fb;'>Admin Access Required</h3>
            <p style='color:#ccc;'>Only admins can upload songs. Contact an admin to get access.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.stop()

st.markdown(
    """
    <div style='text-align:center; padding:1.5rem 0; margin-bottom:2rem;'>
        <h1 style='font-size:2.5rem; color:#667eea; font-weight:800;'>
            ⬆️ Upload a Song
        </h1>
        <p style='color:#ccc; font-size:1rem;'>Allowed formats: .mp3, .wav  |  Max size: 50 MB</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.form("upload_form", clear_on_submit=True):
    audio_file = st.file_uploader("🎵 Choose audio file", type=["mp3", "wav"])

    col1, col2 = st.columns(2)
    with col1:
        title  = st.text_input("Song Title *", placeholder="Selfish Love")
        artist = st.text_input("Artist *", placeholder="Demo Romeo")
    with col2:
        album  = st.text_input("Album", placeholder="Single")
        genre  = st.selectbox("Genre", GENRES)

    submitted = st.form_submit_button("🚀 Upload Song", use_container_width=True, type="primary")

if submitted:
    if not audio_file:
        st.error("⚠️ Please select an audio file.")
        st.stop()
    if not title or not artist:
        st.error("⚠️ Song title and artist are required.")
        st.stop()

    file_bytes = audio_file.read()
    size_mb = len(file_bytes) / (1024 * 1024)
    if size_mb > MAX_FILE_MB:
        st.error(f"❌ File too large ({size_mb:.1f} MB). Max {MAX_FILE_MB} MB.")
        st.stop()

    with st.spinner("📤 Uploading…"):
        try:
            # Sanitise filename
            safe_name = audio_file.name.replace(" ", "_")
            url = upload_audio_file(file_bytes, safe_name)

            duration = _get_duration(file_bytes)
            user = current_user()
            add_song(
                title=title.strip(),
                artist=artist.strip(),
                album=album.strip() or "Single",
                genre=genre,
                duration=duration,
                file_url=url,
                uploaded_by=user["id"],
            )
            get_all_songs.clear()   # Bust cache
            st.success(f"✅ **{title}** by *{artist}* uploaded successfully!")
            st.balloons()
        except Exception as e:
            st.error(f"❌ Upload failed: {e}")
