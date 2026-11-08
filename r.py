import streamlit as st
import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Student Performance AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background-color: #f5f7fb;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #111827;
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }

    /* Main title */
    .main-title {
        font-size: 38px;
        font-weight: 700;
        color: #111827;
        margin-bottom: 5px;
    }

    .subtitle {
        color: #6b7280;
        font-size: 17px;
        margin-bottom: 25px;
    }

    /* Cards */
    .card {
        background-color: white;
        padding: 22px;
        border-radius: 15px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        margin-bottom: 18px;
    }

    .card-title {
        font-size: 18px;
        font-weight: 600;
        color: #111827;
        margin-bottom: 8px;
    }

    .card-text {
        color: #6b7280;
        font-size: 14px;
    }

    /* Result */
    .result-box {
        background-color: white;
        padding: 28px;
        border-radius: 18px;
        border: 1px solid #e5e7eb;
        text-align: center;
        margin-top: 20px;
    }

    .result-mark {
        font-size: 48px;
        font-weight: 700;
        color: #2563eb;
    }

    .result-grade {
        font-size: 30px;
        font-weight: 600;
        color: #111827;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #6b7280;
        padding: 25px;
        font-size: 13px;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# CREATE SYNTHETIC DATASET
# ============================================================

@st.cache_data
def create_dataset():

    np.random.seed(42)

    n = 1200

    attendance = np.random.randint(50, 101, n)

    study_hours = np.random.uniform(1, 10, n)

    assignment_score = np.random.uniform(40, 100, n)

    internal_marks = np.random.uniform(30, 100, n)

    previous_marks = np.random.uniform(30, 100, n)

    participation = np.random.randint(1, 11, n)

    final_marks = (
        attendance * 0.20
        + study_hours * 2.5
        + assignment_score * 0.20
        + internal_marks * 0.25
        + previous_marks * 0.15
        + participation * 0.5
        + np.random.normal(0, 3, n)
    )

    final_marks = np.clip(
        final_marks,
        0,
        100
    )

    return pd.DataFrame({
        "Attendance": attendance,
        "Study Hours": study_hours,
        "Assignment Score": assignment_score,
        "Internal Marks": internal_marks,
        "Previous Marks": previous_marks,
        "Participation": participation,
        "Final Marks": final_marks
    })


# ============================================================
# TRAIN MODEL
# ============================================================

data = create_dataset()

features = [
    "Attendance",
    "Study Hours",
    "Assignment Score",
    "Internal Marks",
    "Previous Marks",
    "Participation"
]

X = data[features]

y = data["Final Marks"]


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)


model = RandomForestRegressor(
    n_estimators=150,
    max_depth=10,
    random_state=42
)


model.fit(
    X_train,
    y_train
)


test_predictions = model.predict(X_test)


mae = mean_absolute_error(
    y_test,
    test_predictions
)


r2 = r2_score(
    y_test,
    test_predictions
)


accuracy = max(
    0,
    min(
        100,
        r2 * 100
    )
)


# ============================================================
# SESSION STATE
# ============================================================

if "history" not in st.session_state:

    st.session_state.history = []


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "## 🎓 Student AI"
    )

    st.caption(
        "Performance Prediction System"
    )

    st.markdown("---")

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "🔮 Prediction",
            "📊 Analytics",
            "ℹ️ About"
        ]
    )

    st.markdown("---")

    st.info(
        "AI-powered academic performance "
        "prediction for educational use."
    )


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.markdown(
        '<div class="main-title">'
        '🎓 Student Performance Prediction'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'AI-powered system for predicting student academic performance'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Students Analysed",
            "1,200"
        )


    with col2:

        st.metric(
            "Model Accuracy",
            f"{accuracy:.1f}%"
        )


    with col3:

        st.metric(
            "MAE",
            f"{mae:.2f}"
        )


    with col4:

        st.metric(
            "Features",
            "6"
        )


    st.markdown("---")


    # --------------------------------------------------------
    # PROJECT CARDS
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)


    with col1:

        st.markdown("""
        <div class="card">

        <div class="card-title">
        🤖 Machine Learning
        </div>

        <div class="card-text">
        Random Forest Regression is used to
        estimate the student's expected final marks.
        </div>

        </div>
        """, unsafe_allow_html=True)


    with col2:

        st.markdown("""
        <div class="card">

        <div class="card-title">
        📈 Performance Analysis
        </div>

        <div class="card-text">
        Analyse attendance, study hours,
        internal marks and other academic factors.
        </div>

        </div>
        """, unsafe_allow_html=True)


    with col3:

        st.markdown("""
        <div class="card">

        <div class="card-title">
        🔮 Prediction
        </div>

        <div class="card-text">
        Enter student details and receive
        an estimated final score and grade.
        </div>

        </div>
        """, unsafe_allow_html=True)


    st.markdown("---")


    # --------------------------------------------------------
    # MODEL WORKFLOW
    # --------------------------------------------------------

    st.subheader(
        "🔄 Machine Learning Workflow"
    )


    st.write(
        "Student Data → Preprocessing → "
        "Random Forest → Prediction → Performance Analysis"
    )


    st.progress(
        100
    )


    st.markdown("---")


    st.subheader(
        "📌 Prediction Factors"
    )


    factor_data = pd.DataFrame({
        "Factor": features,
        "Importance": model.feature_importances_
    })


    factor_data = factor_data.sort_values(
        "Importance",
        ascending=False
    )


    st.bar_chart(
        factor_data.set_index("Factor")
    )


# ============================================================
# PREDICTION
# ============================================================

elif page == "🔮 Prediction":

    st.markdown(
        '<div class="main-title">'
        '🔮 Student Performance Prediction'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Enter the student information below'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # STUDENT PROFILE
    # --------------------------------------------------------

    st.subheader(
        "👨‍🎓 Student Profile"
    )


    col1, col2 = st.columns(2)


    with col1:

        student_name = st.text_input(
            "Student Name",
            placeholder="Enter student name"
        )


    with col2:

        student_id = st.text_input(
            "Student ID",
            placeholder="Enter student ID"
        )


    st.markdown("---")


    # --------------------------------------------------------
    # ACADEMIC DETAILS
    # --------------------------------------------------------

    st.subheader(
        "📚 Academic Details"
    )


    col1, col2 = st.columns(2)


    with col1:

        attendance = st.slider(
            "Attendance (%)",
            min_value=50,
            max_value=100,
            value=75
        )


        study_hours = st.slider(
            "Study Hours per Day",
            min_value=1.0,
            max_value=10.0,
            value=5.0,
            step=0.5
        )


        assignment_score = st.slider(
            "Assignment Score (%)",
            min_value=40,
            max_value=100,
            value=70
        )


    with col2:

        internal_marks = st.slider(
            "Internal Marks (%)",
            min_value=30,
            max_value=100,
            value=65
        )


        previous_marks = st.slider(
            "Previous Exam Marks (%)",
            min_value=30,
            max_value=100,
            value=65
        )


        participation = st.slider(
            "Class Participation",
            min_value=1,
            max_value=10,
            value=6
        )


    st.markdown("---")


    # --------------------------------------------------------
    # PREDICT
    # --------------------------------------------------------

    if st.button(
        "🚀 Predict Performance",
        type="primary",
        use_container_width=True
    ):


        input_data = pd.DataFrame({

            "Attendance": [attendance],

            "Study Hours": [study_hours],

            "Assignment Score": [assignment_score],

            "Internal Marks": [internal_marks],

            "Previous Marks": [previous_marks],

            "Participation": [participation]

        })


        prediction = model.predict(
            input_data
        )[0]


        prediction = max(
            0,
            min(
                100,
                prediction
            )
        )


        # ----------------------------------------------------
        # GRADE
        # ----------------------------------------------------

        if prediction >= 90:

            grade = "A+"
            performance = "Excellent"
            status = "Outstanding performance!"

        elif prediction >= 80:

            grade = "A"
            performance = "Very Good"
            status = "Very good performance!"

        elif prediction >= 70:

            grade = "B"
            performance = "Good"
            status = "Good performance!"

        elif prediction >= 60:

            grade = "C"
            performance = "Average"
            status = "Average performance."

        elif prediction >= 50:

            grade = "D"
            performance = "Needs Improvement"
            status = "Performance needs improvement."

        else:

            grade = "F"
            performance = "Poor"
            status = "Additional academic support may be needed."


        # ----------------------------------------------------
        # SAVE HISTORY
        # ----------------------------------------------------

        st.session_state.history.append({

            "Student": student_name
            if student_name
            else "Unknown",

            "Student ID": student_id
            if student_id
            else "-",

            "Predicted Marks": round(
                prediction,
                2
            ),

            "Grade": grade,

            "Performance": performance

        })


        # ----------------------------------------------------
        # RESULT
        # ----------------------------------------------------

        st.markdown(
            '<div class="result-box">',
            unsafe_allow_html=True
        )


        st.write(
            "### Prediction Result"
        )


        st.markdown(
            f'<div class="result-mark">'
            f'{prediction:.2f}/100'
            f'</div>',
            unsafe_allow_html=True
        )


        st.markdown(
            f'<div class="result-grade">'
            f'Grade {grade}'
            f'</div>',
            unsafe_allow_html=True
        )


        st.write(
            performance
        )


        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


        if prediction >= 70:

            st.success(
                f"✅ {status}"
            )

        elif prediction >= 50:

            st.warning(
                f"⚠️ {status}"
            )

        else:

            st.error(
                f"❗ {status}"
            )


        st.progress(
            int(prediction)
        )


        # ----------------------------------------------------
        # STUDENT SUMMARY
        # ----------------------------------------------------

        st.markdown("---")

        st.subheader(
            "📋 Student Summary"
        )


        summary = pd.DataFrame({

            "Parameter": [

                "Student Name",

                "Student ID",

                "Attendance",

                "Study Hours",

                "Assignment Score",

                "Internal Marks",

                "Previous Marks",

                "Participation"

            ],

            "Value": [

                student_name
                if student_name
                else "Not provided",

                student_id
                if student_id
                else "Not provided",

                f"{attendance}%",

                f"{study_hours} hours/day",

                f"{assignment_score}%",

                f"{internal_marks}%",

                f"{previous_marks}%",

                f"{participation}/10"

            ]

        })


        st.dataframe(
            summary,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# ANALYTICS
# ============================================================

elif page == "📊 Analytics":

    st.markdown(
        '<div class="main-title">'
        '📊 Academic Analytics'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Model insights and prediction history'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # FEATURE IMPORTANCE
    # --------------------------------------------------------

    st.subheader(
        "🔍 Important Performance Factors"
    )


    importance = pd.DataFrame({

        "Factor": features,

        "Importance": model.feature_importances_

    })


    importance = importance.sort_values(
        "Importance",
        ascending=False
    )


    st.bar_chart(
        importance.set_index("Factor")
    )


    st.markdown("---")


    # --------------------------------------------------------
    # DATASET PREVIEW
    # --------------------------------------------------------

    st.subheader(
        "📁 Dataset Preview"
    )


    st.dataframe(
        data.head(15),
        use_container_width=True,
        hide_index=True
    )


    st.markdown("---")


    # --------------------------------------------------------
    # HISTORY
    # --------------------------------------------------------

    st.subheader(
        "🕒 Prediction History"
    )


    if len(st.session_state.history) == 0:

        st.info(
            "No predictions have been made yet."
        )

    else:

        history_df = pd.DataFrame(
            st.session_state.history
        )


        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# ABOUT
# ============================================================

else:

    st.markdown(
        '<div class="main-title">'
        'ℹ️ About the Project'
        '</div>',
        unsafe_allow_html=True
    )


    st.markdown("""
    ### 🎓 Student Performance Prediction System

    This project demonstrates how Machine Learning
    can be used to estimate student academic performance.

    ### 🎯 Objective

    The main objective is to predict expected final
    marks based on academic and behavioural factors.

    ### 🤖 Machine Learning Algorithm

    **Random Forest Regression**

    Random Forest combines multiple decision trees
    to produce a more reliable prediction.

    ### 📥 Input Parameters

    - Attendance
    - Study hours
    - Assignment score
    - Internal marks
    - Previous examination marks
    - Class participation

    ### 📤 Output

    - Predicted final marks
    - Grade
    - Performance level
    - Performance analysis

    ### 🛠 Technologies

    - Python
    - Streamlit
    - Pandas
    - NumPy
    - Scikit-learn

    ### 🔄 System Workflow

    Student Information
    ↓
    Data Processing
    ↓
    Machine Learning Model
    ↓
    Performance Prediction
    ↓
    Grade Classification
    """)


    st.warning(
        "This application is an academic demonstration "
        "and should not be used as the sole basis for "
        "academic decisions."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
    🎓 Student Performance Prediction System
    <br>
    AI/ML Academic Project
    </div>
    """,
    unsafe_allow_html=True
)