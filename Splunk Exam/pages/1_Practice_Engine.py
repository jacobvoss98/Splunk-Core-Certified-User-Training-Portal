import streamlit as st
import json
from datetime import datetime

st.set_page_config(page_title="Practice Engine", page_icon="📊")

@st.cache_data
def load_questions():
    try:
        with open("questions.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

all_questions = load_questions()

# Core tracking structures
if "history" not in st.session_state: 
    st.session_state.history = []
if "quiz_attempts" not in st.session_state:
    st.session_state.quiz_attempts = [] # Persistent run tracking

st.title("Exam Practice Engine 📝")

quiz_list = sorted(list(set([q["quiz_id"] for q in all_questions])))
selected_quiz = st.selectbox("Select a Quiz to Start:", quiz_list, format_func=lambda x: f"Quiz {x} ({'20 Qs' if x < 11 else '12 Qs'})")

quiz_questions = [q for q in all_questions if q["quiz_id"] == selected_quiz]

state_idx_key = f"idx_quiz_{selected_quiz}"
state_submitted_key = f"sub_quiz_{selected_quiz}"
state_ans_key = f"ans_quiz_{selected_quiz}"
state_quiz_saved_key = f"saved_quiz_{selected_quiz}" # Track if the final run was logged

if state_idx_key not in st.session_state: st.session_state[state_idx_key] = 0
if state_submitted_key not in st.session_state: st.session_state[state_submitted_key] = False
if state_ans_key not in st.session_state: st.session_state[state_ans_key] = None
if state_quiz_saved_key not in st.session_state: st.session_state[state_quiz_saved_key] = False

current_idx = st.session_state[state_idx_key]

# Quiz Complete State
if current_idx >= len(quiz_questions):
    st.success(f"🎉 Quiz {selected_quiz} Complete!")
    
    # Calculate performance metrics for this specific window
    quiz_logs = [h for h in st.session_state.history if h["quiz_id"] == selected_quiz]
    correct_run_count = sum(1 for h in quiz_logs if h["status"] == "Correct")
    total_run_count = len(quiz_questions)
    # Calculate performance metrics for this specific window
quiz_logs = [h for h in st.session_state.history if h["quiz_id"] == selected_quiz]
correct_run_count = sum(1 for h in quiz_logs if h["status"] == "Correct")

total_run_count = len(quiz_questions)

# 💡 FIX: Prevent division by zero if the quiz questions list didn't load properly
if total_run_count > 0:
    score_percentage = round((correct_run_count / total_run_count) * 100, 1)
else:
    score_percentage = 0.0
    
    # Log the complete attempt snapshot exactly ONCE per run
    if not st.session_state[state_quiz_saved_key]:
        st.session_state.quiz_attempts.append({
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Quiz ID": f"Quiz {selected_quiz}",
            "Score": f"{correct_run_count} / {total_run_count}",
            "Accuracy (%)": score_percentage
        })
        st.session_state[state_quiz_saved_key] = True

    st.metric("Your Score", f"{correct_run_count} / {total_run_count}", f"{score_percentage}% Accuracy")

    if st.button("Retake this Quiz"):
        st.session_state[state_idx_key] = 0
        st.session_state[state_submitted_key] = False
        st.session_state[state_ans_key] = None
        st.session_state[state_quiz_saved_key] = False
        # Remove individual raw question steps for this quiz so you can fresh-start tracking
        st.session_state.history = [h for h in st.session_state.history if h["quiz_id"] != selected_quiz]
        st.rerun()
else:
    current_q = quiz_questions[current_idx]
    st.markdown(f"**Question {current_idx + 1} of {len(quiz_questions)}**")
    st.progress(current_idx / len(quiz_questions))
    
    st.info(f"### {current_q['question']}")
    selected_option = st.radio("Choose answer:", current_q["options"], key=f"r_{selected_quiz}_{current_idx}", disabled=st.session_state[state_submitted_key])
    
    if not st.session_state[state_submitted_key]:
        if st.button("Submit Answer", type="primary"):
            st.session_state[state_submitted_key] = True
            st.session_state[state_ans_key] = selected_option
            chosen_letter = selected_option.split(".")[0].strip()
            is_correct = chosen_letter in current_q["correct"]
            
            if is_correct:
                st.toast("Correct! 🎯")
            else:
                st.toast("Incorrect ❌")
            
            st.session_state.history.append({
                "question_id": current_q["id"],
                "quiz_id": selected_quiz,
                "status": "Correct" if is_correct else "Incorrect"
            })
            st.rerun()
    else:
        correct_letter = current_q["correct"]
        if st.session_state[state_ans_key].split(".")[0].strip() in correct_letter:
            st.success(f"🎯 **Correct!** Answer is **{correct_letter}**.")
        else:
            st.error(f"❌ **Incorrect.** Correct answer is **{correct_letter}**.")
            
        if st.button("Next Question ➡️"):
            st.session_state[state_idx_key] += 1
            st.session_state[state_submitted_key] = False
            st.session_state[state_ans_key] = None
            st.rerun()