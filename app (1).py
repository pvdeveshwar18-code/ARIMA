Given we've been in this loop for a while, let me give you a shortcut: replace your app.py temporarily with a tiny diagnostic version that will tell you the exact error on-screen — no more log hunting.

🩺 Diagnostic app.py
Copy this ENTIRE content, on GitHub open app.py → click ✏️ Edit → delete everything → paste this → commit:

import streamlit as st
import sys, traceback, platform

st.set_page_config(page_title="XERCES Diagnostic", page_icon="🩺", layout="wide")
st.title("🩺 XERCES Deployment Diagnostic")

st.subheader("Environment")
st.write(f"**Python version:** {sys.version}")
st.write(f"**Platform:** {platform.platform()}")

st.subheader("Import checks")

modules = [
    "yfinance", "pandas", "numpy", "pytz", "plotly.graph_objects",
    "statsmodels.tsa.arima.model", "statsmodels.tsa.stattools",
    "statsmodels.tsa.holtwinters", "openpyxl", "reportlab.pdfgen",
    "nest_asyncio", "emergentintegrations.llm.chat"
]
for m in modules:
    try:
        __import__(m)
        st.success(f"✅ {m}")
    except Exception as e:
        st.error(f"❌ {m} — {type(e).__name__}: {e}")

st.subheader("XERCES modules")
for f in ["app.py", "xerces_plus.py"]:
    try:
        import os
        exists = os.path.exists(f)
        size = os.path.getsize(f) if exists else 0
        st.write(f"**{f}** — exists: {exists}, size: {size} bytes")
    except Exception as e:
        st.error(f"{f} check failed: {e}")

st.subheader("xerces_plus import test")
try:
    import xerces_plus as xp
    st.success(f"✅ xerces_plus imported. DATA_DIR = {xp.DATA_DIR}")
except Exception as e:
    st.error(f"❌ xerces_plus failed:\n\n```\n{traceback.format_exc()}\n```")

st.subheader("Secret check")
try:
    key = st.secrets.get("EMERGENT_LLM_KEY", "NOT_SET")
    if key == "NOT_SET":
        st.warning("EMERGENT_LLM_KEY secret is NOT SET")
    else:
        st.success(f"✅ EMERGENT_LLM_KEY set (starts with {key[:15]}...)")
except Exception as e:
    st.info(f"No secrets configured yet: {e}")

st.info("Once we see all green checkmarks, restore the real app.py from your GitHub history.")
