# Study Game - Flask Web Interface

A modern, interactive study game built with Flask where students answer questions to guess letters in a password. Questions and passwords are dynamically generated from study materials using OpenAI's API.

## Features

✨ **AI-Powered Content Generation**
- Automatically generates study questions from uploaded materials
- Uses OpenAI to select key concepts for the password

🎮 **Interactive Gameplay**
- Answer trivia questions to earn letter guesses
- Guess letters to reveal the password word-by-word
- Real-time feedback on answers and guesses

📚 **Material Support**
- Upload DOCX and TXT files
- Or paste text directly
- Supports multiple materials per game

🤖 **Intelligent Answer Evaluation**
- Uses OpenAI to evaluate answers flexibly
- Accepts spelling variations and alternative phrasings
- Fair grading for open-ended questions

## Installation

### Requirements
- Python 3.8+
- OpenAI API key

### Setup

1. **Install Dependencies**
```bash
pip install flask python-docx openai python-dotenv
```

2. **Set Up Environment Variables**
Create a `.env` file in the project directory:
```
OPENAI_API_KEY=your_api_key_here
FLASK_ENV=development
FLASK_DEBUG=True
```

3. **Run the Application**
```bash
python app.py
```

4. **Access the Game**
Open your browser and navigate to:
```
http://localhost:5000
```

## How to Play

1. **Add Study Materials**
   - Upload a DOCX or TXT file with study content
   - Or paste text directly
   - Can add multiple materials before starting

2. **Start the Game**
   - Click "Start Game" to begin
   - The system generates 5 questions from your materials

3. **Answer Questions**
   - Read each question carefully
   - Type your answer and click Submit
   - OpenAI evaluates if your answer is correct

4. **Guess Letters**
   - For each correct answer, guess one letter
   - The password reveals as letters are guessed
   - See your progress at the top

5. **Win Condition**
   - Reveal the entire password to win
   - See how many questions you answered correctly

## Project Structure

```
ElectiveProject/
├── app.py                 # Flask application & routes
├── templates/
│   ├── base.html         # Base template with styling
│   ├── index.html        # Home page (materials upload)
│   └── game.html         # Game page (Q&A and gameplay)
├── uploads/              # Uploaded files storage
└── .env                  # Environment variables
```

## Key Functions

### Backend (app.py)
- `generate_questions_with_openai()` - Creates questions from materials
- `generate_password_with_openai()` - Selects key term for password
- `check_answer_with_openai()` - Evaluates student answers
- `display_password()` - Shows password with revealed letters

### Frontend (Flask Routes)
- `GET /` - Home page
- `GET /game` - Game page
- `POST /upload` - Handle file/text upload
- `POST /start-game` - Initialize new game
- `GET /get-question` - Fetch current question
- `POST /submit-answer` - Evaluate answer
- `POST /guess-letter` - Process letter guess
- `POST /new-game` - Reset game
- `POST /clear-materials` - Clear materials

## Styling

The application features:
- Modern gradient purple theme
- Responsive design (mobile-friendly)
- Smooth animations and transitions
- Clear visual hierarchy
- Accessible form inputs

## Environment Variables

```env
OPENAI_API_KEY=sk-...              # Your OpenAI API key
FLASK_ENV=development              # Set to 'production' for deployment
FLASK_DEBUG=True                   # Enable debug mode
```

## Troubleshooting

**"No materials provided" error**
- Make sure you've added at least one study material before clicking "Start Game"

**"Could not parse OpenAI response" error**
- The API response format may have changed
- Check that your OpenAI API key is valid

**Questions seem repetitive**
- The game generates new questions after 5 are answered
- Refresh the page or start a new game

## API Usage Notes

- Each game session makes multiple API calls to OpenAI
- Questions are regenerated in batches to provide fresh content
- Answer evaluation uses lenient matching with temperature=0.3

## License

Educational project for learning purposes.
