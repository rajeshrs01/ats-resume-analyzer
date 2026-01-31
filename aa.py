import streamlit as st
import pdfplumber
import docx
import re

# =================================================
# TEXT EXTRACTION
# =================================================

def extract_text(file):
    if file.name.endswith(".pdf"):
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                if page.extract_text():
                    text += page.extract_text() + "\n"
        return text

    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        return "\n".join(p.text for p in doc.paragraphs)

    return ""

# =================================================
# HEADER INFO (NAME + CONTACT)
# =================================================

def extract_header_info(raw_text):
    lines = [l.strip() for l in raw_text.split("\n") if l.strip()]
    header = " ".join(lines[:3])

    name = None
    email = None
    phone = None

    name_match = re.search(
        r"\b[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+){1,3}\b", header
    )
    email_match = re.search(
        r"[a-zA-Z][\w\.]*\s*\d*@gmail\.com", header, re.I
    )
    phone_match = re.search(r"\b[6-9]\d{9}\b", header)

    if name_match:
        name = name_match.group(0)
    if email_match:
        email = email_match.group(0).replace(" ", "")
        email = re.sub(r"\d+@gmail\.com", "@gmail.com", email)
    if phone_match:
        phone = phone_match.group(0)

    return name, email, phone

# =================================================
# NORMALIZE TEXT (FOR READABILITY)
# =================================================

def normalize_text(text):
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)
    text = re.sub(r"(\d)([A-Za-z])", r"\1 \2", text)
    text = re.sub(r"([A-Za-z])(\d)", r"\1 \2", text)
    text = re.sub(r"\s*-\s*", "-", text)
    text = text.replace("•", "\n• ")
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()

# =================================================
# EXTRACT ALL SECTIONS (RULE + KEYWORD BASED)
# =================================================

def extract_sections(text):
    sections = {
        "Summary / Objective": [],
        "Skills": [],
        "Education / Qualifications": [],
        "Projects": [],
        "Experience": [],
        "Internship": [],
        "Certifications": [],
        "Other Information": []
    }

    qualification_terms = [
        "bca", "bsc", "b.tech", "btech", "be",
        "mca", "msc", "mba", "degree", "university", "college"
    ]

    skill_terms = [
        "python", "java", "sql", "html", "css", "javascript",
        "linux", "windows", "network", "cyber", "git", "power bi"
    ]

    certification_terms = [
        "certification", "certified", "course", "forage",
        "infosys", "coursera", "udemy", "tutedude"
    ]

    for line in text.split("\n"):
        line = line.strip()
        if len(line) < 15:
            continue

        l = line.lower()

        if "objective" in l or "summary" in l or "profile" in l:
            sections["Summary / Objective"].append(line)

        elif any(t in l for t in skill_terms):
            sections["Skills"].append(line)

        elif any(t in l for t in qualification_terms):
            sections["Education / Qualifications"].append(line)

        elif "project" in l or "developed" in l or "built" in l:
            sections["Projects"].append(line)

        elif "intern" in l:
            sections["Internship"].append(line)

        elif any(t in l for t in certification_terms):
            sections["Certifications"].append(line)

        elif "experience" in l or "role" in l or "simulation" in l:
            sections["Experience"].append(line)

        else:
            sections["Other Information"].append(line)

    return sections

# =================================================
# ATS SCORING + IMPROVEMENTS
# =================================================

def calculate_ats(sections, email, phone, text):
    score = 0
    improvements = []

    if email:
        score += 15
    else:
        improvements.append("Add a professional email address")

    if phone:
        score += 10
    else:
        improvements.append("Add a valid phone number")

    required_sections = [
        "Summary / Objective",
        "Skills",
        "Education / Qualifications",
        "Projects",
        "Experience",
        "Certifications"
    ]

    for sec in required_sections:
        if sections.get(sec):
            score += 10
        else:
            improvements.append(f"Add or improve {sec} section")

    word_count = len(text.split())
    if 300 <= word_count <= 900:
        score += 15
    else:
        improvements.append("Keep resume length between 1–2 pages")

    score = min(score, 100)

    if score >= 80:
        status = "Strong ATS-friendly resume"
    elif score >= 60:
        status = "Moderately ATS-optimized resume"
    else:
        status = "Resume needs significant ATS improvements"

    return score, status, improvements

# =================================================
# STREAMLIT UI
# =================================================

st.set_page_config(page_title="ATS Resume Analyzer", layout="centered")

st.title("📄 ATS Resume Analyzer")
st.write("Upload your resume (PDF or DOCX). The system will extract everything and analyze ATS readiness.")

uploaded = st.file_uploader("Upload Resume", type=["pdf", "docx"])

if uploaded:
    raw_text = extract_text(uploaded)
    clean_text = normalize_text(raw_text)

    name, email, phone = extract_header_info(raw_text)
    sections = extract_sections(clean_text)
    score, status, improvements = calculate_ats(sections, email, phone, clean_text)

    # ---------------- RAW TEXT ----------------
    st.markdown("---")
    st.subheader("🧾 Extracted Resume Text (Cleaned)")
    st.text(clean_text)

    # ---------------- STRUCTURED OUTPUT ----------------
    st.markdown("---")
    st.subheader("📋 Structured Resume Information")

    st.write(f"**Name:** {name or 'Not detected'}")
    st.write(f"**Contact:** {email or 'Not detected'} | {phone or 'Not detected'}")

    for sec, lines in sections.items():
        if lines:
            st.markdown(f"### {sec}")
            for l in lines:
                st.write(f"- {l}")

    # ---------------- ATS RESULT ----------------
    st.markdown("---")
    st.subheader(f"📊 ATS Score: {score}/100")
    st.write(f"**Status:** {status}")

    st.subheader("🛠 Improvements to be Done")
    if improvements:
        for imp in improvements:
            st.write(f"- {imp}")
    else:
        st.write("No major improvements needed 🎉")
