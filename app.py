"""
==========================================================
LEARN-AI MOBILE
Main Application (With Developer Welcome Gateway)
==========================================================
"""

import streamlit as st
import random
import os

from config import APP_NAME, APP_ICON
from auth import register_user, login_user
from database import initialize_database, seed_lessons

# Import dashboards safely
import modules.Teacher_Dashboard as Teacher_Dashboard
import modules.Student_Dashboard as Student_Dashboard


# ---------------------------------------------------------
# INITIALIZE DATABASE
# ---------------------------------------------------------

initialize_database()
seed_lessons()


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title=APP_NAME,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

st.markdown("""
<style>

.main {
    background: #F5F7FB;
}

section[data-testid="stSidebar"] {
    background: #1F2937;
}

section[data-testid="stSidebar"] * {
    color: white;
}

.stButton>button {
    width: 100%;
    border-radius: 10px;
    height: 45px;
    font-size: 16px;
}

.metric-card {
    background: white;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0px 2px 8px rgba(0,0,0,.08);
}

/* ---------------------------------------------------------
   SIDEBAR LOGOUT BUTTON OVERRIDES (HIGH-CONTRAST)
   --------------------------------------------------------- */
section[data-testid="stSidebar"] div.stButton > button {
    background-color: #D32F2F !important; /* Vivid Crimson Red */
    border: 1px solid #B71C1C !important;
    border-radius: 10px !important;
    transition: background-color 0.2s ease, transform 0.1s ease;
}

/* Explicitly style text & icon within the sidebar button */
section[data-testid="stSidebar"] div.stButton > button p {
    color: #FFFFFF !important;            /* Pure White Text */
    font-weight: bold !important;
}

section[data-testid="stSidebar"] div.stButton > button:hover {
    background-color: #B71C1C !important; /* Darker red on hover */
    border-color: #8B0000 !important;
}

section[data-testid="stSidebar"] div.stButton > button:hover p {
    color: #FFFFFF !important;            /* Ensure text stays white on hover */
}

section[data-testid="stSidebar"] div.stButton > button:active {
    transform: scale(0.98);
}

/* ---------------------------------------------------------
   PORTFOLIO STYLING
   --------------------------------------------------------- */
.portfolio-card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    border: 1px solid #E5E7EB;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# HELPER FUNCTIONS & SESSION STATE
# ---------------------------------------------------------

defaults = {
    "visited_welcome": False,            # Gateway status key
    "logged_in": False,
    "username": "",
    "fullname": "",
    "role": "",
    "xp": 0,
    "streak": 0,
    "navigation_radio": "🏠 Dashboard",  # Track navigation programmatically
    "redirect_to": None                  # Safe transition queue
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def switch_page(page_name):
    """Safely updates the sidebar navigation programmatic state."""
    st.session_state.navigation_radio = page_name


# ---------------------------------------------------------
# CRITICAL REDIRECTION RESOLVER
# ---------------------------------------------------------
if st.session_state.redirect_to is not None:
    target_page = st.session_state.redirect_to
    st.session_state.redirect_to = None  # Clear queue
    st.session_state.navigation_radio = target_page
    st.rerun()


# ---------------------------------------------------------
# SCREEN 0: DEVELOPER PORTFOLIO GATEWAY (WELCOME PAGE)
# ---------------------------------------------------------
if not st.session_state.visited_welcome:

    # 1. Main visual layout of the Landing screen
    st.title("🚀 Welcome to LEARN-AI")
    st.subheader("An Inclusive ICT & Computer Science Interactive Platform")
    st.divider()

    col_bio, col_details = st.columns([3, 2])

    with col_bio:
        st.markdown("### 👨‍💻 Meet the Developer")

        # --- AMENDMENT: PERSONALIZED BIO ---
        st.markdown(
            """
            Hello! I am **Abubakar Mubarak**, a **Software Engineer** and an **Educational Technologist**. 
            My passion lies at the intersection of robust software systems and human learning patterns. I design and engineer 
            interactive ecosystems that leverage artificial intelligence to make technical computer science content 
            accessible, gamified, and highly personalized.
            
            This application, **LEARN-AI**, is designed specifically to align with current ICT structures 
            and help students build, track, and verify practical computing capabilities in an inclusive environment.
            """
        )

        # Callout banner to encourage sign-ins
        st.info("💡 **Inclusive Tech Education:** This project incorporates gamified XP progressions, interactive dynamic testing modules, and accessible learning content.")

    with col_details:
        # --- AMENDMENT: PORTFOLIO PROFILE ---
        st.markdown(
            """
            <div style="background-color:#EBF5FF; padding:20px; border-radius:12px; border-left:6px solid #1E40AF;">
                <h4 style="margin-top:0; color:#1E3A8A;">Software Architect & EdTech Lead</h4>
                <p style="margin: 5px 0;"><strong>Name:</strong> Abubakar Mubarak</p>
                <p style="margin: 5px 0;"><strong>Designation:</strong> Group 10 Capstone 3 Project</p>
                <p style="margin: 5px 0;"><strong>Specialty:</strong> Educational Technology, Python, Streamlit & SQLite</p>
                <p style="margin: 5px 0;"><strong>Current Version:</strong> v1.2.0 (2026 Edition)</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    # 2. Portfolio / Showcase Section
    st.markdown("### 🛠️ Key Architectural Works")
    st.write("Below are the central active modules driving this system's environment:")

    col_w1, col_w2, col_w3 = st.columns(3)

    with col_w1:
        st.markdown(
            """
            <div class="portfolio-card">
                <h4 style="color:#2563EB; margin-top:0;">📚 Dynamic ICT Lessons</h4>
                <p style="font-size:14px; color:#4B5563;">
                    Houses official syllabus content featuring responsive layout tracking, attachments manager, and structured reading tracks.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_w2:
        st.markdown(
            """
            <div class="portfolio-card">
                <h4 style="color:#2563EB; margin-top:0;">🤖 Generative AI Tutor</h4>
                <p style="font-size:14px; color:#4B5563;">
                    An inclusive teaching assistant that explains programming logic, algorithms, and networks with contextually grounded code.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_w3:
        st.markdown(
            """
            <div class="portfolio-card">
                <h4 style="color:#2563EB; margin-top:0;">📝 Modern Quiz Centre</h4>
                <p style="font-size:14px; color:#4B5563;">
                    An adaptive quiz center supporting Custom Timeouts, Mixed-Topic pools, Self-Paced explanations, and instant XP sync.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    # Hero Button to continue to app
    if st.button("🔓 Enter LEARN-AI Application ➡️", type="primary", use_container_width=True):
        st.session_state.visited_welcome = True
        st.rerun()

    st.stop()  # Halt execution so the user cannot view credentials screens yet


# ---------------------------------------------------------
# SCREEN 1: LOGIN / REGISTRATION PAGE
# ---------------------------------------------------------

if not st.session_state.logged_in:

    st.title("📱 LEARN-AI Mobile")
    st.subheader("AI-Powered Inclusive ICT Learning Platform")

    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])

    # --- LOGIN ---
    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login = st.form_submit_button("Login")

        if login:
            ok, result = login_user(username, password)
            if ok:
                st.session_state.logged_in = True
                st.session_state.username = result["username"]
                st.session_state.fullname = result["fullname"]
                st.session_state.role = result["role"]
                st.session_state.xp = result["xp"]
                st.session_state.streak = result["streak"]

                # Redirect to home Dashboard on login
                st.session_state.navigation_radio = "🏠 Dashboard"
                st.success("Login Successful")
                st.rerun()
            else:
                st.error(result)

    # --- REGISTER ---
    with tab2:
        with st.form("register_form"):
            fullname = st.text_input("Full Name")
            username = st.text_input("Choose Username")
            password = st.text_input("Choose Password", type="password")
            role = st.selectbox("Account Type", ["Student", "Teacher"])
            register = st.form_submit_button("Create Account")

        if register:
            ok, message = register_user(
                username=username,
                password=password,
                fullname=fullname,
                role=role
            )
            if ok:
                st.success(message)
            else:
                st.error(message)

    # Simple option to step back to the welcoming page
    if st.button("⬅️ Back to Developer Info", use_container_width=True):
        st.session_state.visited_welcome = False
        st.rerun()

    st.stop()  # Keep execution stopped until users authenticate


# ---------------------------------------------------------
# SIDEBAR NAVIGATION (ROLE-BASED FILTERING)
# ---------------------------------------------------------

with st.sidebar:
    st.image(
        "https://img.icons8.com/color/96/artificial-intelligence.png",
        width=80
    )
    st.title("LEARN-AI")

    st.success(
        f"Logged in as\n\n**{st.session_state.fullname}**\n\nRole: {st.session_state.role}"
    )

    nav_options = [
        "🏠 Dashboard",
        "📚 ICT Lessons",
        "🤖 AI Tutor",
        "📝 Quiz Centre",
        "📈 Analytics"
    ]

    # Safely append exclusive dashboards depending on role
    if st.session_state.role == "Teacher":
        nav_options.append("👨‍🏫 Teacher Dashboard")
    else:
        nav_options.append("🎓 Student Portal")

    nav_options.append("⚙ Settings")

    # Connected directly to programmatically updated session state
    page = st.radio(
        "Navigation",
        options=nav_options,
        key="navigation_radio"
    )

    st.divider()

    st.metric("XP", st.session_state.xp)
    st.metric("Study Streak", f"{st.session_state.streak} Days")
    st.divider()

    # Clear states safely on logout
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.fullname = ""
        st.session_state.role = ""
        st.session_state.xp = 0
        st.session_state.streak = 0

        if "navigation_radio" in st.session_state:
            del st.session_state["navigation_radio"]
        if "redirect_to" in st.session_state:
            del st.session_state["redirect_to"]

        # Reset gateway to show Abubakar Mubarak's details upon logging out
        st.session_state.visited_welcome = False

        st.rerun()


# ---------------------------------------------------------
# ROUTING CONTROLLER
# ---------------------------------------------------------

if page == "🏠 Dashboard":

    st.title("🏠 LEARN-AI Dashboard")
    st.markdown(f"### Welcome back, **{st.session_state.fullname}** 👋\nContinue your ICT learning journey today.")
    st.divider()

    # --- METRICS ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("⭐ XP", st.session_state.xp, "+0")
    with col2:
        st.metric("🔥 Streak", f"{st.session_state.streak} Days")
    with col3:
        st.metric("📚 Lessons", "0 / 8")
    with col4:
        st.metric("🏆 Badge", "Beginner")
    st.divider()

    # --- QUICK ACTIONS ---
    st.subheader("🚀 Quick Actions")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.button(
            "📚 Continue Learning",
            use_container_width=True,
            key="dashboard_continue_learning",
            on_click=switch_page,
            args=("📚 ICT Lessons",)
        )
    with c2:
        st.button(
            "📝 Take Quiz",
            use_container_width=True,
            key="dashboard_take_quiz",
            on_click=switch_page,
            args=("📝 Quiz Centre",)
        )
    with c3:
        st.button(
            "🤖 Ask AI Tutor",
            use_container_width=True,
            key="dashboard_ask_tutor",
            on_click=switch_page,
            args=("🤖 AI Tutor",)
        )
    st.divider()

    # --- DAILY MOTIVATION ---
    st.subheader("💡 Daily Motivation")
    quotes = [
        "Learning never exhausts the mind.",
        "Small progress every day leads to big success.",
        "Consistency beats intensity.",
        "Every expert was once a beginner.",
        "Knowledge grows when it is shared."
    ]
    st.info(random.choice(quotes))
    st.divider()

    # --- ACHIEVEMENTS ---
    st.subheader("🏅 Achievements")
    a1, a2, a3 = st.columns(3)
    with a1:
        st.success("🎖 First Login")
    with a2:
        st.info("🔒 First Quiz")
    with a3:
        st.info("🔒 ICT Explorer")
    st.divider()

    # --- RECENT ACTIVITY ---
    st.subheader("📈 Recent Activity")
    st.write("• Logged into LEARN-AI")
    st.write("• Dashboard accessed")
    st.write("• Ready to begin learning")

elif page == "📚 ICT Lessons":
    import modules.ICT_Lessons as ICT_Lessons
    ICT_Lessons.show_lessons_page()

elif page == "🤖 AI Tutor":
    import modules.AI_Tutor as AI_Tutor
    AI_Tutor.show_ai_tutor_page()

elif "Quiz Centre" in page:
    import modules.Quiz_Center as Quiz_Center
    Quiz_Center.show_quiz_center_page()

elif "Teacher Dashboard" in page:
    if st.session_state.role == "Teacher":
        Teacher_Dashboard.show_teacher_dashboard_page()
    else:
        st.error("Unauthorized: Teacher authorization is required to access this resource.")

elif "Student Portal" in page:
    Student_Dashboard.show_student_dashboard_page()

elif "Analytics" in page:
    import modules.Analytics as Analytics
    Analytics.show_analytics_page()

elif "Settings" in page:
    import modules.Settings as Settings
    Settings.show_settings_page()

else:
    st.title(page)
    st.info("This module will be implemented in the next stages.")