import streamlit as st
import joblib

# Load model and vectorizer
model = joblib.load("chatbot_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# Responses for each intent
responses = {
    "exam": "📌 Exam Schedule:\n- Exams start: June 1, 2026\n- Final exam: June 15, 2026\n- Exam time: 9:00 AM",
    "assignment": "📌 Assignment Deadlines:\n- Assignment due: May 25, 2026\n- Project due: June 12, 2026",
    "library": "📌 Library Hours:\n- Weekdays: 8:00 AM – 6:00 PM\n- Weekends: 10:00 AM – 4:00 PM",
    "tutoring": "📌 Tutoring:\n- Tutoring is free.\n- Available subjects: Math, Physics, CS.\n- Next session: May 20, 2026",
    "registration": "📌 Registration:\n- Starts: June 1, 2026\n- Ends: June 15, 2026\n- Add/drop: June 2 – June 6, 2026",
    "counseling": "📌 Counseling:\n- Hours: 8:00 AM – 4:00 PM\n- Days: Mon–Fri\n- Location: Student Affairs Building",
    "attendance_policy": "📌 Attendance Policy:\n- Minimum attendance: 75%\n- Missing class without excuse affects grade",
    "late_submission_policy": "📌 Late Submission:\n- Late work loses 5% per day\n- Extensions require approval",
    "registrar_contact": "📌 Registrar Contact:\n- Email: registrar@university.edu\n- Phone: +234 800 123 4567",
    "support_contact": "📌 Student Support:\n- Email: support@university.edu\n- Office hours: 8:00 AM – 4:00 PM"
}

st.title("📚 Student Support Chatbot")
st.write("Ask a question about exams, assignments, library, registration etc.")

user_input = st.text_input("Type your question here:")

if user_input:
    input_vec = vectorizer.transform([user_input])
    intent = model.predict(input_vec)[0]
    answer = responses.get(intent, "Sorry, I don't have an answer for that yet.")
    st.write(f"**Bot:** {answer}")
