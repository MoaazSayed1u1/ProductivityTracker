import streamlit as st
from database.supabase_client import get_supabase

st.title("Supabase Test")

supabase = get_supabase()

result = supabase.table("productivity").select("*").execute()

st.write(result.data)