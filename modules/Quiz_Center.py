"""
==========================================================
LEARN-AI MOBILE
Quiz Centre Module (Redesigned)
==========================================================
"""

import streamlit as st
import time
import random
from database import get_all_lessons  # Assuming this helper exists to pull topics

# ---------------------------------------------------------
# MOCK QUIZ DATA GENERATOR (If DB questions aren't ready)
# ---------------------------------------------------------
# In a production environment, you would query these from your database
MOCK_QUESTIONS = {
    "Introduction to AI": [
        {
            "question": "What is the primary goal of Artificial Intelligence?",
            "options": [
                "To make computers run faster",
                "To simulate human intelligence in machines",
                "To replace all human workers immediately",
                "To build physical robots only"
            ],
            "correct": "To simulate human intelligence in machines",
            "explanation": "AI aims to mimic cognitive human functions like learning, reasoning, and problem-solving."
        },
        {
            "question": "Which of the following is an example of Narrow (Weak) AI?",
            "options": [
                "A sci-fi robot with feelings",
                "Siri / Google Assistant",
                "A system that can do any intellectual human task",
                "Skynet"
            ],
            "correct": "Siri / Google Assistant",
            "explanation": "Narrow AI is programmed to perform a single, dedicated task exceptionally well."
        }
    ],
    "Computer Networks": [
        {
            "question": "What does IP stand for in network terminology?",
            "options": [
                "Intranet Protocol",
                "Instant Port",
                "Internet Protocol",
                "Internal Process"
            ],
            "correct": "Internet Protocol",
            "explanation": "An IP address is a unique numerical label assigned to each device connected to a computer network."
        },
        {
            "question": "Which device connects different networks together?",
            "options": [
                "Switch",
                "Hub",
                "Repeater",
                "Router"
            ],
            "correct": "Router",
            "explanation": "Routers forward data packets between computer networks, directing traffic efficiently on the internet."
        }
    ],
    "Cybersecurity Basics": [
        {
            "question": "What is 'Phishing'?",
            "options": [
                "Updating your operating system",
                "A technique to bypass hardware firewalls",
                "Social engineering where attackers trick you into sharing sensitive data",
                "Using a secure virtual private network (VPN)"
            ],
            "correct": "Social engineering where attackers trick you into sharing sensitive data",
            "explanation": "Phishing involves sending fraudulent emails or messages designed to steal credentials or financial information."
        }
    ]
}


def init_quiz_state():
    """Initializes quiz-specific states cleanly."""
    if "quiz_active" not in st.session_state:
        st.session_state.quiz_active = False
    if "current_questions" not in st.session_state:
        st.session_state.current_questions = []
    if "q_index" not in st.session_state:
        st.session_state.q_index = 0
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = {}
    if "quiz_completed" not in st.session_state:
        st.session_state.quiz_completed = False
    if "start_time" not in st.session_state:
        st.session_state.start_time = None


def show_quiz_center_page():
    init_quiz_state()

    st.title("📝 Modern Quiz Centre")
    st.markdown("Test your knowledge, earn **XP**, and level up your ICT skills!")
    st.divider()

    # ---------------------------------------------------------
    # SCREEN 1: CONFIGURATION & SETUP
    # ---------------------------------------------------------
    if not st.session_state.quiz_active and not st.session_state.quiz_completed:

        # Pull topics dynamically (combining our mock data & database concepts)
        try:
            db_lessons = get_all_lessons()
            db_topics = [lesson[1] for lesson in db_lessons]  # Assuming index 1 is Title
        except Exception:
            db_topics = []

        available_topics = list(set(list(MOCK_QUESTIONS.keys()) + db_topics))

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("### 🛠️ Configure Your Quiz")

            # 1. Topic Selection (Dynamic & Divergent)
            selected_topics = st.multiselect(
                "Choose your Topics (Select one, multiple, or leave empty for mixed bag)",
                options=available_topics,
                placeholder="🔍 Select ICT Topics..."
            )

            # 2. Quiz Mode Selector
            quiz_mode = st.radio(
                "Select Quiz Mode",
                options=["⚡ Rapid Fire (Quick, No Timer)", "⏱️ Exam Mode (Timed challenge!)",
                         "📖 Self-Paced (See explanations as you go)"],
                index=0,
                help="Exam mode limits time. Self-Paced explains correct answers immediately."
            )

            # 3. Size Selector
            quiz_size = st.slider("Number of Questions", min_value=2, max_value=10, value=5)

        with col2:
            st.markdown("### 🏆 Your Stats")
            # Minimalistic Metric Card UI
            st.markdown(
                f"""
                <div style="background-color:#ffffff; padding:20px; border-radius:12px; border:1px solid #E5E7EB; box-shadow: 0px 4px 10px rgba(0,0,0,0.05)">
                    <h5 style="color:#1F2937; margin:0 0 10px 0;">Student Profile</h5>
                    <p style="margin:5px 0;"><strong>Current XP:</strong> ⭐ {st.session_state.xp}</p>
                    <p style="margin:5px 0;"><strong>Active Streak:</strong> 🔥 {st.session_state.streak} Days</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.write("")

            # Quick Actions to leave
            if st.button("🎓 Return to Student Portal", use_container_width=True):
                st.session_state.redirect_to = "🎓 Student Portal"
                st.rerun()

        st.divider()

        if st.button("🚀 Start Quiz", type="primary", use_container_width=True):
            # Compile questions based on user selection
            pool = []
            topics_to_pull = selected_topics if selected_topics else available_topics

            for topic in topics_to_pull:
                if topic in MOCK_QUESTIONS:
                    pool.extend(MOCK_QUESTIONS[topic])

            # Fallback if no questions are found for selected DB topics
            if not pool:
                # Merge all mock questions as fallback
                for q_list in MOCK_QUESTIONS.values():
                    pool.extend(q_list)

            # Sample the questions
            random.shuffle(pool)
            st.session_state.current_questions = pool[:quiz_size]
            st.session_state.quiz_mode = quiz_mode
            st.session_state.q_index = 0
            st.session_state.score = 0
            st.session_state.user_answers = {}
            st.session_state.quiz_active = True
            st.session_state.start_time = time.time()
            st.rerun()

    # ---------------------------------------------------------
    # SCREEN 2: ACTIVE QUIZ RUNNER
    # ---------------------------------------------------------
    elif st.session_state.quiz_active and not st.session_state.quiz_completed:
        questions = st.session_state.current_questions
        idx = st.session_state.q_index
        total_q = len(questions)

        if idx < total_q:
            current_q = questions[idx]

            # Header info
            st.subheader(f"Question {idx + 1} of {total_q}")

            # Progress Bar
            progress_pct = int(((idx) / total_q) * 100)
            st.progress(idx / total_q, text=f"{progress_pct}% Completed")

            # Simple timer feedback for Exam Mode
            if "Exam Mode" in st.session_state.quiz_mode:
                elapsed = int(time.time() - st.session_state.start_time)
                limit = total_q * 30  # 30 seconds per question
                remaining = limit - elapsed
                if remaining <= 0:
                    st.error("⏳ Time is up!")
                    st.session_state.quiz_completed = True
                    st.session_state.quiz_active = False
                    st.rerun()
                else:
                    st.warning(f"⏱️ Time Remaining: {remaining // 60}m {remaining % 60}s (Limit: {limit // 60}m)")

            # Question display card
            st.markdown(
                f"""
                <div style="background-color:#F9FAFB; padding:25px; border-radius:12px; border-left:6px solid #4F46E5; margin-bottom:20px;">
                    <h4 style="color:#111827; margin:0;">{current_q['question']}</h4>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Interactive radio selection (unique key per index is crucial)
            user_choice = st.radio(
                "Choose your answer:",
                options=current_q["options"],
                key=f"q_radio_{idx}",
                index=None  # Starts unselected for zero-bias testing
            )

            col_prev, col_next = st.columns([1, 1])

            # Immediate explanation for Self-Paced mode
            if "Self-Paced" in st.session_state.quiz_mode and user_choice is not None:
                if user_choice == current_q["correct"]:
                    st.success("🎯 Correct!")
                else:
                    st.error(f"❌ Incorrect. The correct answer was: **{current_q['correct']}**")
                st.info(f"💡 **Explanation:** {current_q['explanation']}")

            with col_next:
                if user_choice is not None:
                    btn_label = "Finish Quiz 🏁" if idx == total_q - 1 else "Next Question ➡️"
                    if st.button(btn_label, type="primary", use_container_width=True):
                        # Save Answer & Calculate Score
                        st.session_state.user_answers[idx] = user_choice
                        if user_choice == current_q["correct"]:
                            st.session_state.score += 1

                        # Advance index or complete
                        if idx + 1 < total_q:
                            st.session_state.q_index += 1
                        else:
                            st.session_state.quiz_completed = True
                            st.session_state.quiz_active = False
                        st.rerun()
                else:
                    st.button("Please select an answer", disabled=True, use_container_width=True)

            with col_prev:
                if st.button("🚨 Forfeit Quiz", use_container_width=True):
                    # Reset state back to setup screen
                    st.session_state.quiz_active = False
                    st.session_state.quiz_completed = False
                    st.rerun()

    # ---------------------------------------------------------
    # SCREEN 3: QUIZ COMPLETE & PERFORMANCE HUB
    # ---------------------------------------------------------
    elif st.session_state.quiz_completed:
        questions = st.session_state.current_questions
        total_q = len(questions)
        score = st.session_state.score
        percentage = int((score / total_q) * 100) if total_q > 0 else 0

        # Calculate XP payout (e.g., 20 XP per correct answer + 50 XP bonus for perfect score)
        xp_earned = score * 20
        perfect_bonus = 50 if percentage == 100 else 0
        total_xp_payout = xp_earned + perfect_bonus

        st.balloons()
        st.success("🎉 Congratulations! You have completed the quiz.")

        # Result Banner Card
        st.markdown(
            f"""
            <div style="background-color:#EEF2F6; padding:30px; border-radius:15px; text-align:center; margin-bottom:25px;">
                <h2 style="margin:0; color:#1E3A8A;">Your Score: {score} / {total_q}</h2>
                <h1 style="margin:10px 0; font-size:48px; color:#4F46E5;">{percentage}%</h1>
                <p style="font-size:18px; color:#4B5563;">You earned <strong>⭐ +{total_xp_payout} XP</strong> to your profile!</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Update actual Session XP safely inside the system
        if "xp_credited" not in st.session_state or not st.session_state.xp_credited:
            st.session_state.xp += total_xp_payout
            st.session_state.xp_credited = True

        # Show detailed breakdown
        with st.expander("🔍 Review Answers & Explanations", expanded=True):
            for i, q in enumerate(questions):
                user_ans = st.session_state.user_answers.get(i, "No Answer Given")
                is_correct = user_ans == q["correct"]

                status_color = "#10B981" if is_correct else "#EF4444"
                status_symbol = "✅" if is_correct else "❌"

                st.markdown(
                    f"""
                    <div style="border-left: 4px solid {status_color}; padding-left: 15px; margin-bottom: 20px;">
                        <h5 style="margin:0 0 5px 0;">Q{i + 1}: {q['question']}</h5>
                        <p style="margin:2px 0;">Your Answer: <span style="color:{status_color}; font-weight:bold;">{user_ans} {status_symbol}</span></p>
                        <p style="margin:2px 0; color:#4B5563;">Correct Answer: <strong>{q['correct']}</strong></p>
                        <p style="margin:5px 0 0 0; font-size:14px; font-style:italic; color:#6B7280;">💡 Explanation: {q['explanation']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        col_left, col_right = st.columns(2)
        with col_left:
            if st.button("🔄 Try Another Quiz", type="primary", use_container_width=True):
                # Clean quiz states and rerun to step 1
                st.session_state.quiz_active = False
                st.session_state.quiz_completed = False
                st.session_state.xp_credited = False
                st.rerun()

        with col_right:
            if st.button("🎓 Return to Student Portal", use_container_width=True):
                # Safely redirect back using our app.py handler
                st.session_state.quiz_active = False
                st.session_state.quiz_completed = False
                st.session_state.xp_credited = False
                st.session_state.redirect_to = "🎓 Student Portal"
                st.rerun()