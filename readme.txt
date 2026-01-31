▶️ How to Run the Project (Step-by-Step)
1️⃣ Install Python

Make sure Python 3.8 or above is installed.

Check version:

python --version

2️⃣ Install Required Libraries

Create a file named requirements.txt with:

streamlit
pdfplumber
python-docx


Then install:

pip install -r requirements.txt

3️⃣ Run the Streamlit App

In the project folder:

streamlit run aa.py

4️⃣ Open in Browser

Streamlit will open automatically or show a URL like:

http://localhost:8501


Open it in your browser 🎉

📊 Output Generated

Clean extracted resume text

Structured resume sections

Name & contact information

ATS score

ATS readiness status

Improvement suggestions

🎓 Use Case (For Viva / Interview)

“This project simulates an Applicant Tracking System by extracting unstructured resume text, structuring the data using rule-based NLP, evaluating ATS compatibility, and providing actionable feedback.”

🔮 Future Enhancements

Job Description (JD) matching

Skill gap analysis

PDF export of ATS report

Online deployment (Streamlit Cloud)