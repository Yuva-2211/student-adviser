
import streamlit as st
import pandas as pd
import joblib


@st.cache_data
def load_model():
    return joblib.load("/content/pipeline.pkl")

model = load_model()


def generate_recommendations(student_data, predicted_score):
    suggestions = []

  
    if student_data['study_hours_per_day'] < 2:
        suggestions.append("Increase study time to at least 2 hours daily with Pomodoro technique.")
    if student_data['sleep_hours'] < 7:
        suggestions.append("Improve sleep to 7-8 hours by setting a fixed bedtime.")
    if student_data['social_media_hours'] > 2:
        suggestions.append("Limit social media to 1.5 hours daily using app blockers.")
    if student_data['netflix_hours'] > 2:
        suggestions.append("Cut down Netflix time to 1 hour and take regular study breaks.")
    if student_data['diet_quality'] == 'Poor':
        suggestions.append("Add a nutritious breakfast and include fruits daily.")
    if student_data['exercise_frequency'] < 2:
        suggestions.append("Try to exercise at least 3 times a week for better focus.")
    if student_data['attendance_percentage'] < 80:
        suggestions.append("Improve attendance to 90%+ by regular class participation.")
    if student_data['mental_health_rating'] < 5:
        suggestions.append("Practice journaling and consider weekly mentor check-ins.")

    
    if predicted_score < 50:
        suggestions.insert(0, f" Predicted exam score is low ({predicted_score:.1f}). Immediate action recommended.")
    elif predicted_score < 75:
        suggestions.insert(0, f" Predicted exam score is moderate ({predicted_score:.1f}). There is room for improvement.")
    elif predicted_score < 90:
        suggestions.insert(0, f" Predicted exam score is good ({predicted_score:.1f}). You can still optimize some areas.")
    else:
        suggestions.insert(0, f" Excellent predicted score ({predicted_score:.1f})! Keep doing what's working.")

    
    if predicted_score >= 90:
        return suggestions[:6] 
    return suggestions


# Streamlit UI
st.set_page_config(page_title="Exam Score Predictor", layout="centered")
st.title("🎓 Personalized Exam Score Predictor & Roadmap")
st.markdown("Enter your daily habits and lifestyle data to estimate your exam score and get custom recommendations.")

# Input fields
age = st.number_input("Age", min_value=1, max_value=100)
study_hours_per_day = st.slider("Study Hours per Day", 0, 24, 8)
social_media_hours = st.slider("Social Media Hours per Day", 0, 24, 6)
netflix_hours = st.slider("Netflix Hours per Day", 0, 24, 4)
attendance_percentage = st.slider("Attendance Percentage", 0, 100, 90, 1)
sleep_hours = st.slider("Sleep Hours per Day", 0.0, 12.0, 7.0, 0.1)
exercise_frequency = st.slider("Exercise Frequency (times per week)", 0, 7, 3)
mental_health_rating = st.slider("Mental Health Rating (1-10)", 1, 10, 7)
gender = st.selectbox("Gender", ['Female', 'Male', 'Other'])
part_time_job = st.selectbox("Part-time Job?", ['No', 'Yes'])
diet_quality = st.selectbox("Diet Quality", ['Fair', 'Good', 'Poor'])
parental_education_level = st.selectbox("Parental Education Level", ['Master', 'High School', 'Bachelor', 'Unknown'])
internet_quality = st.selectbox("Internet Quality", ['Average', 'Poor', 'Good'])
extracurricular_participation = st.selectbox("Extracurricular Participation?", ['No', 'Yes'])

# Prediction trigger
if st.button(" Predict Exam Score & Get Recommendations"):

    # Create input DataFrame
    input_df = pd.DataFrame({
        'age': [age],
        'study_hours_per_day': [study_hours_per_day],
        'social_media_hours': [social_media_hours],
        'netflix_hours': [netflix_hours],
        'attendance_percentage': [attendance_percentage],
        'sleep_hours': [sleep_hours],
        'exercise_frequency': [exercise_frequency],
        'mental_health_rating': [mental_health_rating],
        'gender': [gender],
        'part_time_job': [part_time_job],
        'diet_quality': [diet_quality],
        'parental_education_level': [parental_education_level],
        'internet_quality': [internet_quality],
        'extracurricular_participation': [extracurricular_participation],
    })

    
    pred_score = model.predict(input_df)[0]
    pred_score = min(pred_score, 100)

    # Graphical feedback - progress bar
    st.subheader("Predicted Exam Score")
    st.progress(int(pred_score))  # visual progress bar
    st.success(f"Your predicted exam score is **{pred_score:.1f}** out of 100")

    # Display recommendations
    recs = generate_recommendations(input_df.iloc[0], pred_score)
    st.markdown("### 💡 Personalized Recommendations")
    for rec in recs:
        st.write(f"- {rec}")
