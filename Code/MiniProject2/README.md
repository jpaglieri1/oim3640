# Resume to Job Description Scorer - Web Application

## Overview
A professional Flask web application that uses OpenAI's GPT-3.5 to analyze resume matches against job descriptions. The app provides AI-powered scoring and detailed feedback.

## Features
✨ **Modern, Responsive UI** - Drag-and-drop file uploads
🤖 **AI-Powered Analysis** - Uses OpenAI GPT-3.5 for intelligent matching
📄 **Multiple File Formats** - Supports .txt, .pdf, and .docx files
⚡ **Real-time Feedback** - Loading spinner and instant results
🎨 **Professional Design** - Beautiful gradient interface with smooth animations

## Requirements
- Python 3.8+
- Flask
- OpenAI API key
- python-docx (for .docx support)
- pdfplumber (for .pdf support)
- python-dotenv (for environment variables)

## Installation

1. **Install dependencies:**
   ```bash
   pip install flask openai python-docx pdfplumber python-dotenv werkzeug
   ```

2. **Set up environment variables:**
   Create a `.env` file in the MiniProject2 directory:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

3. **Run the application:**
   ```bash
   python miniproject2.py
   ```

4. **Access the web app:**
   Open your browser and go to: `http://localhost:5000`

## Usage

1. **Upload Resume** - Click or drag-and-drop your resume file
2. **Upload Job Description** - Click or drag-and-drop the job description file
3. **Click "Analyze Resume Match"** - Wait for AI analysis
4. **View Results** - See the matching score, strengths, gaps, and recommendations

## File Formats Supported
- **.pdf** - PDF documents (requires pdfplumber)
- **.docx** - Microsoft Word documents
- **.txt** - Plain text files

## Output Format
The AI provides:
- **SCORE** - 0-100 matching percentage
- **SUMMARY** - Brief analysis overview
- **STRENGTHS** - Top 3 matching areas
- **GAPS** - Top 3 missing skills
- **RECOMMENDATION** - Hiring recommendation

## Project Structure
```
MiniProject2/
├── miniproject2.py          # Main Flask app
├── templates/
│   └── index.html          # Web interface
├── uploads/                # Temporary file storage (auto-created)
├── .env                    # Environment variables (create this)
└── README_WEB_APP.md       # This file
```

## Notes
- Uploaded files are temporarily stored and automatically deleted after analysis
- Maximum file size: 16MB
- API calls may take 10-30 seconds depending on file size
- Keep your OpenAI API key secure in the `.env` file

## Troubleshooting

**Issue: "Unable to provide an analysis as both documents are not provided"**
- Ensure both files are properly uploaded and contain text
- Check that the files are valid .txt, .pdf, or .docx files

**Issue: OpenAI API errors**
- Verify your API key is correct in the `.env` file
- Check that you have sufficient API credits
- Ensure your API key has access to the gpt-3.5-turbo model

**Issue: File upload fails**
- Check file size (max 16MB)
- Verify file format is supported (.txt, .pdf, .docx)
- Ensure proper file permissions