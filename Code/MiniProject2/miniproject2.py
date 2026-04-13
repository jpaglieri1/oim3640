import os
from openai import OpenAI
from dotenv import load_dotenv
from docx import Document

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def resupload():
    """Read resume from file"""
    resume = Document(input("Input directory to resume: "))

def jobdesc():
    """Read job description from file"""
    description = Document(input("Input directory to job description: "))

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

def main():
    """Main function to run the resume scoring tool"""
    print("=== Resume to Job Description Scorer ===\n")
    
    try:
        # Get resume and job description
        resume = resupload()
        job_description = jobdesc()
        
        # Score the match
        print("\nAnalyzing resume match... Please wait.\n")
        score_result = score_resume_match(resume, job_description)
        
        # Display results
        print("=== ANALYSIS RESULTS ===\n")
        print(score_result)
        
    except FileNotFoundError as e:
        print(f"Error: File not found. {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()