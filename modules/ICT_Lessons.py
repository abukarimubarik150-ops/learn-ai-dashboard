import streamlit as st
import os
import re
from database import get_connection, update_user_xp, increment_user_streak, get_lesson_attachments


def get_lesson_content(lesson_title):
    """
    Returns rich, GES-aligned dynamic lesson notes and an interactive mini-quiz
    by looking for keywords in the selected lesson's title.
    """
    title_clean = lesson_title.lower()

    # -------------------------------------------------------------------------
    # LESSON 1: INTRODUCTION TO COMPUTING
    # -------------------------------------------------------------------------
    if "introduction to computing" in title_clean or "computing" in title_clean:
        notes = """
        ### 💻 Lesson 1: Introduction to Computing

        A **computer** is an electronic device that accepts raw data as input, processes it according to a set of instructions (program), stores the results, and produces output information.

        ---

        #### 1. The Information Processing Cycle
        Every computing task follows four main stages:
        1. **Input:** Feeding raw data into the system. *(e.g., typing text on a keyboard).*
        2. **Processing:** The CPU manipulating data into meaningful information.
        3. **Storage:** Keeping digital records on a drive *(e.g., HDD or SSD)* for future use.
        4. **Output:** Displaying or presenting the results to the user *(e.g., screen visual or paper printout).*

        ---

        #### 2. Essential Hardware Components
        * **Input Unit:** Keyboard, mouse, scanners, and digital cameras.
        * **Processing Unit (CPU):** Composed of the **Arithmetic Logic Unit (ALU)** for calculations and the **Control Unit (CU)** for routing system signals.
        * **Output Unit:** Monitor, printer, and multimedia projector.
        """
        quiz = {
            "question": "Which component of the Central Processing Unit (CPU) executes mathematical and logical evaluations?",
            "options": ["Control Unit (CU)", "Arithmetic Logic Unit (ALU)", "Random Access Memory (RAM)",
                        "System Registry"],
            "correct": "Arithmetic Logic Unit (ALU)",
            "explanation": "The ALU handles all arithmetic computations (addition, subtraction, etc.) and logical comparisons (greater than, equal to, etc.)."
        }

    # -------------------------------------------------------------------------
    # LESSON 2: INFORMATION AND COMMUNICATION TECHNOLOGY (ICT)
    # -------------------------------------------------------------------------
    elif "information and communication technology" in title_clean or "ict" in title_clean:
        notes = """
        ### 📡 Lesson 2: Information and Communication Technology (ICT)

        **ICT** refers to a broad set of technological tools and resources used to transmit, store, create, share, or exchange information. It merges computing, telecommunications, and broadcasting networks together.

        ---

        #### 1. Core Components of ICT
        * **Information:** Processed, organized data that holds context and meaning for the receiver.
        * **Communication:** The transmission of data from a sender to a receiver through a medium (cables, airwaves, or satellite).
        * **Technology:** The physical machinery (computers, routers, optical fibers) and logical protocols that enable communication.

        ---

        #### 2. Key Impacts of ICT in Ghana
        * **Education:** E-learning platforms (like *LEARN-AI*!), virtual classrooms, and open-source learning repositories.
        * **Financial Sector:** Mobile Money (MoMo) technologies and digital banking systems that enable easy transactions across rural and urban centers.
        * **Administration:** Digital portals for government services (such as passport renewals and tax filings).
        """
        quiz = {
            "question": "Which of the following represents 'Communication' in an ICT context?",
            "options": ["Raw data stored on an offline USB drive",
                        "Transmitting a message from a sender to a receiver over a network",
                        "Typing text into an offline word document", "Running a calculation inside the CPU's ALU"],
            "correct": "Transmitting a message from a sender to a receiver over a network",
            "explanation": "Communication strictly requires the exchange of messages/data across a channel or transmission medium from one node to another."
        }

    # -------------------------------------------------------------------------
    # LESSON 3: RELATIONAL DATABASE CONCEPTS
    # -------------------------------------------------------------------------
    elif "relational database" in title_clean or "database" in title_clean:
        notes = """
        ### 🗃️ Lesson 3: Relational Database Concepts

        A **Relational Database** is a collection of structured data items organized as a set of formally-described tables from which data can be accessed or reassembled in many different ways.

        ---

        #### 1. The Core Building Blocks
        * **Table (Relation):** A structured layout of rows and columns.
        * **Row (Tuple / Record):** A single, complete horizontal entry in a table representing one individual item (e.g., one student or one teacher).
        * **Column (Attribute / Field):** A vertical set of data values of a specific type (e.g., `Age` or `EnrollmentDate`).

        ---

        #### 2. Primary and Foreign Keys
        * **Primary Key (PK):** A column (or set of columns) that uniquely identifies every single row in a table. It *cannot* contain duplicate or null values. *(e.g., student ID `1343637`).*
        * **Foreign Key (FK):** A column in one table that links to a Primary Key in another table. This establishes the **relationship** between the tables.
        """
        quiz = {
            "question": "What is the primary function of a Foreign Key in a relational database?",
            "options": ["To ensure a table cannot contain any duplicate rows",
                        "To establish a link or relationship between two tables",
                        "To speed up data calculations across simple columns",
                        "To encrypt password hashes safely before storage"],
            "correct": "To establish a link or relationship between two tables",
            "explanation": "A Foreign Key points directly to a Primary Key in another table, creating a relational bridge between the records."
        }

    # -------------------------------------------------------------------------
    # LESSON 4: INTERNET ARCHITECTURES & TOPOLOGIES
    # -------------------------------------------------------------------------
    elif "internet architecture" in title_clean or "topology" in title_clean or "architectures" in title_clean:
        notes = """
        ### 🌐 Lesson 4: Internet Architectures & Topologies

        Network **Topology** refers to the structural arrangement of different nodes, links, and devices in a computer network. 

        ---

        #### 1. Common Physical Topologies
        * **Star Topology:** Every computer is connected to a central hub, switch, or router. If one computer's cable breaks, the rest of the network remains operational.
        * **Bus Topology:** All devices share a single backbone communication cable. If the main backbone fails, the entire network drops.
        * **Ring Topology:** Devices are connected in a circular loop. Data packets travel in one direction around the circle.
        * **Mesh Topology:** Every device has a dedicated point-to-point connection to every other device, providing the highest level of redundancy and fault tolerance.

        ---

        #### 2. Network Architectures
        * **Client-Server:** Centralized servers host databases and resources. Clients (user devices) request these files.
        * **Peer-to-Peer (P2P):** Flat structure where all connected nodes share equal responsibility without a central controller.
        """
        quiz = {
            "question": "Which physical network topology is characterized by all devices connecting directly to a central hub or switch?",
            "options": ["Bus Topology", "Ring Topology", "Star Topology", "Mesh Topology"],
            "correct": "Star Topology",
            "explanation": "In a Star layout, the central device manages all routing, making it easy to add or remove machines without disrupting service."
        }

    # -------------------------------------------------------------------------
    # LESSON 5: BASIC ALGORITHM DESIGN & LOGIC
    # -------------------------------------------------------------------------
    elif "algorithm" in title_clean or "logic" in title_clean or "design" in title_clean:
        notes = """
        ### 🧠 Lesson 5: Basic Algorithm Design & Logic

        An **Algorithm** is a step-by-step sequence of instructions or logical rules used to solve a specific problem or complete a computation task.

        ---

        #### 1. Representing Algorithms
        * **Pseudocode:** An informal, high-level description of a computer program written in structured plain English (e.g., `IF score > 50 THEN print Pass`).
        * **Flowcharts:** Standardized graphical diagrams representing step-by-step logic.
          * *Ovals:* Start and End blocks.
          * *Parallelograms:* Input and Output steps.
          * *Rectangles:* Process and Calculation blocks.
          * *Diamonds:* Decision points (True/False checks).

        ---

        #### 2. Control Structures
        * **Sequence:** Following instructions step-by-step, in chronological order.
        * **Selection (Decision):** Making choices based on criteria *(e.g., IF/ELSE statements).*
        * **Iteration (Looping):** Repeating instructions until a specific condition is met *(e.g., WHILE loops).*
        """
        quiz = {
            "question": "In standard flowcharting, which geometric shape represents a Decision or Condition step?",
            "options": ["Rectangle", "Oval", "Parallelogram", "Diamond"],
            "correct": "Diamond",
            "explanation": "Diamond blocks represent logical forks (decisions) that branch the execution flow based on True/False criteria."
        }

    # -------------------------------------------------------------------------
    # LESSON 6: INTRODUCTION TO WORD PROCESSING
    # -------------------------------------------------------------------------
    elif "word processing" in title_clean or "word processor" in title_clean:
        notes = """
        ### 📝 Lesson 6: Introduction to Word Processing

        A **Word Processor** is an application software designed for the creation, editing, formatting, and printing of text-based documents. 

        ---

        #### 1. Core Functions of Word Processors
        Unlike traditional typewriters, digital word processors allow you to manipulate text seamlessly before printing:
        * **Creating:** Typing fresh text into a clean workspace.
        * **Editing:** Modifying existing text (correcting spelling, inserting sentences, or moving paragraphs).
        * **Formatting:** Enhancing the document layout and text styles (adjusting margins, bolding text, changing font sizes).
        * **Saving:** Writing the document to permanent storage so you can access it later.

        ---

        #### 2. Key Interface Elements
        * **Title Bar:** Located at the top of the window, showing the current document name (e.g., *Document1*).
        * **Ribbon/Menu Bar:** The command hub featuring grouped tabs like **Home**, **Insert**, and **Page Layout**.
        * **The Workspace:** The blank white page where you type your content.
        * **Status Bar:** Displays information about the current working state (e.g., Page count, Word count, Zoom percentage).

        ---

        #### 3. Crucial Keyboard Shortcuts (Ghana Curriculum Standards)
        Saving time while typing is a vital practical skill. Memorize these standard shortcuts:
        * **Ctrl + N:** Open a brand new document.
        * **Ctrl + O:** Open an existing document.
        * **Ctrl + S:** Save the current document.
        * **Ctrl + P:** Send the document to the printer.
        """
        quiz = {
            "question": "Which standard keyboard shortcut is used to save changes made to a document?",
            "options": ["Ctrl + S", "Ctrl + N", "Ctrl + P", "Ctrl + V"],
            "correct": "Ctrl + S",
            "explanation": "Ctrl + S is the universal keyboard shortcut used to quickly save documents to active storage, protecting your progress."
        }

    # -------------------------------------------------------------------------
    # FALLBACK
    # -------------------------------------------------------------------------
    else:
        notes = f"""
        ### 📚 Standard Study Module: {lesson_title}
        This module introduces essential competencies, tools, and terminology based on your regional curriculum guidelines.
        """
        quiz = {
            "question": "Which component is central to learning ICT concepts?",
            "options": ["Hands-on practice", "Ignoring system updates", "Disabling hardware", "Bypassing safety"],
            "correct": "Hands-on practice",
            "explanation": "Active engagement with systems reinforces core computational models."
        }

    return notes, quiz


def show_lessons_page():
    # -----------------------------
    # SESSION STATE INITIALIZATION
    # -----------------------------
    if "current_lesson" not in st.session_state:
        st.session_state.current_lesson = 1
    if "completed_lessons" not in st.session_state:
        st.session_state.completed_lessons = []

    # -----------------------------
    # DATABASE FETCH
    # -----------------------------
    lessons = []
    try:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
        except TypeError:
            cursor = conn.cursor()

        cursor.execute("SELECT * FROM lessons ORDER BY id")
        lessons = cursor.fetchall()
        conn.close()
    except Exception as e:
        st.error(f"Database error: {e}")

    st.title("📚 ICT Lessons")
    st.caption("Learn ICT step-by-step with AI guidance calibrated for the Ghana Curriculum.")
    st.divider()

    if not lessons:
        st.warning("No lessons found in the database. Please check your seed script data.")
        return

    # -----------------------------
    # LESSON LAYOUT & SELECTION
    # -----------------------------
    left, right = st.columns([1, 3])

    with left:
        st.subheader("Lessons List")

        lesson_names = []
        lesson_mapping = {}  # Resolves selected sidebar item -> raw DB item
        default_index = 0    # Default to the first lesson in the radio selection

        # Check if a lesson was redirected from the Student Dashboard
        preselected_lesson_id = st.session_state.get("current_lesson_id", None)

        for index, b_lesson in enumerate(lessons):
            if isinstance(b_lesson, dict):
                l_id = b_lesson['id']
                l_title = b_lesson['title']
            else:
                l_id = b_lesson[0]
                l_title = b_lesson[1]

            # Clear duplicate manual prefixes like "Lesson 6: ", etc.
            clean_title = re.sub(r'(?i)^lesson\s*\d+\s*[:\-]?\s*', '', l_title).strip()

            # Format sequential chronological numbers: Lesson 1, Lesson 2...
            display_label = f"Lesson {index + 1}: {clean_title}"
            lesson_names.append(display_label)
            lesson_mapping[display_label] = b_lesson

            # If the student redirected using this lesson ID, set it as active
            if preselected_lesson_id is not None and l_id == preselected_lesson_id:
                default_index = index

        # CRITICAL STREAMLIT FIX: Explicitly set the widget's internal state
        # BEFORE rendering it, overriding old selections from previous runs.
        if preselected_lesson_id is not None and lesson_names:
            st.session_state.lesson_radio_selection = lesson_names[default_index]
            # Clear the redirection key so it doesn't get locked on subsequent runs
            st.session_state.current_lesson_id = None

        # Programmatically set the selected radio item
        selected = st.radio(
            "Select Lesson",
            lesson_names,
            key="lesson_radio_selection"
        )

    # Cleanly fetch the selected row using our mapping container
    lesson = lesson_mapping[selected]

    if isinstance(lesson, dict):
        selected_id = lesson['id']
        title = lesson['title']
        desc = lesson['description']
        diff = lesson['difficulty']
        dur = lesson['duration']
    else:
        selected_id = lesson[0]
        title = lesson[1]
        desc = lesson[2]
        diff = lesson[4] if len(lesson) > 4 else "Intermediate"
        dur = lesson[5] if len(lesson) > 5 else "20 mins"

    # Clean title for layout header rendering
    display_title = re.sub(r'(?i)^lesson\s*\d+\s*[:\-]?\s*', '', title).strip()

    # -----------------------------
    # DISPLAY SELECTED CONTENT
    # -----------------------------
    with right:
        st.subheader(display_title)
        st.write(desc)

        # Micro Badge Metadata Header
        st.markdown(
            f"""
            <div style="background-color:#EBF5FB; padding:10px 15px; border-left: 5px solid #2980B9; border-radius:5px; margin-bottom:15px;">
                <span style="color:#2C3E50; font-weight:bold;">📶 Difficulty:</span> {diff} &nbsp;|&nbsp;
                <span style="color:#2C3E50; font-weight:bold;">⏱️ Estimated Study Time:</span> {dur}
            </div>
            """,
            unsafe_allow_html=True
        )
        st.divider()

        # Dynamic Content Loader matching purely on title keywords
        lesson_notes, mini_quiz = get_lesson_content(title)

        st.markdown(lesson_notes)
        st.divider()

        # -----------------------------
        # LESSON ATTACHMENTS (FILES & LINKS)
        # -----------------------------
        attachments = get_lesson_attachments(selected_id)

        if attachments:
            st.subheader("📥 Lesson Resources & Multimedia")
            st.info("Study these additional media resources or download attached files for offline usage:")

            for item in attachments:
                if item["file_type"] == "file":
                    try:
                        file_path = item["file_path_or_url"]
                        if os.path.exists(file_path):
                            with open(file_path, "rb") as file_bytes:
                                st.download_button(
                                    label=f"💾 Download: {item['file_name']}",
                                    data=file_bytes,
                                    file_name=item["file_name"],
                                    key=f"download_{item['id']}",
                                    use_container_width=True
                                )
                        else:
                            st.warning(f"File not found on server: {item['file_name']}")
                    except Exception as e:
                        st.error(f"Error loading file {item['file_name']}: {e}")

                elif item["file_type"] == "video_link":
                    st.video(item["file_path_or_url"])
                    st.markdown(f"🔗 [Open Video Link]({item['file_path_or_url']})")

                elif item["file_type"] == "podcast_link":
                    st.audio(item["file_path_or_url"])
                    st.markdown(f"🔗 [Open Audio Link]({item['file_path_or_url']})")

                elif item["file_type"] == "doc_link":
                    st.markdown(f"📖 **Additional Reading:** [{item['file_name']}]({item['file_path_or_url']})")

            st.divider()

        # -----------------------------
        # INTERACTIVE QUIZ AREA
        # -----------------------------
        st.subheader("✍️ Quick Check Quiz")
        st.write("Test your understanding before finishing this module:")

        quiz_key = f"quiz_{selected_id}"
        user_choice = st.radio(
            mini_quiz["question"],
            mini_quiz["options"],
            key=quiz_key,
            index=None  # Start unselected
        )

        if user_choice:
            if user_choice == mini_quiz["correct"]:
                st.success(f"🎉 **Correct!** {mini_quiz['explanation']}")
            else:
                st.error(f"❌ **Incorrect!** Try reviewing the key points above. Hint: {mini_quiz['correct']}")

        st.divider()

        # -----------------------------
        # STUDY REVISION NOTES
        # -----------------------------
        st.subheader("📝 My Study Notes")
        notes_key = f"notes_{selected_id}"
        notes = st.text_area("Type your personal revision points here...", height=120, key=notes_key)

        if st.button("💾 Save Notes", key=f"save_{selected_id}"):
            st.success("Notes saved locally for this session.")
        st.divider()

        # -----------------------------
        # BOTTOM CONTROLS & REWARDS
        # -----------------------------
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("⭐ Bookmark", key=f"book_{selected_id}", use_container_width=True):
                st.success("Lesson bookmarked successfully!")
        with c2:
            if st.button("▶ Read Aloud", key=f"read_{selected_id}", use_container_width=True):
                st.info("Text-to-Speech playback integration is loading...")
        with c3:
            if st.button("✅ Complete Lesson", key=f"comp_{selected_id}", type="primary", use_container_width=True):
                if title not in st.session_state.completed_lessons:
                    st.session_state.completed_lessons.append(title)

                    # Update user database details
                    update_user_xp(st.session_state.username, 10)
                    increment_user_streak(st.session_state.username)

                    # IMMEDIATELY synchronize local session state variables
                    st.session_state.xp += 10
                    st.session_state.streak += 1

                    st.success("🎉 Lesson completed! +10 XP earned, and your study streak advanced!")
                    st.rerun()
                else:
                    st.info("You have already completed this lesson module for this session.")