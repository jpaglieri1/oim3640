import os
from openai import OpenAI
from dotenv import load_dotenv
from docx import Document
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_file(filepath):
    """Extract text from various file formats"""
    try:
        if filepath.endswith('.docx'):
            doc = Document(filepath)
            return "\n".join([para.text for para in doc.paragraphs])
        elif filepath.endswith('.pdf'):
            if pdfplumber is None:
                raise ImportError("PDF support requires 'pdfplumber'. Install it with: pip install pdfplumber")
            with pdfplumber.open(filepath) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() or ""
                    text += "\n"
                return text.strip()
        else:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
    except Exception as e:
        raise Exception(f"Error reading file: {str(e)}")

def score_resume_match(resume, job_description):
    """
    Use OpenAI API to score how well a resume matches a job description.
    Returns a score (0-100) and detailed breakdown.
    """
    try:
        prompt = f"""You are an expert recruiter. Analyze how well this resume matches the job description.

JOB DESCRIPTION:
{job_description}

RESUME:
{resume}

Provide your analysis in the following format:
SCORE: [0-100]
SUMMARY: [1-2 sentence summary]
STRENGTHS: [List top 3 matching areas]
GAPS: [List top 3 gaps or missing skills]
RECOMMENDATION: [Brief hiring recommendation]"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert recruiter scoring resume matches."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        result = response.choices[0].message.content
        return result
    
    except Exception as e:
        return f"Error calling OpenAI API: {str(e)}"

@app.route('/')
def index():
    """Main page with upload form"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Handle file upload and analysis"""
    try:
        # Check if files are present
        if 'resume' not in request.files or 'job_description' not in request.files:
            return jsonify({'error': 'Both resume and job description files are required'}), 400
        
        resume_file = request.files['resume']
        jobdesc_file = request.files['job_description']
        
        # Check if files were selected
        if resume_file.filename == '' or jobdesc_file.filename == '':
            return jsonify({'error': 'Please select both files'}), 400
        
        # Validate file types
        if not allowed_file(resume_file.filename) or not allowed_file(jobdesc_file.filename):
            return jsonify({'error': 'Only .txt, .pdf, and .docx files are allowed'}), 400
        
        # Save uploaded files temporarily
        resume_filename = secure_filename(resume_file.filename)
        jobdesc_filename = secure_filename(jobdesc_file.filename)
        
        resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_filename)
        jobdesc_path = os.path.join(app.config['UPLOAD_FOLDER'], jobdesc_filename)
        
        resume_file.save(resume_path)
        jobdesc_file.save(jobdesc_path)
        
        # Extract text from files
        resume_text = extract_text_from_file(resume_path)
        jobdesc_text = extract_text_from_file(jobdesc_path)
        
        # Score the match
        result = score_resume_match(resume_text, jobdesc_text)
        
        # Clean up temporary files
        os.remove(resume_path)
        os.remove(jobdesc_path)
        
        return jsonify({'result': result}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)