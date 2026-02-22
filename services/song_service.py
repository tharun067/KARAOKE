import io
import streamlit as st
from database.db import get_client

BUCKET = "audio"
MAX_FILE_MB = 50




def upload_audio_file(file_bytes: bytes, filename: str) -> str:
    """Upload bytes to Supabase Storage and return the public URL."""
    client = get_client()
    path = f"songs/{filename}"
    client.storage.from_(BUCKET).upload(
        path,
        file_bytes,
        {"content-type": "audio/mpeg", "upsert": "true"},
    )
    public_url = client.storage.from_(BUCKET).get_public_url(path)
    return public_url




def add_song(
    title: str,
    artist: str,
    album: str,
    genre: str,
    duration: float,
    file_url: str,
    uploaded_by: str,
) -> dict:
    res = (
        get_client()
        .table("songs")
        .insert(
            {
                "title": title,
                "artist": artist,
                "album": album,
                "genre": genre,
                "duration": duration,
                "file_url": file_url,
                "uploaded_by": uploaded_by,
            }
        )
        .execute()
    )
    return res.data[0]


@st.cache_data(ttl=60)
def get_all_songs() -> list[dict]:
    res = (
        get_client()
        .table("songs")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )
    return res.data or []


def search_songs(query: str = "", artist: str = "", genre: str = "") -> list[dict]:
    """Filtered song list. Falls back to cached full list and filters in-Python."""
    songs = get_all_songs()
    if query:
        songs = [s for s in songs if query.lower() in s["title"].lower()]
    if artist and artist != "All":
        songs = [s for s in songs if s["artist"] == artist]
    if genre and genre != "All":
        songs = [s for s in songs if s["genre"] == genre]
    return songs


def delete_song(song_id: str) -> None:
    get_client().table("songs").delete().eq("id", song_id).execute()


def get_genres(songs: list[dict]) -> list[str]:
    return ["All"] + sorted({s["genre"] for s in songs if s.get("genre")})


def get_artists(songs: list[dict]) -> list[str]:
    return ["All"] + sorted({s["artist"] for s in songs if s.get("artist")})


def format_duration(seconds: float | None) -> str:
    if not seconds:
        return "--:--"
    m, s = divmod(int(seconds), 60)
    return f"{m:02d}:{s:02d}"
