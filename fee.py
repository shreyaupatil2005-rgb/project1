import streamlit as st

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI College Chatbot",
    page_icon="🎓",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

.main{
    background-color:#f4f7fb;
}

.title{
    background:#1e3c72;
    color:white;
    padding:20px;
    border-radius:12px;
    text-align:center;
}

.card{
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0px 4px 10px rgba(0,0,0,0.1);
    margin-bottom:20px;
}

.info-box{
    background:white;
    padding:20px;
    border-radius:15px;
    border-left:6px solid #1e3c72;
    margin-top:15px;
}

.chat-box{
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0px 4px 10px rgba(0,0,0,0.1);
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------

st.markdown("""
<div class="title">
    <h1>AI Chatbot for College Administration</h1>
    <p>Smart College Information Management System</p>
</div>
""", unsafe_allow_html=True)

st.write("")

# ---------------- COLLEGE INFORMATION ----------------

college_data = {
    "admission": """
📌 Admission Details

• Admission Starts: June 10
• Eligibility: 12th Pass
• Required Documents:
    - 10th Marks Card
    - 12th Marks Card
    - Aadhar Card
    - Passport Photos
""",

    "fee": """
💰 Fee Structure

• B.Tech: ₹1,07,495 per year
• BSc CS: ₹50,000 per year
• BCA: ₹45,000 per year
• BCom: ₹35,000 per year
• Hostel Fee: ₹60,000 per year
""",

    "exam": """
📝 Exam Schedule

• Internal Exams: July 10
• Practical Exams: August 5
• Semester Exams: August 20
""",

    "attendance": """
📊 Attendance Details

• Minimum Attendance Required: 75%
• Current Attendance Portal Available
• Students below 75% cannot attend exams
""",

    "assignment": """
📚 Assignment Details

• Python Project: June 25
• DBMS Assignment: June 28
• AI Report: July 2
""",

    "scholarship": """
🎓 Scholarships Available

• Merit Scholarship
• Sports Scholarship
• SC/ST Scholarship
• Girls Scholarship
• Research Scholarship
""",

    "placement": """
🏢 Placement Information

• TCS Drive: July 15
• Infosys Recruitment: July 20
• Wipro Interview: July 25
• Average Package: ₹4.5 LPA
""",

    "timetable": """
📅 Timetable

Monday:
• Maths
• Python
• DBMS

Tuesday:
• Java
• OS
• AI

Wednesday:
• Python Lab
• Maths
• DBMS
"""
}

# ---------------- CARDS ----------------

st.subheader("College Services")

col1, col2, col3, col4 = st.columns(4)

services = [
    "Admission",
    "Fee Structure",
    "Exam Schedules",
    "Attendance",
    "Assignments",
    "Scholarships",
    "Placements",
    "Timetable"
]

for i, service in enumerate(services):

    with [col1, col2, col3, col4][i % 4]:

        st.markdown(f"""
        <div class="card">
            <h3 style="color:#1e3c72;">{service}</h3>
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"View {service}"):

            keyword = service.lower()

            if "fee" in keyword:
                keyword = "fee"

            elif "exam" in keyword:
                keyword = "exam"

            elif "assignment" in keyword:
                keyword = "assignment"

            elif "scholarship" in keyword:
                keyword = "scholarship"

            elif "placement" in keyword:
                keyword = "placement"

            elif "attendance" in keyword:
                keyword = "attendance"

            elif "timetable" in keyword:
                keyword = "timetable"

            else:
                keyword = "admission"

            st.markdown(f"""
            <div class="info-box">
            {college_data[keyword]}
            </div>
            """, unsafe_allow_html=True)

# ---------------- AI CHATBOT ----------------

st.write("")
st.write("")

st.markdown("""
<div class="chat-box">
    <h2 style="color:#1e3c72;">College AI Chatbot</h2>
</div>
""", unsafe_allow_html=True)

user_question = st.text_input(
    "Ask any college-related question"
)

# ---------------- AI RESPONSE SYSTEM ----------------

if user_question:

    question = user_question.lower()

    response = ""

    # Admission Questions
    if (
        "admission" in question or
        "apply" in question or
        "eligibility" in question or
        "documents" in question
    ):
        response = college_data["admission"]

    # Fee Questions
    elif (
        "fee" in question or
        "fees" in question or
        "payment" in question or
        "hostel fee" in question
    ):
        response = college_data["fee"]

    # Exam Questions
    elif (
        "exam" in question or
        "internal" in question or
        "semester" in question or
        "practical" in question
    ):
        response = college_data["exam"]

    # Attendance Questions
    elif (
        "attendance" in question or
        "percentage" in question or
        "75%" in question
    ):
        response = college_data["attendance"]

    # Assignment Questions
    elif (
        "assignment" in question or
        "project" in question or
        "submission" in question or
        "deadline" in question
    ):
        response = college_data["assignment"]

    # Scholarship Questions
    elif (
        "scholarship" in question or
        "financial aid" in question or
        "merit scholarship" in question
    ):
        response = college_data["scholarship"]

    # Placement Questions
    elif (
        "placement" in question or
        "company" in question or
        "job" in question or
        "package" in question
    ):
        response = college_data["placement"]

    # Timetable Questions
    elif (
        "timetable" in question or
        "class schedule" in question or
        "classes" in question
    ):
        response = college_data["timetable"]

    # Greetings
    elif (
        "hello" in question or
        "hi" in question or
        "hey" in question
    ):
        response = """
👋 Hello!

I can help you with:
• Admissions
• Fees
• Exams
• Attendance
• Assignments
• Scholarships
• Placements
• Timetable
"""

    # Default Response
    else:
        response = """
❌ Sorry!

I can answer only college-related questions such as:
• Admission
• Fees
• Exams
• Attendance
• Assignments
• Scholarships
• Placements
• Timetable
"""

    st.success(response)

# ---------------- FOOTER ----------------

st.write("")
st.write("")

st.markdown("""
<div style="
background:#1e3c72;
color:white;
padding:15px;
text-align:center;
border-radius:10px;
">
© 2026 AI Chatbot for College Administration
</div>
""", unsafe_allow_html=True)