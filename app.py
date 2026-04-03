# Chatbot - Student Support System
# Nigerian Navy Institute of Technology
# Features:
#   Dynamic exam schedule (auto yearly update)
#   Weekday-only exam listing
#    Countdown to exam start

import datetime   #set dates 
import streamlit as st
import joblib

# Load trained ML model and vectorizer
model = joblib.load("chatbot_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# Generate Exam Schedule
def get_exam_details(month, start_week):  # Generates weekday-only exam schedule (Mon–Fri only) and countdown.  
    # Get current year
    year = datetime.datetime.now().year
    first_day = datetime.date(year, month, 1)   # First day of the month
    first_monday = first_day + datetime.timedelta(days=(7 - first_day.weekday()) % 7)  # Find first Monday
    start_date = first_monday + datetime.timedelta(weeks=start_week - 1)  # Move to desired week

# Get only weekdays (10 days = 2 weeks)
    exam_days = []
    current_day = start_date
    while len(exam_days) < 10:
        if current_day.weekday() < 5:  # Monday–Friday
            exam_days.append(current_day)
        current_day += datetime.timedelta(days=1)
    first_exam_day = exam_days[0]
    last_exam_day = exam_days[-1]
    today = datetime.date.today()    # Countdown
    days_to_start = (first_exam_day - today).days

    if days_to_start > 0:
        countdown = f"Exam starts in {days_to_start} days"
    elif days_to_start == 0:
        countdown = "Exam starts today!"
    else:
        countdown = "Exam already started or completed"

    schedule = "\n".join(     # Format schedule
        [day.strftime("%A, %d %B %Y") for day in exam_days]
    )
    return schedule, first_exam_day, last_exam_day, countdown

# GENERATE EXAM DATA
first_sched, f_start, f_end, f_count = get_exam_details(3, 1)   # March (Week 1–2)
second_sched, s_start, s_end, s_count = get_exam_details(8, 3) # August (Week 3–4)

# CHATBOT RESPONSES
responses = {
    "1st Semester exam": f""" First Semester Exam Schedule:
{f_start.strftime('%d %B %Y')} to {f_end.strftime('%d %B %Y')}
{f_count}
Exam Days (Weekdays only):
{first_sched}
Daily start time: 9:00 AM""",
    "2nd Semester exam": f""" Second Semester Exam Schedule:
{s_start.strftime('%d %B %Y')} to {s_end.strftime('%d %B %Y')}
{s_count}
Exam Days (Weekdays only):
{second_sched}
Daily start time: 9:00 AM""",
    "assignment and project": """ Assignment and Project Deadlines:
- Assignment due: May 25, 2026
- Project due: June 12, 2026""",
    "library": """ Library Hours:
- Weekdays: 8:00 AM – 6:00 PM
- Weekends: 10:00 AM – 4:00 PM""",
    "tutoring": """ Tutoring:
- Free for students
- Subjects: Math, Physics, CS
- Next session: May 20, 2026""",
    "registration": """ Registration:
- Starts: June 1, 2026
- Ends: June 15, 2026
- Add/Drop: June 2 – June 6, 2026""",
    "counseling": """ Counseling:
- Hours: 8:00 AM – 4:00 PM
- Days: Mon–Fri
- Location: Student Affairs Building""",
    "attendance_policy": """ Attendance Policy:
- Minimum: 75%
- Unexcused absence affects grade""",
    "late_submission_policy": """ Late Submission:
- 5% deduction per day
- Extensions require approval""",
    "registrar_contact": """ Registrar Contact:
- Email: registrar@university.edu
- Phone: +234 800 123 4567""",
    "support_contact": """ Student Support:
- Email: support@university.edu
- Office hours: 8:00 AM – 4:00 PM"""
}
# STREAMLIT UI
st.title("📚 Nigerian Navy Institute of Technology: Student Support System")
st.write("Ask about exams, assignments, library, registration, etc.")
user_input = st.text_input("Type your question here:")

if user_input:
    text = user_input.lower()
    if "exam" in text:
        if any(word in text for word in ["2nd", "second", "sem 2", "semester 2"]):
            intent = "2nd Semester exam"
        elif any(word in text for word in ["1st", "first", "sem 1", "semester 1"]):
            intent = "1st Semester exam"
        else:
            # If user just says "exam", default to upcoming one
            intent = "1st Semester exam"
    else:
        # fallback to ML model
        input_vec = vectorizer.transform([text])
        intent = model.predict(input_vec)[0]
    answer = responses.get(intent, "Sorry, I don't have an answer for that yet.")
    st.write(f"**Bot:** {answer}")
