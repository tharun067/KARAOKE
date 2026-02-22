"""Shared configuration and styling for all pages."""
import streamlit as st


def apply_page_config():
    """Apply page configuration (call this first in each page)."""
    st.set_page_config(
        page_title="Karaoke Music",
        page_icon="🎤",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def apply_custom_css():
    """Apply custom CSS styling."""
    st.markdown(
        """
        <style>
        /* ── Global modern dark theme ── */
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #0a0a15 0%, #1a1a2e 100%);
            color: #f0f0f0;
        }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #16213e 0%, #0f3460 100%);
            box-shadow: 2px 0 20px rgba(0,0,0,0.3);
        }
        
        /* ── Sidebar branding ── */
        .sidebar-title {
            font-size: 2rem;
            font-weight: 900;
            text-align: center;
            color: #667eea;
            padding: 1rem 0;
            margin-bottom: 0.5rem;
            letter-spacing: 2px;
            text-shadow: 0 0 20px rgba(102, 126, 234, 0.5);
        }
        
        .user-badge {
            background: rgba(102, 126, 234, 0.15);
            border: 2px solid #667eea;
            border-radius: 12px;
            padding: 0.8rem;
            text-align: center;
            margin: 1rem 0;
        }
        
        /* ── Enhanced Cards ── */
        .song-card {
            background: linear-gradient(135deg, #1e1e30 0%, #2a2a40 100%);
            border-radius: 16px;
            padding: 1.2rem 1.5rem;
            margin-bottom: 0.8rem;
            border: 2px solid transparent;
            border-image: linear-gradient(135deg, #667eea, #764ba2) 1;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        .song-card:hover { 
            border-color: #667eea;
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        }

        /* ── Improved Buttons ── */
        .stButton > button {
            border-radius: 12px;
            transition: all 0.3s ease;
            font-weight: 600;
            border: 2px solid transparent;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
            border-color: #f093fb;
        }
        
        /* ── Navigation buttons ── */
        button[kind="secondary"] {
            background: rgba(102, 126, 234, 0.1) !important;
            border: 2px solid rgba(102, 126, 234, 0.3) !important;
        }
        
        /* ── Audio player enhancement ── */
        audio {
            width: 100%;
            border-radius: 12px;
            margin-top: 0.5rem;
            background: #1e1e30;
        }
        
        /* ── Glowing Metrics ── */
        [data-testid="metric-container"] {
            background: linear-gradient(135deg, #1e1e30 0%, #2a2a40 100%);
            border: 2px solid rgba(102, 126, 234, 0.3);
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }
        [data-testid="metric-container"]:hover {
            border-color: #667eea;
            box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
        }
        
        /* ── Input fields ── */
        input, textarea, select {
            border-radius: 12px !important;
            background-color: #1e1e30 !important;
            border: 2px solid rgba(102, 126, 234, 0.3) !important;
            color: #f0f0f0 !important;
        }
        input:focus, textarea:focus, select:focus {
            border-color: #667eea !important;
            box-shadow: 0 0 10px rgba(102, 126, 234, 0.3) !important;
        }
        
        /* ── Dividers ── */
        hr {
            border-color: rgba(102, 126, 234, 0.2) !important;
        }
        
        /* ── Hide Streamlit branding ── */
        footer { visibility: hidden; }
        #MainMenu { visibility: hidden; }
        
        /* ── Smooth animations ── */
        * {
            transition: background-color 0.2s ease, border-color 0.2s ease;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
