import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
#from transformers import BartTokenizer, BartForConditionalGeneration, Trainer, TrainingArguments


# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Sample JSON data
json_data = {
    "patient_name": "Mr. Abc",
    "referring_doctor": "Dr. Xyz",
    "compliant": "Slurred speech and Weakness",
    "diagnosis": "ACUTE ISCHEMIC STROKE",
    "sessions_done": [
        {
            "date": "15-Jul-24",
            "name": "Strength Training",
            "count": 2,
            "activities": [
                {"name": "Weight Cuff", "level": "Level 1"},
                {"name": "Swiss Ball", "level": "Level 1"},
                {"name": "Erogmeter", "level": "Level 1"}
            ]
        }
    ],
    "improvements": [
        {"date": "15-Jul-24", "improvement": "Foleys Catheter Removal"},
        {"date": "18-Jul-24", "improvement": "Sitting with support"},
        {"date": "21-Jul-24", "improvement": "Wheel chair mobilisation"}
    ],
    "milestones": "Tracstomy Tube Removed, Sitting without support",
    "vitals_admission": {
        "heart_rate": "70",
        "blood_pressure": "120/80",
        "temperature": "98.6",
        "respiratory_rate": 16
    },
    "vital_last_week": {
        "heart_rate": "80",
        "blood_pressure": "130/85",
        "temperature": "99.5",
        "respiratory_rate": 18
    },
    "vital_weekly": [
        {"date": "15-Jul-24", "heart_rate": "70", "blood_pressure": "120/80", "temperature": "98.6", "respiratory_rate": 16}
    ],
    "procedures_done": [
        {"date": "15-Jul-24", "name": "Wound Dressings"},
        {"date": "17-Jul-24", "name": "Tube Changing(NG,FC)"},
        {"date": "19-Jul-24", "name": "Nebulization"}
    ]
}

# Define the prompt for summarization
prompt = """You are a JSON data summarizer. You will be taking the JSON data and
summarizing it into a paragraph format the output in 10 lines. """

# Function to preprocess JSON data
def preprocess_json(json_data):
    """Preprocess JSON data into a formatted string for summarization."""
    patient_name = json_data.get('patient_name', 'Unknown')
    referring_doctor = json_data.get('referring_doctor', 'Unknown')
    complaint = json_data.get('compliant', 'Not specified')
    diagnosis = json_data.get('diagnosis', 'Not specified')

    # Treatment Sessions
    sessions = json_data.get('sessions_done', [])
    session_details = ""
    for session in sessions:
        date = session.get('date', 'Unknown date')
        name = session.get('name', 'Unknown')
        activities = session.get('activities', [])
        activities_str = ', '.join([f"{activity['name']} at {activity['level']}" for activity in activities])
        session_details += f"On {date}, {name} included activities such as {activities_str}. "

    # Key Improvements
    improvements = json_data.get('improvements', [])
    improvements_str = ', '.join([f"{imp['improvement']} on {imp['date']}" for imp in improvements])

    # Milestones
    milestones = json_data.get('milestones', 'Not specified')

    # Vitals
    vitals_admission = json_data.get('vitals_admission', {})
    recent_vitals = json_data.get('vital_last_week', {})
    vital_details = (
        f"Vital Signs on Admission: Heart Rate: {vitals_admission.get('heart_rate', 'N/A')}, "
        f"Blood Pressure: {vitals_admission.get('blood_pressure', 'N/A')}, "
        f"Temperature: {vitals_admission.get('temperature', 'N/A')}, "
        f"Respiratory Rate: {vitals_admission.get('respiratory_rate', 'N/A')}. "
        f"Recent Vital Signs: Heart Rate: {recent_vitals.get('heart_rate', 'N/A')}, "
        f"Blood Pressure: {recent_vitals.get('blood_pressure', 'N/A')}, "
        f"Temperature: {recent_vitals.get('temperature', 'N/A')}, "
        f"Respiratory Rate: {recent_vitals.get('respiratory_rate', 'N/A')}. "
    )

    # Procedures Done
    procedures = json_data.get('procedures_done', [])
    procedures_str = ', '.join([f"{proc['name']} on {proc['date']}" for proc in procedures])

    return (
        f"Patient Name: {patient_name}. Referring Doctor: {referring_doctor}. "
        f"Complaint: {complaint}. Diagnosis: {diagnosis}. "
        f"Treatment Sessions: {session_details} "
        f"Key Improvements: {improvements_str}. "
        f"Milestones Achieved: {milestones}. "
        f"{vital_details} "
        f"Procedures Done: {procedures_str}."
    )

# Function to generate summary using Google Gemini
def generate_gemini_content(json_data):
    """Generate summary of JSON data using Google Gemini."""
    formatted_text = preprocess_json(json_data)
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + formatted_text)
    return response.text

# Generate and print the summary
summary = generate_gemini_content(json_data)
print(summary)
