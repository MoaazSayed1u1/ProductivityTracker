import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def get_supabase() -> Client:
    url = st.secrets["https://opycvzajctmrsqhhthth.supabase.co"]
    key = st.secrets["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9weWN2emFqY3RtcnNxaGh0aHRoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODUwNjU4MzQsImV4cCI6MjEwMDY0MTgzNH0.GJKeNKdtHps7YZj8yh8JZZ5t-4xU7437Ti2kDMxo_iw"]

    return create_client(url, key)