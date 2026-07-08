import streamlit as st

st.set_page_config(page_title="Splunk Hub", page_icon="🏠", layout="centered")

st.title("⚡ Splunk Core Certified User Training Portal")
st.markdown("### Welcome to your interactive command center.")
st.write("Use the sidebar on the left to navigate between the live practice engine and your diagnostic performance analytics.")

st.markdown("---")

# Visual Quick-Link Cards
col1, col2 = st.columns(2)

with col1:
    st.info("### 📝 Exam Simulator")
    st.write("Test your knowledge with 212 structured exam questions, instant feedback, and core logic tracking.")

with col2:
    st.success("### 📈 Analytics Suite")
    st.write("Review real-time performance graphs, tracking modules, and accuracy drill-downs.")