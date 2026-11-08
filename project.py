import google.generativeai as genai
import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Chatbot for College Administration", layout="wide")
# Gemini API Configuration
# Gemini API Configuration
API_KEY = "AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # Your actual Gemini API key
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

# Header
st.title("🎓 AI Chatbot for College Administration")
st.write("Smart College Information Management System")

# Information Cards
col1, col2 = st.columns(2)

with col1:
    st.subheader("📅 Exam Schedule")

    exam_schedule = pd.DataFrame({
        "Subject": [
            "MATHS",
            "ATCD",
            "DBMS",
            "PYTHON",
            "AI",
            "LIFE SKILLS"
        ],
        "Date": [
            "25 June 2026",
            "27 June 2026",
            "30 June 2026",
            "03 July 2026",
            "05 July 2026",
            "08 July 2026"
        ],
        "Time": [
            "10:00 AM - 1:00 PM",
            "10:00 AM - 1:00 PM",
            "10:00 AM - 1:00 PM",
            "10:00 AM - 1:00 PM",
            "10:00 AM - 1:00 PM",
            "10:00 AM - 1:00 PM"
        ]
    })

    st.dataframe(exam_schedule, use_container_width=True)

with col2:
    st.subheader("📝 Assignment Deadlines")
    st.write("""
    - PYTHON - MAY 10
    - AI - MAY 13
    - KANNADA - MAY 20
    - DBMS - MAY 25
    - ATCD - MAY 30
    - LIFE SKILLS - JUNE 10
    """)

# Timetable
st.subheader("📚 Weekly Timetable")

timetable = {
    "Day": ["Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
    "10-11": ["PYTHON-Dr.Sujata Malapure", "DBMS-Prof.Bannamma", "ATCD-Dr.Rashmi", "PYTHON-Dr.Sujata Malapure", "PYTHON-Dr.Sujata Malapure", "KANNADA-Dr.Sarika"],
    "11-12": ["AI-Prof.Supriya", "PYTHON-Dr.Sujata Malapure", "KANNADA-Dr.Sarika", "ATCD-Dr.Rashmi", "AI-Prof.Supriya", "LIFE SKILLS-Dr.Swati"],
    "12:15-1:15": ["MATHS-Prof.Geeta", "ATCD-Dr.Rashmi", "MATHS-Prof.Geeta", "DBMS-Prof.Bannamma", "MATHS-Prof.Geeta", "PYTHON-Dr.Sujata Malapure"],
    "2-3": ["DBMS-Prof.Bannamma", "MATHS-Prof.Geeta", "AI-Prof.Supriya", "LAB", "LAB", "AI-Prof.Supriya"],
    "3-4": ["ATCD-Dr.Rashmi", "AI-Prof.Supriya", "LIFE SKILLS-Dr.Swati", "LAB", "LAB", "DBMS-Prof.Bannamma"],
    "4-5": ["PROJECT-Dr.Ayesha Heena", "PROJECT-Dr.Ayesha Heena", "PROJECT-Dr.Ayesha Heena", "LAB", "LAB", "ATCD-Dr.Rashmi"]
}

st.dataframe(timetable, use_container_width=True)

# CGPA Calculator
st.subheader("🎯 SGPA & CGPA Calculator")

m1 = st.number_input("PYTHON Marks /50", 0, 50)
m2 = st.number_input("AI Marks /50", 0, 50)
m3 = st.number_input("MATHS Marks /50", 0, 50)
m4 = st.number_input("DBMS Marks /50", 0, 50)
m5 = st.number_input("ATCD Marks /50", 0, 50)
m6 = st.number_input("KANNADA Marks /50", 0, 50)

if st.button("Calculate CGPA"):
    total = m1 + m2 + m3 + m4 + m5 + m6
    percentage = total / 3
    cgpa = percentage / 9.5

    st.success(f"Percentage: {percentage:.2f}%")
    st.success(f"CGPA: {cgpa:.2f}")

# Chatbot
# ===============================

# =====================================
# AI College Chatbot
# =====================================

st.subheader("🤖 AI College Chatbot")

question = st.text_input("Ask any college-related question")

if st.button("Send"):

    if question:

        message = question.lower()

        # College Database Answers

        if "python teacher" in message:
            reply = "Python teacher is Dr. Sujata Malapure."

        elif "ai teacher" in message:
            reply = "AI teacher is Prof. Supriya Bagewadi."

        elif "dbms teacher" in message:
            reply = "DBMS teacher is Prof. Bannamma Patil."

        elif "maths teacher" in message:
            reply = "Maths teacher is Prof. Geeta."

        elif "exam" in message:
            reply = """
Semester Examination Schedule:

MATHS - 25 June 2026
ATCD - 27 June 2026
DBMS - 30 June 2026
PYTHON - 03 July 2026
AI - 05 July 2026
LIFE SKILLS - 08 July 2026

Time: 10:00 AM - 1:00 PM
"""

        elif "assignment" in message:
            reply = """
Assignment Deadlines:

PYTHON - May 10
AI - May 13
KANNADA - May 20
DBMS - May 25
ATCD - May 30
LIFE SKILLS - June 10
"""

        elif "timetable" in message:
            reply = "Weekly timetable is displayed above."

        elif "cgpa" in message:
            reply = "Use the CGPA Calculator section above."

        else:
            # Gemini AI for Unknown Questions

            prompt = f"""
            You are an AI chatbot for college administration.

            Answer student questions politely and clearly.

            Question:
            {question}
            """

            try:
               response = model.generate_content(prompt)
               reply = response.text
            except Exception as e:
               reply = str(e)
        st.write("### Bot Response")
        st.success(reply)

