import streamlit as st
import pandas as pd


def show_analytics_page():
    st.title("📈 Performance Analytics")
    st.caption("Track your learning speed, quiz outcomes, and curriculum coverage milestone metrics.")
    st.divider()

    # -----------------------------
    # GATHER CURRENT APPLICATION METRICS
    # -----------------------------
    completed_count = len(st.session_state.get("completed_lessons", []))
    total_lessons = 8  # Base syllabus metric matching your dashboard
    completion_percentage = int((completed_count / total_lessons) * 100) if completed_count > 0 else 0

    current_xp = st.session_state.get("xp", 0)
    current_streak = st.session_state.get("streak", 0)

    # -----------------------------
    # HIGHLIGHT CARDS
    # -----------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Curriculum Progress", f"{completion_percentage}%", f"{completed_count}/{total_lessons} Lessons")
    with col2:
        st.metric("Total Experience Points", f"{current_xp} XP")
    with col3:
        st.metric("Active Learning Streak", f"{current_streak} Days")

    st.divider()

    # -----------------------------
    # VISUAL CHARTS (MOCK PROGRESS DATA BASED ON CURRENT STATE)
    # -----------------------------
    left_col, right_col = st.columns(2)

    with left_col:
        st.subheader("📚 Syllabus Progress Breakdown")
        # Build progress data frame dynamically
        progress_data = pd.DataFrame({
            "Status": ["Completed", "Remaining"],
            "Count": [completed_count, max(0, total_lessons - completed_count)]
        })
        # Set index for clean charting labels
        progress_data = progress_data.set_index("Status")
        st.bar_chart(progress_data, color="#3B82F6")

    with right_col:
        st.subheader("🎯 Weekly Study Consistency")
        # Activity logs tracking XP accumulation
        weekly_xp = pd.DataFrame({
            "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            "XP Earned": [10 if current_xp > 0 else 0, 0, 20 if current_xp > 20 else 0, 0, current_xp, 0, 0]
        })
        weekly_xp = weekly_xp.set_index("Day")
        st.line_chart(weekly_xp, color="#10B981")

    st.divider()

    # -----------------------------
    # SYLLABUS CHECKLIST SUMMARY
    # -----------------------------
    st.subheader("📋 Completed Core Subjects Summary")
    if completed_count == 0:
        st.info(
            "No lessons have been marked completed yet! Head over to the '📚 ICT Lessons' page to begin tracking your syllabus.")
    else:
        st.write("You have successfully studied the following notes modules during this session:")
        for lesson_title in st.session_state.completed_lessons:
            st.checkbox(f"✨ {lesson_title}", value=True, disabled=True, key=f"analytic_chk_{hash(lesson_title)}")