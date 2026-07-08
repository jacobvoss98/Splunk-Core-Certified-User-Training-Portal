import streamlit as st
import pandas as pd

st.set_page_config(page_title="Analytics Center", page_icon="📈", layout="wide")

st.title("📊 Quiz Performance History by Number")
st.markdown("---")

if "quiz_attempts" not in st.session_state or len(st.session_state.quiz_attempts) == 0:
    st.warning("No finalized quiz attempts found! Complete all questions in any quiz to generate a timestamped attempt snapshot.")
else:
    # 1. Parse historical attempts structure straight into Pandas
    attempts_df = pd.DataFrame(st.session_state.quiz_attempts)
    
    # 2. Add Quiz Filtering Sidebar Options
    st.sidebar.title("Filter Options")
    unique_quizzes = sorted(list(attempts_df["Quiz ID"].unique()))
    filter_option = st.sidebar.selectbox("Select View:", ["All Quizzes"] + unique_quizzes)
    
    # Filter dataframe based on user choice
    if filter_option == "All Quizzes":
        display_df = attempts_df
        st.subheader("📈 Global Accuracy Progression Timeline")
    else:
        display_df = attempts_df[attempts_df["Quiz ID"] == filter_option]
        st.subheader(f"📈 Accuracy Progression Timeline for {filter_option}")

    # 3. High-Level Metrics Cards for Selected View
    total_runs = len(display_df)
    avg_accuracy = display_df["Accuracy (%)"].mean()
    
    c1, c2 = st.columns(2)
    c1.metric(f"Total Completed Runs ({filter_option})", f"{total_runs}")
    c2.metric(f"Average Accuracy ({filter_option})", f"{round(avg_accuracy, 1)}%")
    
    st.markdown("---")
    
    # 4. Timeline Progress Visualization for Selected Quiz
    chart_data = display_df.copy()
    chart_data["Attempt Number"] = range(1, len(chart_data) + 1)
    chart_data = chart_data.set_index("Attempt Number")
    
    st.line_chart(data=chart_data["Accuracy (%)"], use_container_width=True)
    
    st.markdown("---")
    
    # 5. Timestamped Historic Log Table for Selected Quiz
    st.subheader(f"🗃️ Timestamped Registry: {filter_option}")
    st.markdown("Attempts are shown in chronological order (newest at the top):")
    
    # Display table in descending order so newest runs sit right at the top
    st.dataframe(display_df.iloc[::-1], hide_index=True, use_container_width=True)