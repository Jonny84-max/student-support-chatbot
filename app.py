# Chatbot - Student Support System
# Nigerian Navy Institute of Technology
# Features:
#   Dynamic exam schedule (auto yearly update)
#   Weekday-only exam listing
#    Countdown to exam start

import datetime
import streamlit as st
import joblib

# Load model and vectorizer
model = joblib.load("chatbot_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# Function to generate exam schedule
def get_exam_details(month, start_week):
    """
    Generates exam schedule for a semester.
    Returns:
        first_exam_day
        last_exam_day
        countdown string
        show_days (boolean)
        exam_days (list of weekdays)
    """
    year = datetime.datetime.now().year
    first_day = datetime.date(year, month, 1)
    first_monday = first_day + datetime.timedelta(days=(7 - first_day.weekday()) % 7)  # Find first Monday
    start_date = first_monday + datetime.timedelta(weeks=start_week - 1)       # Start date for requested week
    exam_days = []   # Generate only weekdays for 2 weeks (10 weekdays)
    current_day = start_date
    while len(exam_days) < 10:
        if current_day.weekday() < 5:  # Mon-Fri only
            exam_days.append(current_day)
        current_day += datetime.timedelta(days=1)
    first_exam_day = exam_days[0]
    last_exam_day = exam_days[-1]

    # Countdown and whether to show days
    today = datetime.date.today()
    days_to_start = (first_exam_day - today).days
    if days_to_start > 0:
        countdown = f"Exam starts in {days_to_start} days"
        show_days = days_to_start <= 7    # Show full exam days only if <7 days
    else:
        countdown = ""  # Neutral if exam started or passed
        show_days = False

    # Return all required info
    return first_exam_day, last_exam_day, countdown, show_days, exam_days

# Generate schedules
f_start, f_end, f_count, f_show_days, f_days = get_exam_details(3, 1)   # 1st sem: March, 1st week
s_start, s_end, s_count, s_show_days, s_days = get_exam_details(8, 3)   # 2nd sem: August, 3rd week

# Build responses
responses = {
    "1st Semester exam": f" First Semester Exam Schedule:\n {f_start.strftime('%d %B %Y')} – {f_end.strftime('%d %B %Y')}\n{f_count}\n{f_days}\n Daily start time: 9:00 AM",
    "2nd Semester exam": f" Second Semester Exam Schedule:\n {s_start.strftime('%d %B %Y')} – {s_end.strftime('%d %B %Y')}\n{s_count}\n{s_days}\n Daily start time: 9:00 AM",
    "assignment and project deadlines": " Assignment and Project Deadlines:\n- Assignment due: May 25, 2026\n- Project due: June 12, 2026",
    "library": " Library Hours:\n- Weekdays: 8:00 AM – 6:00 PM\n- Weekends: 10:00 AM – 4:00 PM",
    "tutoring": " Tutoring:\n- Tutoring is free.\n- Available subjects: Math, Physics, CS.\n- Next session: May 20, 2026",
    "registration": " Registration:\n- Starts: June 1, 2026\n- Ends: June 15, 2026\n- Add/drop: June 2 – June 6, 2026",
    "counseling": " Counseling:\n- Hours: 8:00 AM – 4:00 PM\n- Days: Mon–Fri\n- Location: Student Affairs Building",
    "attendance_policy": " Attendance Policy:\n- Minimum attendance: 75%\n- Missing class without excuse affects grade",
    "late_submission_policy": " Late Submission:\n- Late work loses 5% per day\n- Extensions require approval",
    "registrar_contact": " Registrar Contact:\n- Email: registrar@university.edu\n- Phone: +234 800 123 4567",
    "support_contact": " Student Support:\n- Email: support@university.edu\n- Office hours: 8:00 AM – 4:00 PM"
}

def format_exam_response(start, end, countdown, show_days, days):
    response = f"Exam Schedule:\n🗓 {start.strftime('%d %B %Y')} – {end.strftime('%d %B %Y')}\n{countdown}\nDaily start time: 9:00 AM"
    if show_days:
        day_list = "\n".join([day.strftime("%A, %d %B %Y") for day in days])
        response += f"\n\nExam Days (Weekdays only):\n{day_list}"
    return response

responses["1st Semester exam"] = format_exam_response(f_start, f_end, f_count, f_show_days, f_days)
responses["2nd Semester exam"] = format_exam_response(s_start, s_end, s_count, s_show_days, s_days)

# Streamlit interface
st.title("📚 Nigerian Navy Institute of Technology: Student Support Chatbot")
st.write("Ask about exams, assignments, library, registration, etc.")

user_input = st.text_input("Type your question here:")

if user_input:
    text = user_input.lower()
    # Simple keyword rule-based detection
    if "exam" in text:
        if any(word in text for word in ["2nd", "second", "sem 2", "semester 2"]):
            intent = "2nd Semester exam"
        elif any(word in text for word in ["1st", "first", "sem 1", "semester 1"]):
            intent = "1st Semester exam"
        else:
            # Default to upcoming semester
            intent = "1st Semester exam"
    else:
        input_vec = vectorizer.transform([text])
        intent = model.predict(input_vec)[0]

    answer = responses.get(intent, "Sorry, I don't have an answer for that yet.")
    st.write(f"**Bot:** {answer}")
