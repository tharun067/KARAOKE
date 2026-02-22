import streamlit as st
from shared_config import apply_page_config, apply_custom_css
from services.song_service import search_songs, get_all_songs, get_genres, get_artists, format_duration, delete_song
from auth.auth_utils import is_admin, is_authenticated

# Apply configuration
apply_page_config()
apply_custom_css()

SONGS_PER_PAGE = 10

if not is_authenticated():
    st.markdown(
        """
        <div style='text-align:center; padding:2rem; background:linear-gradient(135deg, rgba(102, 126, 234, 0.15), rgba(118, 75, 162, 0.15)); 
                    border-radius:16px; border:2px solid rgba(102, 126, 234, 0.3);'>
            <div style='font-size:3rem; margin-bottom:1rem;'>🔒</div>
            <h3 style='color:#667eea;'>Access Restricted</h3>
            <p style='color:#ccc;'>Please log in to view the music library.</p>
        </div>
        """,
            unsafe_allow_html=True
    )
    st.stop()

st.markdown(
    """
    <div style='text-align:center; padding:1.5rem 0; margin-bottom:1.5rem;'>
        <h1 style='font-size:2.5rem; color:#667eea; font-weight:800;'>
            🎵 Music Library
        </h1>
        <p style='color:#ccc; font-size:1rem;'>Browse and play your favorite karaoke tracks</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Enhanced Filters ──────────────────────────────────────────────────────
all_songs = get_all_songs()
genres  = get_genres(all_songs)
artists = get_artists(all_songs)

st.markdown("### 🔍 Search & Filter")
col1, col2, col3 = st.columns([3, 2, 2])
with col1:
    query = st.text_input("🔍 Search songs", placeholder="Enter song title...", label_visibility="collapsed")
with col2:
    sel_artist = st.selectbox("🎸 Artist", artists, label_visibility="collapsed")
with col3:
    sel_genre = st.selectbox("🎼 Genre", genres, label_visibility="collapsed")

songs = search_songs(
    query=query,
    artist="" if sel_artist == "All" else sel_artist,
    genre="" if sel_genre == "All" else sel_genre,
)

st.markdown(
    f"""
    <div style='padding:0.8rem 1rem; background:rgba(102, 126, 234, 0.1); border-radius:8px; 
                border-left:4px solid #667eea; margin:1rem 0;'>
        <span style='font-weight:600; color:#667eea;'>📊 {len(songs)}</span> 
        <span style='color:#ccc;'>song(s) found</span>
    </div>
    """,
    unsafe_allow_html=True
)

if not songs:
    st.markdown(
        """
        <div style='text-align:center; padding:2rem; background:rgba(240, 147, 251, 0.05); 
                    border-radius:12px; border:2px dashed rgba(240, 147, 251, 0.3); margin:2rem 0;'>
            <div style='font-size:3rem; margin-bottom:1rem;'>🔍</div>
            <h4 style='color:#f093fb;'>No Results Found</h4>
            <p style='color:#ccc;'>Try adjusting your search filters.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.stop()


total_pages = max(1, (len(songs) - 1) // SONGS_PER_PAGE + 1)
if "lib_page" not in st.session_state:
    st.session_state["lib_page"] = 1
page = st.session_state["lib_page"]
page_songs = songs[(page - 1) * SONGS_PER_PAGE : page * SONGS_PER_PAGE]

# ── Enhanced Song cards ───────────────────────────────────────────────────
for idx, song in enumerate(page_songs):
    st.markdown(
        f"""
        <div style='padding:1.2rem; background:linear-gradient(135deg, #1e1e30, #2a2a40); 
                    border-radius:12px; border:2px solid rgba(102, 126, 234, 0.2); 
                        margin-bottom:1rem; transition: all 0.3s;'>
                <div style='display:flex; align-items:center; justify-content:space-between;'>
                    <div style='flex:1; display:flex; align-items:center; gap:1rem;'>
                        <div style='font-size:1.5rem;'>🎵</div>
                        <div>
                            <div style='font-size:1.1rem; font-weight:600; color:#f0f0f0;'>{song['title']}</div>
                            <div style='color:#ccc; margin-top:0.2rem;'>🎤 {song['artist']} • {song.get('album', 'Unknown')}</div>
                        </div>
                    </div>
                    <div style='display:flex; gap:1rem; align-items:center;'>
                        <div style='background:rgba(102, 126, 234, 0.2); padding:0.4rem 0.8rem; border-radius:8px;'>
                            <span style='color:#667eea; font-weight:600; font-size:0.9rem;'>{song.get('genre', 'Other')}</span>
                        </div>
                        <div style='color:#ccc; font-size:0.9rem;'>{format_duration(song.get("duration"))}</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    if st.button(f"▶ Play", key=f"play_{song['id']}", use_container_width=False):
            st.session_state["now_playing"] = song
            st.rerun()

    # ── Pagination controls ───────────────────────────────────────────────────
    if total_pages > 1:
        st.markdown("<br>", unsafe_allow_html=True)
        pcol1, pcol2, pcol3 = st.columns([1, 2, 1])
        with pcol1:
            if page > 1:
                if st.button("⬅️ Previous", use_container_width=True, type="secondary"):
                    st.session_state["lib_page"] -= 1
                    st.rerun()
        with pcol2:
            st.markdown(
                f"<div style='text-align:center; padding:0.5rem; color:#667eea; font-weight:600;'>Page {page} of {total_pages}</div>",
                unsafe_allow_html=True
            )
        with pcol3:
            if page < total_pages:
                if st.button("Next ➡️", use_container_width=True, type="secondary"):
                    st.session_state["lib_page"] += 1
                    st.rerun()

    # ── Now playing player ────────────────────────────────────────────────────
    np = st.session_state.get("now_playing")
    if np:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div style='padding:1.5rem; background:linear-gradient(135deg, rgba(102, 126, 234, 0.15), rgba(118, 75, 162, 0.15)); 
                        border-radius:16px; border:2px solid #667eea; margin:1rem 0;'>
                <div style='font-size:1.8rem; margin-bottom:0.5rem;'>🎧 Now Playing</div>
                <div style='font-size:1.3rem; font-weight:700; color:#667eea;'>{np['title']}</div>
                <div style='color:#ccc; margin-top:0.3rem; font-size:1rem;'>
                    🎤 {np['artist']} • {np.get('album', 'Single')} • <span style='color:#f093fb;'>{np.get('genre', 'Other')}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.audio(np["file_url"], format="audio/mp3")

        if is_admin():
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🗑️ Delete this song", key="delete_now_playing", type="secondary"):
                try:
                    delete_song(np["id"])
                    st.session_state.pop("now_playing", None)
                    # Bust cache
                    get_all_songs.clear()
                    st.success("✅ Song deleted successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Delete failed: {e}")
