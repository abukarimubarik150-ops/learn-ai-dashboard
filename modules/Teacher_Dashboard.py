import streamlit as st
import os
import json
import google.generativeai as genai
import streamlit.components.v1 as components
# We import GoogleAPICallError instead of APIError here:
from google.api_core.exceptions import InvalidArgument, GoogleAPICallError, GoogleAPIError
from fpdf import FPDF
from database import (
    get_connection,
    add_lesson_attachment,
    update_lesson_in_db,
    delete_lesson_from_db
)

# --- CONFIGURATION & KEY RETRIEVAL ---
api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", "YOUR_ACTUAL_API_KEY_HERE"))

# Initialize the library
if api_key and api_key != "YOUR_ACTUAL_API_KEY_HERE":
    genai.configure(api_key=api_key)

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


# --- HELPER FUNCTIONS ---
def read_aloud_widget(text, key_prefix=""):
    """
    Renders a clean HTML/JS controller inside Streamlit that uses the
    user's browser SpeechSynthesis API to read text aloud.
    """
    safe_text = json.dumps(text)

    html_code = f"""
    <div style="display: flex; gap: 10px; align-items: center; padding: 5px 0; font-family: sans-serif;">
        <button id="speak-btn-{key_prefix}" style="background-color: #1E88E5; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; font-weight: bold; display: flex; align-items: center; gap: 5px;">
            🔊 Play
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


def create_pdf(text, title):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    safe_text = text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, txt=safe_text)
    return pdf.output(dest='S').encode('latin-1')


def add_lesson_to_db_local(title, description, difficulty, duration):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO lessons (title, description, difficulty, duration) VALUES (?, ?, ?, ?)",
                       (title, description, difficulty, duration))
        conn.commit()
        l_id = cursor.lastrowid
        conn.close()
        return l_id, "Success"
    except Exception as e:
        return None, str(e)


def fetch_all_lessons():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM lessons ORDER BY id")
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception:
        return []


def get_gemini_model():
    """Safely verifies key and gets model"""
    if not api_key or api_key == "YOUR_ACTUAL_API_KEY_HERE":
        return None, "API Key is missing. Check secrets.toml or env variables."

    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        if not models:
            return None, "No active models support generating content."
        selected_model_name = next((m for m in models if "gemini-1.5-flash" in m), models[0])
        return genai.GenerativeModel(selected_model_name), None

    except InvalidArgument:
        return None, "Google API Key is invalid. Check configuration."
    except GoogleAPICallError as e:
        return None, f"Google API Error: {e.message}"
    except GoogleAPIError as e:
        return None, f"Google Core Error: {str(e)}"
    except Exception as e:
        return None, f"Error: {str(e)}"


# --- MAIN DASHBOARD ---
def show_teacher_dashboard_page():
    st.title("👨‍🏫 Teacher Dashboard")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "➕ Add Lesson", "⚙️ Manage", "📊 Progress", "🤖 AI Planner", "📝 AI Quiz"
    ])

    with tab1:
        st.subheader("📝 Create a New Curriculum Lesson")
        with st.form("add_lesson_form", clear_on_submit=True):
            col_a, col_b = st.columns(2)
            lesson_title = col_a.text_input("Lesson Title")
            lesson_difficulty = col_b.selectbox("Difficulty", ["Beginner", "Intermediate", "Advanced"])
            lesson_description = st.text_area("Description")
            prerequisites = st.text_area("Prerequisites")
            assessment = st.text_area("Assessment Questions")
            uploaded_file = st.file_uploader("Upload Document", type=["pdf", "png", "jpg"])
            video_link = st.text_input("Video URL")
            submit = st.form_submit_button("🚀 Publish Lesson")

        if submit:
            l_id, msg = add_lesson_to_db_local(lesson_title, f"{lesson_description}\n\nPrereqs: {prerequisites}",
                                               lesson_difficulty, "30 mins")
            if l_id:
                st.success("Lesson Published!")
                st.balloons()

    with tab2:
        st.subheader("🛠️ Manage Lessons")
        db_lessons = fetch_all_lessons()
        if db_lessons:
            options = {f"{r[1]} (ID: {r[0]})": r for r in db_lessons}
            sel = st.selectbox("Select Lesson", list(options.keys()))
            row = options[sel]
            if st.button("🗑️ Delete Selected"):
                delete_lesson_from_db(row[0])
                st.rerun()

    with tab4:
        st.subheader("🤖 AI Curriculum Assistant")
        model, error_msg = get_gemini_model()

        if error_msg:
            st.error(f"🔌 AI Feature Disabled: {error_msg}")
        else:
            with st.form("ai_planner_form"):
                topic = st.text_input("Topic")
                gen_btn = st.form_submit_button("✨ Generate Plan")

            if gen_btn and topic:
                with st.status("Gemini is drafting your lesson...", expanded=True) as status:
                    try:
                        response = model.generate_content(f"Create a syllabus-aligned lesson plan for {topic}")
                        st.session_state.ai_plan = response.text
                        status.update(label="✅ Complete!", state="complete")
                    except Exception as e:
                        status.update(label="❌ Failed!", state="error")
                        st.error(f"Generation failed: {str(e)}")

            if "ai_plan" in st.session_state:
                st.write("---")
                st.subheader("🎧 Listen to Lesson Plan")
                read_aloud_widget(st.session_state.ai_plan, key_prefix="planner")
                st.write("---")

                st.markdown(st.session_state.ai_plan)
                pdf = create_pdf(st.session_state.ai_plan, "Lesson")
                st.download_button("📥 Download PDF", data=pdf, file_name="lesson.pdf", mime="application/pdf")

    with tab5:
        st.subheader("📝 AI Quiz Center")
        model, error_msg = get_gemini_model()

        if error_msg:
            st.error(f"🔌 AI Feature Disabled: {error_msg}")
        else:
            with st.form("quiz_gen_form"):
                topic = st.text_input("Quiz Topic")
                num = st.slider("Questions", 3, 10, 5)
                quiz_btn = st.form_submit_button("✨ Generate Quiz")

            if quiz_btn and topic:
                with st.status("Generating quiz...", expanded=True) as status:
                    try:
                        res = model.generate_content(f"Create {num} MCQs for {topic} in JSON format.")
                        st.session_state.quiz_data = res.text
                        status.update(label="Quiz ready!", state="complete")
                    except Exception as e:
                        status.update(label="❌ Failed!", state="error")
                        st.error(f"Quiz generation failed: {str(e)}")

            if "quiz_data" in st.session_state:
                st.write("---")
                st.subheader("🎧 Listen to Quiz Content")
                read_aloud_widget(st.session_state.quiz_data, key_prefix="quiz")
                st.write("---")

                st.code(st.session_state.quiz_data, language="json")
                pdf = create_pdf(st.session_state.quiz_data, "Quiz")
                st.download_button("📥 Download Quiz PDF", data=pdf, file_name="quiz.pdf", mime="application/pdf")