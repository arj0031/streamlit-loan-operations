"""Standalone Loan Operations Portal Streamlit application."""
from __future__ import annotations

import streamlit as st

from operations_portal import render_operations_portal
from styles import operations_brand, theme_css

st.set_page_config(
    page_title="Loan Operations Portal | MuleSoft demonstration",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(f"<style>{theme_css(True)}</style>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown(operations_brand(), unsafe_allow_html=True)
    st.markdown(
        '<div style="position:fixed;bottom:36px;left:25px;right:20px;color:#6f8b7c;font-size:8px;font-weight:700;letter-spacing:1.4px">DEMO WORKSPACE</div>'
        '<div style="position:fixed;bottom:16px;left:25px;right:20px;padding-top:12px;border-top:1px solid rgba(216,235,224,.12);color:#e3eee7;font-size:10px"><strong>Loan operations</strong><br><span style="color:#84a090;font-size:9px">Back-office view</span></div>',
        unsafe_allow_html=True,
    )

render_operations_portal()
