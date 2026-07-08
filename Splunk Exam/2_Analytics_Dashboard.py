import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Analytics Center", page_icon="📈", layout="wide")

st.title("📊 Permanent Performance Dashboard")
st.markdown("---")

try:
    # Read live attempts straight from Google Sheets cloud storage
    conn = st.connection("gsheets", type=GSheetsConnection)
    attempts_df = conn.read(ttl=0) # ttl=0 ensures it clears cache and pulls live rows
except Exception as e:
    st.error(f"Could not connect to database sheet: {e}")
    st.stop()

if attempts_df.empty or "Quiz ID" not in attempts_df.columns:
    st.warning("📊 Your Cloud Database is connected but empty! Complete a quiz to see your scores saved here forever.")
else:
    st.sidebar.title("Filter Options")
    unique_quizzes = sorted(list(attempts_df["Quiz ID"].dropna().unique()))
    filter_option = st.sidebar.selectbox("Select View:", ["All Quizzes"] + unique_quizzes)
    
    if filter_option == "All Quizzes":
        display_df = attempts_df
        st.subheader("📈 Global Accuracy Progression Timeline")
    else:
        display_df = attempts_df[attempts_df["Quiz ID"] == filter_option]
        st.subheader(f"📈 Accuracy Progression Timeline for {filter_option}")

    total_runs = len(display_df)
    
    # Ensure accuracy data column calculations are evaluated as numeric floats
    display_df["Accuracy (%)"] = pd.to_numeric(display_df["Accuracy (%)"], errors='coerce')
    avg_accuracy = display_df["Accuracy (%)"].mean()
    
    c1, c2 = st.columns(2)
    c1.metric(f"Total Completed Runs ({filter_option})", f"{total_runs}")
    c2.metric(f"Average Accuracy ({filter_option})", f"{round(avg_accuracy, 1)}%" if not pd.isna(avg_accuracy) else "0.0%")
    
    st.markdown("---")
    
    # Chart plotting mapping timeline
    chart_data = display_df.dropna(subset=["Accuracy (%)"]).copy()
    chart_data["Attempt Number"] = range(1, len(chart_data) + 1)
    chart_data = chart_data.set_index("Attempt Number")
    
    if not chart_data.empty:
        st.line_chart(data=chart_data["Accuracy (%)"], use_container_width=True)
    
    st.markdown("---")
    
    st.subheader(f"🗃️ Cloud Registry Log: {filter_option}")
    st.dataframe(display_df.iloc[::-1], hide_index=True, use_container_width=True)