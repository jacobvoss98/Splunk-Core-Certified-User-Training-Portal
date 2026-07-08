import streamlit as st
import json

st.set_page_config(page_title="Practice Engine", page_icon="📊")

@st.cache_data
def load_questions():
    try:
        with open("questions.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

all_questions = load_questions()

if "history" not in st.session_state: 
    st.session_state.history = []

st.title("Exam Practice Engine 📝")

# 1. Quiz Selection Dropdown
quiz_list = sorted(list(set([q["quiz_id"] for q in all_questions])))
selected_quiz = st.selectbox("Select a Quiz to Start:", quiz_list, format_func=lambda x: f"Quiz {x} ({'20 Qs' if x < 11 else '12 Qs'})")

# Filter down to just the selected quiz's questions
quiz_questions = [q for q in all_questions if q["quiz_id"] == selected_quiz]

# Track individual quiz state separately using a key string unique to the quiz ID
state_idx_key = f"idx_quiz_{selected_quiz}"
state_submitted_key = f"sub_quiz_{selected_quiz}"
state_ans_key = f"ans_quiz_{selected_quiz}"

if state_idx_key not in st.session_state: st.session_state[state_idx_key] = 0
if state_submitted_key not in st.session_state: st.session_state[state_submitted_key] = False
if state_ans_key not in st.session_state: st.session_state[state_ans_key] = None

current_idx = st.session_state[state_idx_key]

if current_idx >= len(quiz_questions):
    st.success(f"🎉 Quiz {selected_quiz} Complete!")
    if st.button("Reset this Quiz"):
        st.session_state[state_idx_key] = 0
        st.session_state[state_submitted_key] = False
        st.session_state[state_ans_key] = None
        # Clean history for just this specific quiz
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
            
            # Save data step WITH quiz_id for analytics mapping
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