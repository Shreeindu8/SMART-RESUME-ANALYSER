
import streamlit as st
from pypdf import PdfReader
import re

st.set_page_config(
    page_title="Smart Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# -----------------------------------
# SKILL DATABASE
# -----------------------------------
SKILLS = [
    "python", "java", "c", "c++", "sql",
    "html", "css", "javascript",
    "machine learning", "deep learning",
    "data analysis", "data analytics",
    "pandas", "numpy", "pytorch", "tensorflow",
    "streamlit", "flask", "django",
    "aws", "azure", "cloud computing",
    "docker", "kubernetes", "devops",
    "git", "github", "linux",
    "communication", "problem solving",
    "data structures", "algorithms",
    "testing", "selenium", "automation",
    "power bi", "excel", "tableau",
    "mongodb", "database", "rest api",
    "leadership", "teamwork", "project management",
    "agile", "communication skills"
]

# -----------------------------------
# ALTERNATIVE KEYWORD DATABASE
# -----------------------------------
ALTERNATIVES = {
    "data analysis": ["data analytics", "data interpretation"],
    "data analytics": ["data analysis", "business analytics"],
    "machine learning": ["predictive modeling", "ML"],
    "deep learning": ["neural networks", "DL"],
    "python": ["Python programming", "Python development"],
    "sql": ["SQL querying", "relational database querying"],
    "cloud computing": ["cloud technology", "cloud infrastructure"],
    "aws": ["Amazon Web Services", "AWS cloud services"],
    "devops": ["CI/CD", "continuous integration and delivery"],
    "testing": ["software testing", "quality assurance"],
    "automation": ["test automation", "automated workflows"],
    "communication": ["stakeholder communication", "written communication"],
    "teamwork": ["cross-functional collaboration", "team collaboration"],
    "leadership": ["team leadership", "technical leadership"],
    "project management": ["project coordination", "project planning"],
    "database": ["data management", "database management"],
    "rest api": ["RESTful APIs", "API integration"],
    "power bi": ["business intelligence", "BI reporting"],
    "problem solving": ["analytical thinking", "troubleshooting"],
    "data structures": ["DSA", "data structures and algorithms"]
}

# -----------------------------------
# INTERVIEW THEME DATABASE
# -----------------------------------
INTERVIEW_THEMES = {
    "Ownership and initiative": {
        "keywords": [
            "ownership", "independently", "self-starter",
            "initiative", "proactive", "take responsibility",
            "end-to-end"
        ],
        "questions": [
            "Tell me about a time you took ownership of a task.",
            "Describe a problem you solved without being asked.",
            "How do you work when requirements are unclear?"
        ]
    },
    "Teamwork and collaboration": {
        "keywords": [
            "teamwork", "collaboration", "cross-functional",
            "stakeholders", "work with others", "team player"
        ],
        "questions": [
            "Tell me about a time you worked through a team disagreement.",
            "How did you contribute to a group project?",
            "Describe how you handled feedback from a teammate."
        ]
    },
    "Leadership": {
        "keywords": [
            "leadership", "mentor", "lead a team",
            "decision-making", "guide others"
        ],
        "questions": [
            "Describe a time you guided a team toward a goal.",
            "Tell me about a difficult decision you made.",
            "How would you help a teammate who is struggling?"
        ]
    },
    "Adaptability and learning": {
        "keywords": [
            "adaptability", "fast-paced", "learn quickly",
            "changing priorities", "flexible", "new technologies"
        ],
        "questions": [
            "Tell me about a time you learned something quickly.",
            "How do you respond when priorities change?",
            "Describe a mistake and what you learned from it."
        ]
    },
    "Analytical thinking and problem solving": {
        "keywords": [
            "analytical", "problem-solving", "troubleshooting",
            "critical thinking", "debugging", "root cause"
        ],
        "questions": [
            "Describe a difficult technical problem you solved.",
            "How do you investigate a bug you cannot reproduce?",
            "Tell me about a decision you made using data."
        ]
    }
}

# -----------------------------------
# HELPER FUNCTIONS
# -----------------------------------
def extract_pdf_text(uploaded_file):
    try:
        reader = PdfReader(uploaded_file)
        return "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )
    except Exception as error:
        st.error(f"Unable to read PDF: {error}")
        return ""


def contains_term(text, term):
    pattern = r"(?<!\w)" + re.escape(term) + r"(?!\w)"
    return bool(re.search(pattern, text, re.IGNORECASE))


def find_skills(text):
    return [
        skill for skill in SKILLS
        if contains_term(text, skill)
    ]


def ats_checks(text):
    checks = []

    if re.search(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b", text):
        checks.append(("PASS", "Email address detected"))
    else:
        checks.append(("CHECK", "No email address detected"))

    if re.search(r"(?:\+?\d[\d\s().-]{7,}\d)", text):
        checks.append(("PASS", "Possible phone number detected"))
    else:
        checks.append(("CHECK", "No obvious phone number detected"))

    headings = [
        "education", "experience", "projects",
        "skills", "certifications"
    ]

    found_headings = [
        heading for heading in headings
        if re.search(r"\b" + heading + r"\b", text, re.IGNORECASE)
    ]

    if len(found_headings) >= 3:
        checks.append((
            "PASS",
            "Several common resume section headings detected"
        ))
    else:
        checks.append((
            "CHECK",
            "Check whether standard section headings are present"
        ))

    if len(text.split()) >= 80:
        checks.append(("PASS", "Resume text extracted"))
    else:
        checks.append((
            "CHECK",
            "Very little text extracted; inspect the PDF manually"
        ))

    return checks


# -----------------------------------
# APPLICATION HEADER
# -----------------------------------
st.title("📄 Smart Resume Analyzer & Career Assistant")

st.write(
    "Analyze your resume, compare it with a job description, "
    "inspect ATS text extraction, prepare for behavioral interviews, "
    "and discover alternative industry keywords."
)

st.warning(
    "This application provides preliminary checks and suggestions. "
    "It cannot guarantee ATS compatibility or predict actual interview questions."
)

# -----------------------------------
# RESUME INPUT
# -----------------------------------
st.header("1. Upload Your Resume")

uploaded_file = st.file_uploader(
    "Upload a text-based PDF resume",
    type=["pdf"]
)

resume_text = ""

if uploaded_file:
    resume_text = extract_pdf_text(uploaded_file)

    if resume_text.strip():
        st.success("Resume text extracted successfully.")
    else:
        st.warning(
            "No selectable text was extracted. "
            "This can happen with scanned PDFs."
        )

pasted_resume = st.text_area(
    "Or paste resume text here",
    height=150
)

if pasted_resume.strip():
    resume_text = pasted_resume

# -----------------------------------
# JOB DESCRIPTION
# -----------------------------------
st.header("2. Job Description")

job_description = st.text_area(
    "Paste the complete job description",
    height=200,
    placeholder="Paste the job requirements here..."
)

region = st.selectbox(
    "Target job market",
    [
        "India",
        "United States",
        "United Kingdom",
        "Europe",
        "Global"
    ]
)

# -----------------------------------
# RUN ANALYSIS
# -----------------------------------
if st.button("🚀 Analyze Resume", type="primary"):

    if not resume_text.strip():
        st.error("Please upload a PDF or paste your resume text.")

    elif not job_description.strip():
        st.error("Please enter a job description.")

    else:
        # Skill matching
        required_skills = find_skills(job_description)

        matched = [
            skill for skill in required_skills
            if contains_term(resume_text, skill)
        ]

        missing = [
            skill for skill in required_skills
            if skill not in matched
        ]

        score = (
            len(matched) / len(required_skills) * 100
            if required_skills else 0.0
        )

        st.divider()
        st.header("3. Resume Match Dashboard")

        col1, col2, col3 = st.columns(3)
        col1.metric("Skill Match", f"{score:.1f}%")
        col2.metric("Matched Skills", len(matched))
        col3.metric("Missing Skills", len(missing))

        st.progress(int(score))

        with st.expander("View skill-by-skill results", expanded=True):
            if not required_skills:
                st.info(
                    "No skills from the built-in database were detected "
                    "in the job description."
                )

            for skill in required_skills:
                if skill in matched:
                    st.success(f"{skill.title()} — Found")
                else:
                    st.error(f"{skill.title()} — Missing")

        # -----------------------------------
        # FEATURE 1: ATS RENDER / TEXT TESTER
        # -----------------------------------
        st.divider()
        st.header("4. ATS Text Extraction Tester")

        st.write(
            "This shows the text extracted from your resume and checks "
            "for some common issues. It is an approximation, not an exact "
            "copy of any specific employer's ATS."
        )

        ats_results = ats_checks(resume_text)
        passed = sum(
            1 for status, _ in ats_results if status == "PASS"
        )

        st.metric(
            "Preliminary Checks Passed",
            f"{passed} / {len(ats_results)}"
        )

        for status, message in ats_results:
            if status == "PASS":
                st.success(message)
            else:
                st.warning(message)

        with st.expander("View extracted text in reading order"):
            st.text(resume_text)

        st.caption(
            "Tip: Compare this extracted text with your original PDF. "
            "Look for missing content, scrambled headings, merged words "
            "or sections appearing in the wrong order."
        )

        # -----------------------------------
        # FEATURE 2: INTERVIEW TRAP PREDICTOR
        # -----------------------------------
        st.divider()
        st.header("5. Behavioral Interview Predictor")

        st.write(
            "The predictor identifies behavioral themes suggested by "
            "the wording of the job description."
        )

        jd_lower = job_description.lower()
        detected_themes = []

        for theme, data in INTERVIEW_THEMES.items():
            matched_terms = [
                keyword for keyword in data["keywords"]
                if keyword in jd_lower
            ]

            if matched_terms:
                detected_themes.append(
                    (theme, matched_terms, data["questions"])
                )

        if detected_themes:
            for theme, terms, questions in detected_themes:
                with st.expander(f"🎯 {theme}", expanded=True):
                    st.write(
                        "**Job-description signals:** "
                        + ", ".join(terms)
                    )

                    st.write("**Practice questions:**")

                    for question in questions:
                        st.write(f"- {question}")

                    st.write(
                        "**Preparation tip:** Use a real example from "
                        "your college project, internship or teamwork. "
                        "Explain the situation, your action and the result."
                    )
        else:
            st.info(
                "No predefined behavioral themes were detected. "
                "Try pasting a more detailed job description."
            )

        # -----------------------------------
        # FEATURE 3: ALTERNATIVE KEYWORD INJECTOR
        # -----------------------------------
        st.divider()
        st.header("6. Alternative Keyword Suggestions")

        st.write(
            f"Target market: **{region}**. "
            "These suggestions come from a built-in synonym list; "
            "they are not live market research."
        )

        keyword_suggestions = {}

        for skill in missing:
            alternatives = ALTERNATIVES.get(skill, [])

            if alternatives:
                keyword_suggestions[skill] = alternatives

        selected_alternatives = []

        if keyword_suggestions:
            st.write(
                "Select alternatives that accurately describe your "
                "skills or experience."
            )

            for original, alternatives in keyword_suggestions.items():
                choice = st.selectbox(
                    f"Missing skill: {original.title()}",
                    ["Do not add"] + alternatives,
                    key=f"alt_{original}"
                )

                if choice != "Do not add":
                    selected_alternatives.append(
                        (original, choice)
                    )

            if selected_alternatives:
                st.subheader("Review your selected alternatives")

                for original, alternative in selected_alternatives:
                    st.write(
                        f"- **{original.title()}** → {alternative}"
                    )

                suggested_text = "\n".join(
                    f"{original.title()}: {alternative}"
                    for original, alternative in selected_alternatives
                )

                st.download_button(
                    "⬇️ Download Keyword Suggestions",
                    data=suggested_text,
                    file_name="alternative_keywords.txt",
                    mime="text/plain"
                )
        else:
            st.info(
                "No built-in alternatives are available for the "
                "missing skills detected in this job description."
            )

        st.warning(
            "Only use alternative terms that genuinely match your "
            "knowledge and experience. Do not add skills you do not have."
        )

        # -----------------------------------
        # DOWNLOAD FULL REPORT
        # -----------------------------------
        st.divider()
        st.header("7. Download Analysis Report")

        report = f"""
SMART RESUME ANALYZER REPORT
============================

Target market: {region}
Skill match score: {score:.1f}%

Required skills detected:
{', '.join(required_skills) if required_skills else 'None detected'}

Matched skills:
{', '.join(matched) if matched else 'None'}

Missing skills:
{', '.join(missing) if missing else 'None'}

ATS TEXT EXTRACTION CHECKS:
""" 

        for status, message in ats_results:
            report += f"\n{status}: {message}"

        report += "\n\nBEHAVIORAL INTERVIEW THEMES:\n"

        if detected_themes:
            for theme, terms, questions in detected_themes:
                report += f"\n{theme}\n"
                report += "Signals: " + ", ".join(terms) + "\n"

                for question in questions:
                    report += f"- {question}\n"
        else:
            report += "No predefined themes detected.\n"

        report += "\nALTERNATIVE KEYWORD SUGGESTIONS:\n"

        if selected_alternatives:
            for original, alternative in selected_alternatives:
                report += f"- {original} -> {alternative}\n"
        else:
            report += "No alternatives selected.\n"

        st.download_button(
            "📥 Download Full Report",
            data=report,
            file_name="smart_resume_analysis.txt",
            mime="text/plain"
        )

st.divider()
st.caption(
    "Smart Resume Analyzer | Python + Streamlit + pypdf"
)
