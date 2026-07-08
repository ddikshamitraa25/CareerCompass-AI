"""
Career Compass AI - Your Personal AI Career Mentor
=====================================================
Made with ❤️ using Streamlit + Gemini

Developed by Diksha Mitra

Version 1.0
License: MIT
"""

import os
import time
import random

import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# ----------------------------------------------------------------------------
# APP CONFIGURATION
# ----------------------------------------------------------------------------
load_dotenv()

APP_NAME = "Career Compass AI"
APP_TAGLINE = "Your Personal AI Career Mentor"
MODEL_NAME = "gemini-2.5-flash"

st.set_page_config(
    page_title=f"{APP_NAME} | {APP_TAGLINE}",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------------
# CUSTOM CSS - MODERN GRADIENT / CARD BASED UI
# ----------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
    /* ---------- Global ---------- */
    html, body, [class*="css"]  {
        font-family: 'Segoe UI', 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }

    /* ---------- Hero Header ---------- */
    .hero-container {
        background: linear-gradient(120deg, #7F00FF 0%, #E100FF 50%, #00C6FF 100%);
        padding: 2.2rem 2rem;
        border-radius: 20px;
        margin-bottom: 1.6rem;
        box-shadow: 0 10px 35px rgba(126, 0, 255, 0.35);
        text-align: center;
    }
    .hero-title {
        color: #ffffff;
        font-size: 2.4rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: 0.5px;
    }
    .hero-subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1.05rem;
        margin-top: 0.4rem;
        font-weight: 400;
    }

    /* ---------- Cards ---------- */
    .cc-card {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(6px);
        border-radius: 16px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1.1rem;
        box-shadow: 0 4px 18px rgba(0,0,0,0.25);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .cc-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 26px rgba(0,0,0,0.35);
    }

    .cc-feature-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.3rem;
    }
    .cc-feature-desc {
        color: rgba(255,255,255,0.75);
        font-size: 0.92rem;
        margin-bottom: 0.8rem;
    }

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 1px solid rgba(255,255,255,0.08);
    }
    section[data-testid="stSidebar"] * {
        color: #f1f1f1 !important;
    }

    /* ---------- Buttons ---------- */
    div.stButton > button {
        background: linear-gradient(90deg, #7F00FF, #E100FF);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.4rem;
        font-weight: 600;
        transition: 0.25s ease;
        width: 100%;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 18px rgba(225, 0, 255, 0.45);
    }

    /* ---------- Text inputs ---------- */
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(255,255,255,0.08) !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
    }

    /* ---------- Response Box ---------- */
    .cc-response-box {
        background: rgba(255,255,255,0.07);
        border-left: 4px solid #E100FF;
        border-radius: 12px;
        padding: 1.3rem 1.5rem;
        color: #f5f5f5;
        line-height: 1.6;
        margin-top: 1rem;
    }

    /* ---------- Footer ---------- */
    .cc-footer {
        text-align: center;
        padding: 1.4rem 0 0.6rem 0;
        color: rgba(255,255,255,0.55);
        font-size: 0.85rem;
        border-top: 1px solid rgba(255,255,255,0.1);
        margin-top: 2.5rem;
    }

    /* ---------- Badges ---------- */
    .cc-badge {
        display: inline-block;
        background: rgba(0, 198, 255, 0.18);
        color: #7be0ff;
        border: 1px solid rgba(0, 198, 255, 0.4);
        border-radius: 20px;
        padding: 0.15rem 0.7rem;
        font-size: 0.75rem;
        margin-right: 0.4rem;
        margin-bottom: 0.4rem;
    }

    /* Hide Streamlit default chrome */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# CONSTANTS
# ----------------------------------------------------------------------------
FEATURES = {
    "🏠 Home": "home",
    "🎯 Explain Career": "explain_career",
    "🛠️ Required Skills": "required_skills",
    "🗺️ Learning Roadmap": "learning_roadmap",
    "📅 Daily Study Plan": "daily_study_plan",
    "🎤 Interview Questions": "interview_questions",
    "📄 Resume Tips": "resume_tips",
    "📝 Generate Quiz": "generate_quiz",
    "💬 Ask Anything": "ask_anything",
    "✨ Motivation Quote": "motivation_quote",
    "📚 Learning Resources": "learning_resources",
    "ℹ️ About": "about",
}

MOTIVATION_FALLBACKS = [
    "Success is the sum of small efforts, repeated day in and day out.",
    "Your only limit is the one you set for yourself. Keep learning!",
    "Every expert was once a beginner. Keep going.",
    "Discipline beats motivation. Show up today, even a little.",
    "The future belongs to those who prepare for it today.",
]

# ----------------------------------------------------------------------------
# GEMINI API SETUP
# ----------------------------------------------------------------------------
def get_api_key() -> str:
    """Retrieve the Gemini API key from environment variables or Streamlit secrets."""
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
        except Exception:
            api_key = ""
    return api_key


def configure_gemini() -> bool:
    """Configure the Gemini client. Returns True if configuration succeeded."""
    api_key = get_api_key()
    if not api_key:
        return False
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception:
        return False


def call_gemini(prompt: str, temperature: float = 0.7) -> str:
    """
    Send a prompt to the Gemini model and return the generated text.
    Handles errors gracefully and returns a user-friendly message on failure.
    """
    if not configure_gemini():
        return (
            "⚠️ **API key not found.** Please add your `GEMINI_API_KEY` to a `.env` "
            "file or Streamlit secrets. See the README for setup instructions."
        )

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        generation_config = genai.types.GenerationConfig(temperature=temperature)
        response = model.generate_content(prompt, generation_config=generation_config)

        if hasattr(response, "text") and response.text:
            return response.text.strip()
        return "⚠️ The AI did not return any content. Please try rephrasing your request."

    except Exception as error:  # noqa: BLE001
        return f"❌ **Something went wrong while contacting Gemini API.**\n\nDetails: `{error}`"


# ----------------------------------------------------------------------------
# PROMPT BUILDERS (AI PERSONA APPLIED)
# ----------------------------------------------------------------------------
PERSONA_INSTRUCTION = (
    "You are Career Compass AI, a friendly, encouraging, and knowledgeable AI career "
    "mentor. You speak in a warm, supportive, and professional tone, like an experienced "
    "mentor guiding a student. Use simple language, clear structure, bullet points, and "
    "headings where helpful. Always stay accurate and practical."
)


def build_prompt(task_instruction: str) -> str:
    """Wrap any task-specific instruction with the mentor persona."""
    return f"{PERSONA_INSTRUCTION}\n\nTASK:\n{task_instruction}"


def prompt_explain_career(career: str) -> str:
    return build_prompt(
        f"Explain the career path '{career}' to a beginner in a clear, engaging way. "
        f"Cover: what the role involves day-to-day, why it matters, typical work "
        f"environment, and career growth potential. Keep it beginner-friendly and "
        f"organized with headings."
    )


def prompt_required_skills(career: str) -> str:
    return build_prompt(
        f"List the required skills for a career in '{career}'. Separate the answer into "
        f"'Technical Skills' and 'Soft Skills' sections, using bullet points. Briefly "
        f"explain why each skill matters."
    )


def prompt_learning_roadmap(career: str) -> str:
    return build_prompt(
        f"Create a step-by-step learning roadmap for someone who wants to become a "
        f"'{career}', starting from beginner level. Break it into phases (e.g., "
        f"Foundations, Intermediate, Advanced, Job-Ready) with topics to learn in each "
        f"phase and approximate time estimates."
    )


def prompt_daily_study_plan(career: str, hours: str) -> str:
    return build_prompt(
        f"Design a practical daily study plan for someone learning to become a "
        f"'{career}', who can dedicate {hours} hours per day. Break the plan into a "
        f"weekly table (Day 1-7) with topics and short tasks. Keep it realistic and "
        f"achievable."
    )


def prompt_interview_questions(career: str, level: str) -> str:
    return build_prompt(
        f"Generate 10 common interview questions for a '{level}' level candidate "
        f"applying for a '{career}' role. Include a mix of technical and behavioral "
        f"questions. After the list, briefly explain how to approach answering them."
    )


def prompt_resume_tips(career: str) -> str:
    return build_prompt(
        f"Provide detailed resume-writing tips for someone applying to '{career}' "
        f"roles. Include sections on: formatting, keywords/ATS optimization, project "
        f"presentation, and common mistakes to avoid."
    )


def prompt_generate_quiz(topic: str, num_questions: str) -> str:
    return build_prompt(
        f"Create a {num_questions}-question multiple choice quiz on the topic "
        f"'{topic}' for a learner preparing for a career in this field. For each "
        f"question, provide 4 options labeled A-D, then clearly state the correct "
        f"answer and a one-line explanation. Number the questions."
    )


def prompt_ask_anything(question: str) -> str:
    return build_prompt(
        f"Answer the following student question about careers, learning, or the job "
        f"market as helpfully and accurately as possible:\n\n'{question}'"
    )


def prompt_motivation_quote(mood: str) -> str:
    return build_prompt(
        f"Give one short, original, powerful motivational quote for a student who is "
        f"feeling '{mood}' about their career journey. Follow it with one sentence of "
        f"encouragement. Keep the entire response under 60 words."
    )


def prompt_learning_resources(career: str) -> str:
    return build_prompt(
        f"Recommend high-quality learning resources (free and paid) for someone "
        f"studying to become a '{career}'. Organize into categories: Online Courses, "
        f"YouTube Channels, Books, and Communities/Forums. Give 2-3 items per category."
    )


# ----------------------------------------------------------------------------
# UI HELPER FUNCTIONS
# ----------------------------------------------------------------------------
def render_hero() -> None:
    """Render the top hero banner."""
    st.markdown(
        f"""
        <div class="hero-container">
            <p class="hero-title">🧭 {APP_NAME}</p>
            <p class="hero-subtitle">{APP_TAGLINE}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_response(content: str) -> None:
    """Render an AI response inside a styled box."""
    st.markdown(f'<div class="cc-response-box">{content}</div>', unsafe_allow_html=True)


def render_feature_header(title: str, description: str) -> None:
    """Render a feature section header card."""
    st.markdown(
        f"""
        <div class="cc-card">
            <p class="cc-feature-title">{title}</p>
            <p class="cc-feature-desc">{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def validate_input(value: str, field_name: str = "This field") -> bool:
    """Simple input validation helper. Shows a warning if empty."""
    if not value or not value.strip():
        st.warning(f"⚠️ {field_name} cannot be empty. Please enter a value.")
        return False
    return True


def generate_with_spinner(prompt: str, spinner_text: str = "🧠 Thinking...") -> str:
    """Call Gemini while showing a loading spinner, with basic retry-friendly UX."""
    with st.spinner(spinner_text):
        time.sleep(0.3)  # tiny UX delay so spinner is visibly smooth
        return call_gemini(prompt)


# ----------------------------------------------------------------------------
# FEATURE PAGES
# ----------------------------------------------------------------------------
def page_home() -> None:
    render_feature_header(
        "👋 Welcome to Career Compass AI",
        "Your all-in-one AI-powered mentor for exploring careers, building skills, "
        "and staying motivated on your learning journey.",
    )

    cols = st.columns(3)
    highlights = [
        ("🎯", "Explore Careers", "Understand any career path in plain language."),
        ("🗺️", "Plan Your Growth", "Get roadmaps and daily study plans tailored to you."),
        ("📝", "Practice & Prepare", "Quizzes and interview questions to test yourself."),
    ]
    for col, (icon, title, desc) in zip(cols, highlights):
        with col:
            st.markdown(
                f"""
                <div class="cc-card" style="text-align:center;">
                    <div style="font-size:2rem;">{icon}</div>
                    <p class="cc-feature-title">{title}</p>
                    <p class="cc-feature-desc">{desc}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("### 🚀 Explore All Features")
    feature_list = [k for k in FEATURES if k not in ("🏠 Home", "ℹ️ About")]
    badges_html = "".join(f'<span class="cc-badge">{f}</span>' for f in feature_list)
    st.markdown(f'<div class="cc-card">{badges_html}</div>', unsafe_allow_html=True)

    st.info("👈 Use the sidebar to navigate between features and start your journey!")


def page_explain_career() -> None:
    render_feature_header("🎯 Explain Career", "Get a clear, beginner-friendly breakdown of any career.")
    career = st.text_input("Enter a career title", placeholder="e.g., Data Scientist, UX Designer")
    if st.button("Explain This Career", key="btn_explain_career"):
        if validate_input(career, "Career title"):
            result = generate_with_spinner(prompt_explain_career(career), "🧠 Researching this career...")
            render_response(result)


def page_required_skills() -> None:
    render_feature_header("🛠️ Required Skills", "Discover the technical and soft skills needed for a career.")
    career = st.text_input("Enter a career title", placeholder="e.g., Full Stack Developer", key="skills_career")
    if st.button("Get Required Skills", key="btn_skills"):
        if validate_input(career, "Career title"):
            result = generate_with_spinner(prompt_required_skills(career), "🧠 Compiling skill list...")
            render_response(result)


def page_learning_roadmap() -> None:
    render_feature_header("🗺️ Learning Roadmap", "Get a phase-by-phase roadmap from beginner to job-ready.")
    career = st.text_input("Enter a career title", placeholder="e.g., Machine Learning Engineer", key="roadmap_career")
    if st.button("Generate Roadmap", key="btn_roadmap"):
        if validate_input(career, "Career title"):
            result = generate_with_spinner(prompt_learning_roadmap(career), "🧠 Mapping your roadmap...")
            render_response(result)


def page_daily_study_plan() -> None:
    render_feature_header("📅 Daily Study Plan", "Get a realistic weekly study plan based on your availability.")
    career = st.text_input("Enter a career title", placeholder="e.g., Cloud Engineer", key="study_career")
    hours = st.selectbox("Hours available per day", ["1", "2", "3", "4", "5+"], key="study_hours")
    if st.button("Create Study Plan", key="btn_study_plan"):
        if validate_input(career, "Career title"):
            result = generate_with_spinner(
                prompt_daily_study_plan(career, hours), "🧠 Building your weekly plan..."
            )
            render_response(result)


def page_interview_questions() -> None:
    render_feature_header("🎤 Interview Questions", "Practice with common interview questions and tips.")
    career = st.text_input("Enter a career title", placeholder="e.g., Backend Developer", key="interview_career")
    level = st.selectbox("Experience level", ["Fresher", "Junior", "Mid-Level", "Senior"], key="interview_level")
    if st.button("Generate Interview Questions", key="btn_interview"):
        if validate_input(career, "Career title"):
            result = generate_with_spinner(
                prompt_interview_questions(career, level), "🧠 Preparing interview questions..."
            )
            render_response(result)


def page_resume_tips() -> None:
    render_feature_header("📄 Resume Tips", "Get tailored resume advice for your target career.")
    career = st.text_input("Enter a career title", placeholder="e.g., Product Manager", key="resume_career")
    if st.button("Get Resume Tips", key="btn_resume"):
        if validate_input(career, "Career title"):
            result = generate_with_spinner(prompt_resume_tips(career), "🧠 Reviewing best resume practices...")
            render_response(result)


def page_generate_quiz() -> None:
    render_feature_header("📝 Generate Quiz", "Test your knowledge with an AI-generated quiz.")
    topic = st.text_input("Enter a topic", placeholder="e.g., Python Basics, Networking", key="quiz_topic")
    num_questions = st.selectbox("Number of questions", ["3", "5", "10"], key="quiz_count")
    if st.button("Generate Quiz", key="btn_quiz"):
        if validate_input(topic, "Topic"):
            result = generate_with_spinner(
                prompt_generate_quiz(topic, num_questions), "🧠 Writing quiz questions..."
            )
            render_response(result)


def page_ask_anything() -> None:
    render_feature_header("💬 Ask Anything", "Ask your AI mentor any career or learning-related question.")
    question = st.text_area(
        "Type your question", placeholder="e.g., How do I switch careers into tech?", key="ask_question"
    )
    if st.button("Ask Career Compass AI", key="btn_ask"):
        if validate_input(question, "Question"):
            result = generate_with_spinner(prompt_ask_anything(question), "🧠 Thinking about your question...")
            render_response(result)


def page_motivation_quote() -> None:
    render_feature_header("✨ Motivation Quote", "Get an instant boost of motivation.")
    mood = st.selectbox(
        "How are you feeling today?",
        ["Unmotivated", "Stressed", "Confident", "Confused", "Excited", "Tired"],
        key="mood_select",
    )
    if st.button("Get Motivation", key="btn_motivation"):
        result = generate_with_spinner(prompt_motivation_quote(mood), "✨ Finding the right words...")
        if result.startswith("⚠️") or result.startswith("❌"):
            result = random.choice(MOTIVATION_FALLBACKS)
        render_response(result)


def page_learning_resources() -> None:
    render_feature_header("📚 Learning Resources", "Get curated courses, books, and communities for your career.")
    career = st.text_input("Enter a career title", placeholder="e.g., DevOps Engineer", key="resources_career")
    if st.button("Find Resources", key="btn_resources"):
        if validate_input(career, "Career title"):
            result = generate_with_spinner(prompt_learning_resources(career), "🧠 Curating resources...")
            render_response(result)


def page_about() -> None:
    render_feature_header("ℹ️ About Career Compass AI", "Learn more about this project.")
    st.markdown(
        """
        <div class="cc-card">
        <p class="cc-feature-desc">
        <b>Career Compass AI</b> is an AI-powered learning buddy built with
        <b>Streamlit</b> and the <b>Google Gemini API</b>. It acts as a friendly
        career mentor, helping students and early-career professionals explore
        careers, build learning roadmaps, prepare for interviews, and stay
        motivated.
        </p>
        <p class="cc-feature-desc">
        <b>Built with:</b> Python · Streamlit · Google Generative AI SDK · Custom CSS
        </p>
        <p class="cc-feature-desc">
        <b>Version:</b> 1.0.0 &nbsp;|&nbsp; <b>License:</b> MIT
        </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


PAGE_RENDERERS = {
    "home": page_home,
    "explain_career": page_explain_career,
    "required_skills": page_required_skills,
    "learning_roadmap": page_learning_roadmap,
    "daily_study_plan": page_daily_study_plan,
    "interview_questions": page_interview_questions,
    "resume_tips": page_resume_tips,
    "generate_quiz": page_generate_quiz,
    "ask_anything": page_ask_anything,
    "motivation_quote": page_motivation_quote,
    "learning_resources": page_learning_resources,
    "about": page_about,
}


# ----------------------------------------------------------------------------
# SIDEBAR NAVIGATION
# ----------------------------------------------------------------------------
def render_sidebar() -> str:
    """Render sidebar navigation and return the selected page key."""
    with st.sidebar:
        st.markdown("## 🧭 Career Compass AI")
        st.caption(APP_TAGLINE)
        st.markdown("---")

        selection = st.radio("Navigate", list(FEATURES.keys()), label_visibility="collapsed")

        st.markdown("---")
        api_status = "🟢 Connected" if get_api_key() else "🔴 API Key Missing"
        st.caption(f"**Gemini API Status:** {api_status}")
        if not get_api_key():
            st.caption("Add `GEMINI_API_KEY` to your `.env` file. See README for help.")

        st.markdown("---")
        st.caption("Made with ❤️ using Streamlit + Gemini API")

    return FEATURES[selection]


# ----------------------------------------------------------------------------
# FOOTER
# ----------------------------------------------------------------------------
def render_footer() -> None:
    st.markdown(
        f"""
        <div class="cc-footer">
            🧭 <b>{APP_NAME}</b> — {APP_TAGLINE}<br>
            Built with Streamlit &amp; Google Gemini API &nbsp;|&nbsp; © 2026 Diksha Mitra
        </div>
        """,
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------------------
# MAIN APP ENTRY POINT
# ----------------------------------------------------------------------------
def main() -> None:
    render_hero()
    page_key = render_sidebar()

    render_function = PAGE_RENDERERS.get(page_key, page_home)
    render_function()

    render_footer()


if __name__ == "__main__":
    main()
