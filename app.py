import re
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# -------------------------------
# SMART SUMMARIZER (NO API)
# -------------------------------
def smart_summarize(text):
    summary = {
        "Academic Prerequisites": [],
        "Test Scores": [],
        "Application Materials": [],
        "Important Deadlines": [],
        "Key Points": []
    }

    text_lower = text.lower()

    # Percentage / GPA
    percent = re.findall(r'\d+%', text)
    if percent:
        summary["Academic Prerequisites"].append(f"Minimum Marks Required: {percent[0]}")

    # Exams
    exams = ["jee", "sat", "act", "gre", "toefl", "ielts"]
    for exam in exams:
        if exam in text_lower:
            summary["Test Scores"].append(exam.upper())

    # Documents
    if "recommendation" in text_lower:
        summary["Application Materials"].append("Recommendation Letters")
    if "statement of purpose" in text_lower:
        summary["Application Materials"].append("Statement of Purpose")
    if "transcript" in text_lower:
        summary["Application Materials"].append("Transcripts")
    if "essay" in text_lower:
        summary["Application Materials"].append("Essays")

    # Deadline
    months = ["january","february","march","april","may","june",
              "july","august","september","october","november","december"]
    for month in months:
        if month in text_lower:
            summary["Important Deadlines"].append(month.capitalize())

    # Fees
    fee = re.findall(r'₹\d+|\d+\s?rupees', text, re.IGNORECASE)
    if fee:
        summary["Key Points"].append(f"Application Fee: {fee[0]}")

    return summary


# -------------------------------
# SMART CHECKLIST GENERATOR
# -------------------------------
def generate_checklist(school, program, requirements):
    checklist = []

    checklist.append({
        "category": "General",
        "item": f"Complete application form for {school}",
        "priority": "high"
    })

    if program:
        checklist.append({
            "category": "General",
            "item": f"Apply for {program} program",
            "priority": "high"
        })

    if "recommendation" in requirements.lower():
        checklist.append({
            "category": "Recommendations",
            "item": "Request recommendation letters",
            "priority": "high"
        })

    if "transcript" in requirements.lower():
        checklist.append({
            "category": "Academic Documents",
            "item": "Submit official transcripts",
            "priority": "high"
        })

    if "jee" in requirements.lower():
        checklist.append({
            "category": "Test Scores",
            "item": "Submit JEE scorecard",
            "priority": "medium"
        })

    checklist.append({
        "category": "Financial",
        "item": "Pay application fee",
        "priority": "high"
    })

    return checklist


# -------------------------------
# ROUTES
# -------------------------------

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/summarize')
def summarize_page():
    return render_template('summarizer.html')


@app.route('/checklist')
def checklist_page():
    return render_template('checklist.html')


@app.route('/api/summarize', methods=['POST'])
def api_summarize():
    data = request.get_json()
    requirements_text = data.get('requirements', '')

    if not requirements_text.strip():
        return jsonify({'error': 'Please provide requirements text'}), 400

    summary = smart_summarize(requirements_text)
    return jsonify({'summary': summary})


@app.route('/api/generate-checklist', methods=['POST'])
def api_generate_checklist():
    data = request.get_json()
    school_name = data.get('school', '')
    program_name = data.get('program', '')
    additional_requirements = data.get('requirements', '')

    if not school_name.strip():
        return jsonify({'error': 'Please provide a school name'}), 400
    checklist = generate_checklist(school_name, program_name, additional_requirements)
    return jsonify({'checklist': checklist})


# -------------------------------
# RUN
# -------------------------------
if __name__ == '__main__':
    app.run(debug=True)