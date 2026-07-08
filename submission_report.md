# 📑 Submission Report — Career Compass AI

## 1. Project Title
**Career Compass AI** — *Your Personal AI Career Mentor*

## 2. Objective
To build a professional, fully functional **AI Learning Buddy** application
using **Streamlit** (frontend) and the **Google Gemini API** (backend AI
engine) that helps users explore careers, plan their learning journey, and
stay motivated — while satisfying all core assignment requirements and
demonstrating portfolio-quality software engineering and UI/UX design.

## 3. Tech Stack Used

| Layer | Technology |
|---|---|
| Frontend | Streamlit, Custom CSS, Responsive Layout |
| Backend | Python 3.9+, Google Gemini API (`google-generativeai`) |
| Config Management | `python-dotenv` |
| Deployment Target | Streamlit Community Cloud |

## 4. Features Implemented

1. Explain Career
2. Required Skills
3. Learning Roadmap
4. Daily Study Plan
5. Interview Questions
6. Resume Tips
7. Generate Quiz
8. Ask Anything
9. Motivation Quote
10. Learning Resources

Additional requirements fulfilled:
- ✅ Sidebar navigation with icons and emojis
- ✅ Professional gradient-based, card-driven UI
- ✅ Expandable/structured response sections
- ✅ Loading spinners on every AI request
- ✅ Full error handling (missing API key, API failures, empty input)
- ✅ Input validation across all forms
- ✅ Professional footer and dedicated About section
- ✅ Responsive layout (multi-column on desktop, stacks on smaller screens)

## 5. AI Persona Design

A consistent **"Career Compass AI"** persona — a friendly, encouraging,
knowledgeable career mentor — is injected into every prompt sent to Gemini.
This ensures uniform tone and quality across all ten features. Full details
are documented in `persona.md`.

## 6. Prompt Engineering Approach

Five reusable, parameterized prompt templates were designed (`prompts.md`):
**Explain Topic**, **Real-Life Example**, **Generate Quiz**, **Evaluate
Answer**, and **Full Learning Session**. Each template:
- Begins with the shared persona instruction
- Requests structured output (headings, bullet points, numbered lists)
- Is parameterized with user input (career, topic, hours, level, etc.)
- Uses moderate temperature (0.7) for a balance of accuracy and natural tone

## 7. Error Handling & Validation

- Missing/invalid Gemini API key → friendly warning message + sidebar status
  indicator (🟢/🔴), app does not crash.
- Empty form submissions → inline `st.warning()` messages prevent wasted API
  calls.
- API/network failures → caught exceptions displayed as readable error
  messages instead of raw stack traces.
- Motivation Quote feature includes a **local fallback quote list** in case
  the API is unreachable, ensuring the feature never fully fails.

## 8. UI/UX Highlights

- Custom gradient hero banner and background
- Glassmorphism-style cards with hover effects
- Gradient-themed buttons and inputs
- Sidebar with radio-button navigation, icons, and live API status
- Styled AI response boxes for clear readability
- Consistent iconography and emoji usage throughout

## 9. Testing Performed

- Manually tested all 10 features with multiple sample inputs (valid,
  empty, and edge-case inputs).
- Verified error handling by temporarily removing the API key.
- Verified responsive behavior at different browser widths.
- Verified spinner and response rendering timing.

## 10. Deliverables Included in Submission

- `app.py` — complete, runnable Streamlit application
- `requirements.txt` — dependency list
- `README.md` — full setup, usage, and deployment documentation
- `.env.example`, `.gitignore`, `LICENSE`
- `assets/logo.png` — app branding
- `persona.md`, `prompts.md`, `quiz.md`, `reflection.md`,
  `sample_conversation.md`, `screenshots_guide.md`, `submission_report.md`

## 11. Conclusion

Career Compass AI successfully demonstrates the integration of a modern
Streamlit frontend with the Google Gemini API to create a cohesive,
persona-driven AI learning assistant. The project satisfies all stated
functional requirements while going further with production-quality UI
polish, robust error handling, and complete supporting documentation —
making it suitable both as an academic submission and a portfolio piece.

---
*Prepared as part of the Career Compass AI project submission package.*
