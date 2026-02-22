import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

_client: Client | None = None


def _get_secret(key: str) -> str:
    """Try Streamlit secrets first, then env vars."""
    try:
        import streamlit as st
        val = st.secrets.get(key, "")
        if val:
            return val
    except Exception:
        pass
    return os.environ.get(key, "")


def get_client() -> Client:
    """Return a singleton Supabase client."""
    global _client
    if _client is None:
        url = _get_secret("SUPABASE_URL")
        # Use service role key to bypass RLS (safe in server-side Streamlit)
        key = _get_secret("SUPABASE_SERVICE_ROLE_KEY") or _get_secret("SUPABASE_ANON_KEY")
        if not url or not key:
            raise EnvironmentError(
                "SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in .env"
            )
        _client = create_client(url, key)
    return _client



SCHEMA_SQL = """
-- Users table
CREATE TABLE IF NOT EXISTS users (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name        TEXT NOT NULL,
    email       TEXT UNIQUE NOT NULL,
    password    TEXT NOT NULL,          -- bcrypt hash
    role        TEXT NOT NULL DEFAULT 'user',   -- 'admin' | 'user'
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- Songs metadata table
CREATE TABLE IF NOT EXISTS songs (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title        TEXT NOT NULL,
    artist       TEXT NOT NULL DEFAULT 'Unknown',
    album        TEXT NOT NULL DEFAULT 'Unknown',
    genre        TEXT NOT NULL DEFAULT 'Other',
    duration     REAL,                  -- seconds
    file_url     TEXT NOT NULL,         -- Supabase Storage public URL
    uploaded_by  UUID REFERENCES users(id) ON DELETE SET NULL,
    created_at   TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_songs_title  ON songs (title);
CREATE INDEX IF NOT EXISTS idx_songs_artist ON songs (artist);
CREATE INDEX IF NOT EXISTS idx_songs_genre  ON songs (genre);
CREATE INDEX IF NOT EXISTS idx_users_email  ON users  (email);

-- Supabase Storage bucket  (run via Storage UI or this SQL)
-- INSERT INTO storage.buckets (id, name, public)
-- VALUES ('audio', 'audio', true)
-- ON CONFLICT DO NOTHING;
"""
