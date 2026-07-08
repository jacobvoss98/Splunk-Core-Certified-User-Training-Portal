import streamlit as st
import pandas as pd

st.set_page_config(page_title="Analytics Center", page_icon="📈", layout="wide")

st.title("📊 Diagnostic Performance Analytics")
st.markdown("---")

if "history" not in st.session_state or len(st.session_state.history) == 0:
    st.warning("No performance data generated yet! Go complete some quiz questions first to see your metrics populate.")
else:
    df = pd.DataFrame(st.session_state.history)
    
    # 1. High-Level Summary Metrics
    total_answered = len(df)
    correct_count = len(df[df["status"] == "Correct"])
    accuracy_rate = (correct_count / total_answered) * 100
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Answers Logged", f"{total_answered}")
    m2.metric("Total Correct Solutions", f"{correct_count}")
    m3.metric("Global Accuracy", f"{round(accuracy_rate, 1)}%")
    
    st.markdown("---")
    
    # 2. Group Metrics Separated by Quiz 1-11
    st.subheader("Quiz-by-Quiz Performance Analysis")
    
    # Grouping logic to build scorecard map per Quiz ID
    quiz_summary = df.groupby("quiz_id").agg(
        Total_Attempted=("status", "count"),
        Correct_Answers=("status", lambda x: (x == "Correct").sum())
    ).reset_index()
    
    quiz_summary["Accuracy %"] = round((quiz_summary["Correct_Answers"] / quiz_summary["Total_Attempted"]) * 100, 1)
    quiz_summary.columns = ["Quiz ID", "Total Questions Tried", "Correct Answers", "Accuracy Score (%)"]
    
    # Set index for cleaner native charting
    chart_df = quiz_summary.set_index("Quiz ID")
    
    # Render an interactive comparative breakdown graph
    st.bar_chart(chart_df["Accuracy Score (%)"])
    
    # Display the clean formatted data summary matrix underneath
    st.subheader("Quiz Report Card Matrix")
    st.dataframe(quiz_summary, hide_index=True, use_container_width=True)