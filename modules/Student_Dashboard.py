import streamlit as st
import os
import json
import google.generativeai as genai
import streamlit.components.v1 as components
from google.api_core.exceptions import InvalidArgument, GoogleAPICallError, GoogleAPIError
from database import get_connection

# --- CONFIGURATION & KEY RETRIEVAL ---
api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", "YOUR_ACTUAL_API_KEY_HERE"))

if api_key and api_key != "YOUR_ACTUAL_API_KEY_HERE":
    genai.configure(api_key=api_key)


# --- HELPER FUNCTIONS ---
def read_aloud_widget(text, key_prefix=""):
    """User-friendly client-side browser TTS engine."""
    safe_text = json.dumps(text)
    html_code = f"""
    <div style="display: flex; gap: 10px; align-items: center; padding: 5px 0; font-family: sans-serif;">
        <button id="speak-btn-{key_prefix}" style="background-color: #4CAF50; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; font-weight: bold; display: flex; align-items: center; gap: 5px;">
            🔊 Play Aloud
        </button>
        <button id="pause-btn-{key_prefix}" style="background-color: #FB8C00; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; font-weight: bold; display: flex; align-items: center; gap: 5px;">
            ⏸️ Pause
        </button>
        <button id="stop-btn-{key_prefix}" style="background-color: #E53935; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; font-weight: bold; display: flex; align-items: center; gap: 5px;">
            ⏹️ Stop
        </button>
    </div>
    <script>
        const textToSpeak = {safe_text};
        const speakBtn = document.getElementById('speak-btn-{key_prefix}');
        const pauseBtn = document.getElementById('pause-btn-{key_prefix}');
        const stopBtn = document.getElementById('stop-btn-{key_prefix}');

        const synth = window.speechSynthesis;
        let utterance = null;

        speakBtn.addEventListener('click', () => {{
            if (synth.paused) {{
                synth.resume();
            }} else {{
                synth.cancel();
                utterance = new SpeechSynthesisUtterance(textToSpeak);
                utterance.rate = 1.0;
                utterance.pitch = 1.0;
                synth.speak(utterance);
            }}
        }});
        pauseBtn.addEventListener('click', () => {{
            if (synth.speaking && !synth.paused) {{
                synth.pause();
            }}
        }});
        stopBtn.addEventListener('click', () => {{
            synth.cancel();
        }});
    </script>
    """
    components.html(html_code, height=50)


def fetch_lessons_for_students():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, description, difficulty, duration FROM lessons ORDER BY id DESC")
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception:
        return []


def get_gemini_model():
    if not api_key or api_key == "YOUR_ACTUAL_API_KEY_HERE":
        return None, "API Key missing."
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        selected = next((m for m in models if "gemini-1.5-flash" in m), models[0])
        return genai.GenerativeModel(selected), None
    except Exception as e:
        return None, str(e)


# --- STUDENT DASHBOARD PAGE ---
def show_student_dashboard_page():
    st.title("🎓 Student Learning Portal")
    st.write("Welcome back! Here are your lessons and practice tools.")

    tab1, tab2, tab3 = st.tabs(["📚 My Lessons", "✍️ AI Practice Partner", "🏆 My Progress"])

    with tab1:
        st.subheader("Explore Published Lessons")
        lessons = fetch_lessons_for_students()

        if not lessons:
            st.info("No lessons have been published by your teacher yet. Check back soon!")
        else:
            # Map database records
            options = {f"{r[1]} [{r[3]}]": r for r in lessons}
            selected_key = st.selectbox("Select a lesson to study:", list(options.keys()))

            if selected_key:
                selected_lesson = options[selected_key]
                lesson_id, title, description, difficulty, duration = selected_lesson

                st.write("---")
                st.markdown(f"## {title}")
                st.caption(f"Difficulty: **{difficulty}** | Recommended Time: **{duration}**")

                # Action Button to fully jump over to the active Lessons Module
                if st.button("📖 Launch Full Lesson & Materials", key=f"launch_{lesson_id}", use_container_width=True):
                    # Write target lesson ID to Session State
                    st.session_state.current_lesson_id = lesson_id
                    # Switch the programmatical navigation state to redirect the page
                    st.session_state.redirect_to = "📚 ICT Lessons"
                    st.rerun()

                st.write("---")
                # Audio option for student study comfort
                st.write("🎧 **Listen to lesson notes preview:**")
                read_aloud_widget(description, key_prefix=f"lesson_{lesson_id}")
                st.write("---")

                st.markdown(description)

    with tab2:
        st.subheader("🤖 AI Practice Partner")
        st.write("Need quick study prep? Generate a flash quiz on any topic!")

        model, err = get_gemini_model()
        if err:
            st.warning("AI features are temporarily unavailable. Let your administrator know.")
        else:
            with st.form("student_quiz_form"):
                topic = st.text_input("What topic would you like to practice?", placeholder="e.g., Photosynthesis")
                num_questions = st.slider("Number of Questions", 3, 5, 3)
                start_quiz = st.form_submit_button("Generate Practice Test")

            if start_quiz and topic:
                with st.spinner("Writing questions..."):
                    try:
                        prompt = f"Create a practice quiz of {num_questions} multiple choice questions about {topic} with answers and brief explanations. Present them clearly."
                        res = model.generate_content(prompt)
                        st.session_state.student_practice_content = res.text
                    except Exception as e:
                        st.error(f"Error starting quiz: {str(e)}")

            if "student_practice_content" in st.session_state:
                st.write("---")
                st.write("🎧 **Audio option:**")
                read_aloud_widget(st.session_state.student_practice_content, key_prefix="practice")
                st.write("---")
                st.markdown(st.session_state.student_practice_content)

    with tab3:
        st.subheader("📈 My Progress")
        col1, col2, col3 = st.columns(3)
        col1.metric(label="Lessons Completed", value="0 / 0", delta="Keep studying!")
        col2.metric(label="Average Quiz Score", value="N/A", delta="None taken")
        col3.metric(label="Study Hours", value="0.0 hrs", delta="+0.0 this week")