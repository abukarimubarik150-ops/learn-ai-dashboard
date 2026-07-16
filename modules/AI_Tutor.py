import streamlit as st
import google.generativeai as genai
from config import GEMINI_API_KEY


def show_ai_tutor_page():
    # -----------------------------
    # CONFIGURE GEMINI CLIENT
    # -----------------------------
    if not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
        st.warning(
            "⚠️ Gemini API key is missing or not configured. Please add your key to config.py to activate live AI responses.")
        return

    genai.configure(api_key=GEMINI_API_KEY)

    # -----------------------------
    # SESSION STATE INITIALIZATION
    # -----------------------------
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant",
             "content": "Hello there! 👋 I am your LEARN-AI Tutor, calibrated for the Ghana ICT Curriculum. Ask me anything about computing!"}
        ]

    st.title("🤖 AI Study Tutor")
    st.caption("Your 24/7 personalized instructional assistant.")
    st.divider()

    # -----------------------------
    # SYSTEM PROMPT (CURRICULUM INSTRUCTIONS)
    # -----------------------------
    system_instruction = (
        "You are an AI-powered inclusive ICT learning assistant named LEARN-AI Tutor. "
        "Your target users are junior high school (JHS) and senior high school (SHS) students in Ghana. "
        "Explain computing concepts clearly using relatable analogies, real-world examples relevant to West Africa, "
        "and follow the Ghana Education Service (GES) computing curriculum standards. Keep answers concise, highly accessible, "
        "and encouraging."
    )

    # -----------------------------
    # QUICK SUGGESTIONS PROMPTS
    # -----------------------------
    st.subheader("💡 Quick Questions")
    c1, c2, c3 = st.columns(3)

    def trigger_quick_prompt(prompt_text):
        st.session_state.chat_history.append({"role": "user", "content": prompt_text})
        try:
            # UPDATED CONFIGURATION ENDPOINT
            model = genai.GenerativeModel(
                model_name="gemini-2.5-flash",
                system_instruction=system_instruction
            )
            with st.spinner("Tutor is typing..."):
                response = model.generate_content(prompt_text)
                st.session_state.chat_history.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"API Error: {e}")
        st.rerun()

    with c1:
        if st.button("🌐 Explain the Internet", use_container_width=True):
            trigger_quick_prompt(
                "Can you explain how the internet works for a JHS computing student using a simple analogy?")

    with c2:
        if st.button("💾 What is a Database?", use_container_width=True):
            trigger_quick_prompt(
                "What is a relational database management system? Explain tables, rows, and columns clearly.")

    with c3:
        if st.button("📝 Quiz Me on Hardware", use_container_width=True):
            trigger_quick_prompt(
                "Give me a quick 1-question multiple choice quiz on input and output devices. Don't reveal the answer immediately.")

    st.divider()

    # -----------------------------
    # RENDER CHAT INTERFACE
    # -----------------------------
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # -----------------------------
    # LIVE CHAT SELECTION RUNNER
    # -----------------------------
    if user_query := st.chat_input("Type your ICT question here...", key="ai_chat_input_unique"):
        with st.chat_message("user"):
            st.write(user_query)
        st.session_state.chat_history.append({"role": "user", "content": user_query})

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    formatted_contents = []
                    for msg in st.session_state.chat_history[:-1]:
                        api_role = "user" if msg["role"] == "user" else "model"
                        formatted_contents.append({"role": api_role, "parts": [msg["content"]]})

                    formatted_contents.append({"role": "user", "parts": [user_query]})

                    # UPDATED CONFIGURATION ENDPOINT
                    model = genai.GenerativeModel(
                        model_name="gemini-2.5-flash",
                        system_instruction=system_instruction
                    )

                    response = model.generate_content(formatted_contents)

                    st.write(response.text)
                    st.session_state.chat_history.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"Failed to communicate with Gemini API: {e}")