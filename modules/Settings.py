import streamlit as st
import os
import sqlite3
from PIL import Image
from database import get_connection

# Setup profile picture directory structure
PROFILE_PIC_DIR = os.path.join("uploads", "profile_pics")
if not os.path.exists(PROFILE_PIC_DIR):
    os.makedirs(PROFILE_PIC_DIR)


def get_profile_picture_path(username):
    """Checks if a custom profile picture exists for the user."""
    for ext in ["png", "jpg", "jpeg"]:
        path = os.path.join(PROFILE_PIC_DIR, f"{username}.{ext}")
        if os.path.exists(path):
            return path
    return None


def show_settings_page():
    st.title("⚙️ Account & App Settings")
    st.caption("Manage your profile settings, accessibility layout preferences, and system parameters.")
    st.divider()

    # Safety check: Ensure user is logged in
    if "username" not in st.session_state:
        st.error("Please log in to access settings.")
        return

    # Ensure dynamic styling states are initialized safely
    if "app_theme" not in st.session_state:
        st.session_state.app_theme = "Light"
    if "accessible_font" not in st.session_state:
        st.session_state.accessible_font = False

    username = st.session_state.username

    # -----------------------------
    # TAB INTERFACE
    # -----------------------------
    tab1, tab2, tab3 = st.tabs(["👤 Profile Management", "🎨 Accessibility & Theme", "ℹ️ System Info"])

    # TAB 1: PROFILE MANAGEMENT
    with tab1:
        st.subheader("Edit Profile Details")

        col_pic, col_fields = st.columns([1, 2])

        with col_pic:
            st.markdown("##### Profile Picture")

            # 1. Fetch and Display Current Profile Picture
            current_pic_path = get_profile_picture_path(username)
            if current_pic_path:
                st.image(current_pic_path, caption="Current Photo", width=150)

                # Button to remove profile picture
                if st.button("🗑️ Remove Photo", use_container_width=True):
                    try:
                        os.remove(current_pic_path)
                        st.success("Photo removed!")
                        st.rerun()
                    except Exception:
                        st.error("Could not remove photo file.")
            else:
                # Default avatar fallback
                st.image("https://cdn-icons-png.flaticon.com/512/149/149071.png", caption="Default Avatar", width=150)

            st.write("---")

            # 2. File Upload for New Avatar
            uploaded_pic = st.file_uploader("Upload new photo", type=["png", "jpg", "jpeg"], key="profile_pic_uploader")
            if uploaded_pic is not None:
                if st.button("💾 Save Photo", type="primary", use_container_width=True):
                    # Clean up any existing image files with different extensions first
                    existing_path = get_profile_picture_path(username)
                    if existing_path and os.path.exists(existing_path):
                        os.remove(existing_path)

                    # Save the new photo as '{username}.extension'
                    file_extension = uploaded_pic.name.split(".")[-1].lower()
                    save_path = os.path.join(PROFILE_PIC_DIR, f"{username}.{file_extension}")

                    try:
                        # Open and optimize size to keep app running fast
                        img = Image.open(uploaded_pic)
                        img.thumbnail((300, 300))
                        img.save(save_path)

                        st.success("🎉 Profile picture updated!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error saving image: {e}")

        with col_fields:
            st.markdown("##### Account Information")
            # Prefill fields using existing session state values
            updated_name = st.text_input("Full Name", value=st.session_state.get("fullname", ""))
            current_username = st.text_input("Username (Read-Only)", value=username, disabled=True)
            current_role = st.text_input("Account Type / Role", value=st.session_state.get("role", ""), disabled=True)

            if st.button("💾 Update Profile Name", use_container_width=True):
                if updated_name.strip() == "":
                    st.error("Name field cannot be empty.")
                else:
                    try:
                        # Update sqlite database for persistence
                        conn = get_connection()
                        cursor = conn.cursor()
                        cursor.execute("""
                            UPDATE users 
                            SET fullname = ? 
                            WHERE username = ?
                        """, (updated_name, username))
                        conn.commit()
                        conn.close()

                        # Update active memory session state
                        st.session_state.fullname = updated_name
                        st.success("Profile name updated successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Database error during name update: {e}")

    # TAB 2: ACCESSIBILITY & PREFERENCES (INTEGRATED WITH DYNAMIC APPY STYLING)
    with tab2:
        st.subheader("Display Customization")
        st.write("Adjust the UI layout variables to optimize readability and accessibility across devices.")

        # Match dropdown index to active session state
        theme_index = 0
        if st.session_state.app_theme == "Slate":
            theme_index = 1
        elif st.session_state.app_theme == "Dark":
            theme_index = 2

        theme_choice = st.selectbox(
            "Interface Theme Color",
            options=["Light White", "Slate Gray", "Dark Midnight Blue"],
            index=theme_index
        )

        font_choice = st.toggle(
            "Enable High-Contrast / Large Font Mode",
            value=st.session_state.accessible_font,
            help="Increases application text size dynamically to aid readability."
        )

        enable_tts = st.toggle("Enable automatic Text-to-Speech narration for ICT Lesson modules", value=False)

        st.write("")
        if st.button("🔄 Apply Interface Adjustments", type="primary", use_container_width=True):
            # Translate text selection to main state themes used by our dynamic CSS injector
            theme_mapping = {
                "Light White": "Light",
                "Slate Gray": "Slate",
                "Dark Midnight Blue": "Dark"
            }
            st.session_state.app_theme = theme_mapping[theme_choice]
            st.session_state.accessible_font = font_choice

            st.toast("Aesthetics applied successfully! 🎉")
            st.rerun()

    # TAB 3: SYSTEM INFO (PERSONALIZED BIO)
    with tab3:
        st.subheader("Application Diagnostics")

        st.markdown(f"""
        * **Platform Name:** LEARN-AI Mobile
        * **Lead Developer:** Abubakar Mubarak
        * **Role:** Software Engineer & Educational Technologist
        * **Designation:** Group 10 Capstone 3 Project
        * **Current Engine Version:** v1.2.0 (Production Core)
        * **Active LLM Brain:** Google Gemini 2.5 Flash
        * **Database Subsystem:** SQLite3 Relational Driver
        * **Core Frame Environment:** Streamlit Framework
        """)

        st.divider()
        st.subheader("🏆 Your Session Milestones")
        st.write(f"• **Accumulated XP:** {st.session_state.get('xp', 0)} Points")
        st.write(f"• **Current Study Streak:** {st.session_state.get('streak', 0)} Days consecutive")