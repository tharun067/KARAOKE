# 🎤 Karaoke Music Streaming App

A fully functional, cloud-based music streaming web application built with **Streamlit** + **Supabase**, converted from the original Tkinter desktop app.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🔐 Authentication | Register / Login / Logout with bcrypt password hashing |
| 🛡️ Role-Based Access | Admin (upload + delete) vs User (listen only) |
| 🎵 Music Library | Search, filter by artist & genre, paginated list |
| ▶️ Audio Player | Built-in HTML5 player, plays directly from cloud |
| ⬆️ Song Upload | Admin uploads MP3/WAV → stored in Supabase Storage |
| ☁️ Cloud Database | Supabase (PostgreSQL) — free tier, persistent |
| 🎨 Modern Dark UI | Custom CSS, gradient sidebar, card layout |

---

## 🚀 Quick Setup

### 1. Create a Supabase Project (free)

1. Go to [supabase.com](https://supabase.com) and create a free account
2. Click **New Project**
3. Note your **Project URL** and **anon/public key** from:
   - `Project Settings → API`

### 2. Create the Database Schema

In your Supabase project, go to **SQL Editor** and run:

```sql
-- Users table
CREATE TABLE IF NOT EXISTS users (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name        TEXT NOT NULL,
    email       TEXT UNIQUE NOT NULL,
    password    TEXT NOT NULL,
    role        TEXT NOT NULL DEFAULT 'user',
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- Songs table
CREATE TABLE IF NOT EXISTS songs (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title        TEXT NOT NULL,
    artist       TEXT NOT NULL DEFAULT 'Unknown',
    album        TEXT NOT NULL DEFAULT 'Unknown',
    genre        TEXT NOT NULL DEFAULT 'Other',
    duration     REAL,
    file_url     TEXT NOT NULL,
    uploaded_by  UUID REFERENCES users(id) ON DELETE SET NULL,
    created_at   TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_songs_title  ON songs (title);
CREATE INDEX IF NOT EXISTS idx_songs_artist ON songs (artist);
CREATE INDEX IF NOT EXISTS idx_songs_genre  ON songs (genre);
CREATE INDEX IF NOT EXISTS idx_users_email  ON users  (email);
```

### 3. Create the Storage Bucket

In Supabase → **Storage** → **New Bucket**:
- Name: `audio`
- Public: **Yes** ✅

### 4. Configure Secrets

Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml`:

```toml
SUPABASE_URL = "https://your-project-id.supabase.co"
SUPABASE_ANON_KEY = "your-anon-key"
ADMIN_CODE = "your-secret-admin-code"
```

### 5. Install Dependencies & Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 📁 Project Structure

```
music_app/
├── app.py                  # Main entry point & router
├── requirements.txt
│
├── .streamlit/
│   └── secrets.toml        # API keys (never commit this!)
│
├── database/
│   ├── db.py               # Supabase client + schema SQL
│
├── auth/
│   └── auth_utils.py       # Password hashing, session helpers
│
├── services/
│   ├── user_service.py     # User DB operations
│   └── song_service.py     # Song DB + Storage operations
│
└── pages/
    ├── home.py             # Landing / dashboard
    ├── login.py            # Login form
    ├── register.py         # Registration form
    ├── library.py          # Music library + player
    ├── upload.py           # Song upload (admin only)
    └── profile.py          # User profile
```

---

## 🌐 Deploy to Streamlit Cloud (Free)

1. Push this project to a **GitHub repo**
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo and select `app.py` as the entry file
4. Under **Secrets**, paste your `secrets.toml` contents
5. Click **Deploy** 🎉

Your app will be live at `https://your-app.streamlit.app`

---

## 🛡️ Admin vs User Roles

| Action | User | Admin |
|---|---|---|
| Browse & listen | ✅ | ✅ |
| Search & filter | ✅ | ✅ |
| Upload songs | ❌ | ✅ |
| Delete songs | ❌ | ✅ |
| View profile | ✅ | ✅ |

To make someone an admin, either:
- Enter the **Admin Code** during registration (set in `secrets.toml`)
- Or manually update the `role` column in Supabase Table Editor

---

## 🔧 Environment Variables

| Variable | Required | Description |
|---|---|---|
| `SUPABASE_URL` | ✅ | Your Supabase project URL |
| `SUPABASE_ANON_KEY` | ✅ | Supabase anon/public key |
| `ADMIN_CODE` | Optional | Secret code to register as admin |

---

## 📦 Dependencies

```
streamlit       – Web framework
supabase        – Database + Storage client
bcrypt          – Password hashing
python-dotenv   – .env file support
mutagen         – MP3 duration extraction
```
