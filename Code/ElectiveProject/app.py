import os
import json
import re
from docx import Document
from openai import OpenAI
from dotenv import load_dotenv
from flask import Flask, render_template, request, session, jsonify, redirect, url_for
from werkzeug.utils import secure_filename

load_dotenv()

app = Flask(__name__)
app.secret_key = 'study-game-secret-key-2024'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize OpenAI
API_Key = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ==================== Helper Functions ====================

def extract_text_from_file(filepath):
    """Extract text from various file formats"""
    try:
        if filepath.endswith('.docx'):
            doc = Document(filepath)
            return "\n".join([para.text for para in doc.paragraphs])
        elif filepath.endswith('.txt'):
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            raise ValueError(f"Unsupported file type: {filepath}")
    except Exception as e:
        raise Exception(f"Error reading file: {str(e)}")

def generate_questions_with_openai(material):
    """Generate study questions from material using OpenAI"""
    try:
        response = API_Key.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an educational assistant. Generate a list of study questions based on the provided material. Return a JSON array with objects containing 'question' and 'answer' fields. Keep answers short (1-3 words)."
                },
                {
                    "role": "user",
                    "content": f"Generate study questions from this material:\n\n{material}"
                }
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        response_text = response.choices[0].message.content
        
        try:
            questions_data = json.loads(response_text)
        except json.JSONDecodeError:
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if json_match:
                questions_data = json.loads(json_match.group())
            else:
                raise ValueError("Could not parse OpenAI response")
        
        questions = [(q["question"], q["answer"]) for q in questions_data]
        return questions
    except Exception as e:
        print(f"Error generating questions: {e}")
        return []

def generate_password_with_openai(material):
    """Generate a random password word NOT related to the material"""
    try:
        response = API_Key.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Generate ONE completely random English word that is 5-10 letters long. The word should NOT be related to study, learning, or any academic topic. Return ONLY that single word in UPPERCASE, nothing else. No explanation, no punctuation, just the word."
                },
                {
                    "role": "user",
                    "content": "Generate a random English word (5-10 letters) that is NOT academic related. Return ONLY the word in UPPERCASE."
                }
            ],
            temperature=1.0,
            max_tokens=20,
            top_p=0.95
        )
        
        password = response.choices[0].message.content.strip().upper()
        password = ''.join(c for c in password if c.isalpha())
        
        if not password or len(password) < 4:
            password = "RANDOM"
        
        return password
    except Exception as e:
        print(f"Error generating password: {e}")
        return "RANDOM"

def check_answer_with_openai(user_answer, question, correct_answer):
    """Use OpenAI to check if answer is correct"""
    try:
        response = API_Key.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an educational evaluator. Determine if a student's answer is correct or acceptable for a given question. Be lenient with spelling, capitalization, and minor variations. Return ONLY 'YES' if the answer is correct/acceptable, or 'NO' if it is incorrect. Nothing else."
                },
                {
                    "role": "user",
                    "content": f"Question: {question}\nCorrect Answer: {correct_answer}\nStudent's Answer: {user_answer}\n\nIs the student's answer correct or acceptable?"
                }
            ],
            temperature=0.3,
            max_tokens=10
        )
        
        result = response.choices[0].message.content.strip().upper()
        return "YES" in result
    except Exception as e:
        print(f"Error evaluating answer: {e}")
        user_clean = user_answer.strip().lower()
        correct_clean = correct_answer.strip().lower()
        return user_clean == correct_clean or (len(correct_clean) > 3 and user_clean in correct_clean)

def display_password(password, guessed_letters):
    """Display the password with guessed letters revealed"""
    display = ""
    for letter in password:
        if letter in guessed_letters:
            display += letter
        else:
            display += "_"
    return " ".join(display)

# ==================== Routes ====================

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/game')
def game():
    """Game page"""
    if 'game_state' not in session:
        return redirect(url_for('index'))
    return render_template('game.html')

@app.route('/get-materials', methods=['GET'])
def get_materials():
    """Get current materials info"""
    if 'materials' in session and session['materials']:
        total_chars = sum(len(m) for m in session['materials'])
        material_names = session.get('material_names', ['Pasted Text'] * len(session['materials']))
        return jsonify({
            'success': True,
            'count': len(session['materials']),
            'total_characters': total_chars,
            'material_names': material_names
        })
    return jsonify({
        'success': True,
        'count': 0,
        'total_characters': 0,
        'material_names': []
    })

@app.route('/upload', methods=['POST'])
def upload_material():
    """Handle material upload"""
    try:
        # Initialize materials list and names in session if not present
        if 'materials' not in session:
            session['materials'] = []
        if 'material_names' not in session:
            session['material_names'] = []
        
        text = None
        material_name = None
        
        # Handle file upload
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename and file.filename != '':
                filename = secure_filename(file.filename)
                if not filename:
                    return jsonify({'success': False, 'message': 'Invalid filename'})
                
                material_name = filename
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                try:
                    text = extract_text_from_file(filepath)
                    # Clean up the file after reading
                    if os.path.exists(filepath):
                        os.remove(filepath)
                except Exception as e:
                    print(f"Error reading file: {e}")
                    return jsonify({'success': False, 'message': f'Error reading file: {str(e)}'})
        
        # Handle text input
        elif 'text' in request.form:
            text = request.form.get('text', '').strip()
            if not text:
                return jsonify({'success': False, 'message': 'No text provided'})
            material_name = 'Pasted Text'
        
        else:
            return jsonify({'success': False, 'message': 'No material provided'})
        
        # Add text to session if we got any
        if text and len(text) > 0:
            session['materials'].append(text)
            session['material_names'].append(material_name)
            session.modified = True
            
            total_chars = sum(len(m) for m in session['materials'])
            
            return jsonify({
                'success': True,
                'message': f'Material added successfully ({len(text)} characters)',
                'materials_count': len(session['materials']),
                'total_characters': total_chars,
                'material_names': session['material_names']
            })
        else:
            return jsonify({'success': False, 'message': 'Material appears to be empty'})
    
    except Exception as e:
        print(f"Error in upload_material: {e}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})


@app.route('/start-game', methods=['POST'])
def start_game():
    """Initialize a new game"""
    try:
        if 'materials' not in session or not session['materials']:
            return jsonify({
                'success': False,
                'message': 'Please add study materials first'
            })
        
        if len(session['materials']) == 0:
            return jsonify({
                'success': False,
                'message': 'No materials available. Please add study content.'
            })
        
        # Verify materials contain text
        combined_material = "\n".join(session['materials'])
        print(f"Starting game with {len(session['materials'])} materials, {len(combined_material)} total characters")
        
        if len(combined_material) < 50:
            return jsonify({
                'success': False,
                'message': 'Materials appear too short. Please add more content.'
            })
        
        if len(combined_material) > 3000:
            combined_material = combined_material[:3000]
            print("Material truncated to 3000 characters")
        
        print("Generating questions...")
        questions = generate_questions_with_openai(combined_material)
        
        if not questions or len(questions) < 2:
            return jsonify({
                'success': False,
                'message': 'Could not generate questions from materials. Try adding different content.'
            })
        
        print(f"Generated {len(questions)} questions")
        password = generate_password_with_openai(combined_material)
        print(f"Generated password: {password}")
        
        session['game_state'] = {
            'questions': questions,
            'password': password,
            'guessed_letters': [],
            'current_question_idx': 0,
            'correct_answers': 0,
            'game_active': True,
            'combined_material': combined_material,
            'answered_this_round': False,
            'last_answer_correct': None
        }
        session.modified = True
        
        return jsonify({
            'success': True,
            'message': 'Game started!',
            'password_length': len(password)
        })
    
    except Exception as e:
        print(f"Error in start_game: {e}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/get-question', methods=['GET'])
def get_question():
    """Get the current question"""
    try:
        if 'game_state' not in session or not session['game_state']['game_active']:
            return jsonify({
                'success': False,
                'message': 'No active game'
            })
        
        game = session['game_state']
        
        if game['current_question_idx'] >= len(game['questions']):
            game['current_question_idx'] = 0
        
        question, answer = game['questions'][game['current_question_idx']]
        password_display = display_password(game['password'], game['guessed_letters'])
        
        return jsonify({
            'success': True,
            'question': question,
            'question_number': game['correct_answers'] + 1,
            'password_display': password_display,
            'correct_answers': game['correct_answers'],
            'guessed_letters': sorted(game['guessed_letters'])
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/submit-answer', methods=['POST'])
def submit_answer():
    """Submit an answer to the current question"""
    try:
        if 'game_state' not in session or not session['game_state']['game_active']:
            return jsonify({'success': False, 'message': 'No active game'})
        
        user_answer = request.json.get('answer', '').strip()
        if not user_answer:
            return jsonify({'success': False, 'message': 'Please enter an answer'})
        
        game = session['game_state']
        question, correct_answer = game['questions'][game['current_question_idx']]
        
        is_correct = check_answer_with_openai(user_answer, question, correct_answer)
        
        game['answered_this_round'] = True
        game['last_answer_correct'] = is_correct
        
        if is_correct:
            game['correct_answers'] += 1
            game['current_question_idx'] += 1
            # Loop back to beginning if we've gone through all questions
            if game['current_question_idx'] >= len(game['questions']):
                game['current_question_idx'] = 0
            message = "✓ Correct! Now guess a letter in the password."
        else:
            message = f"✗ Incorrect. The correct answer was: {correct_answer}"
            game['current_question_idx'] += 1
            # Loop back to beginning if we've gone through all questions
            if game['current_question_idx'] >= len(game['questions']):
                game['current_question_idx'] = 0
        
        session.modified = True
        
        return jsonify({
            'success': True,
            'correct': is_correct,
            'message': message,
            'correct_answer': correct_answer
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/guess-letter', methods=['POST'])
def guess_letter():
    """Guess a letter in the password"""
    try:
        if 'game_state' not in session or not session['game_state']['game_active']:
            return jsonify({'success': False, 'message': 'No active game'})
        
        letter = request.json.get('letter', '').strip().upper()
        
        if len(letter) != 1 or not letter.isalpha():
            return jsonify({'success': False, 'message': 'Please enter a single letter'})
        
        game = session['game_state']
        
        if letter in game['guessed_letters']:
            return jsonify({
                'success': False,
                'message': f"You already guessed '{letter}'"
            })
        
        game['guessed_letters'].append(letter)
        password = game['password']
        
        if letter in password:
            message = f"✓ Great! '{letter}' is in the password!"
            letter_found = True
        else:
            message = f"✗ Sorry, '{letter}' is not in the password."
            letter_found = False
        
        password_display = display_password(password, game['guessed_letters'])
        
        # Check if game is won
        game_won = all(l in game['guessed_letters'] for l in password)
        
        if game_won:
            game['game_active'] = False
            message = f"🎉 CONGRATULATIONS! YOU WON! 🎉\nThe password was: {password}"
        
        session.modified = True
        
        return jsonify({
            'success': True,
            'message': message,
            'letter_found': letter_found,
            'password_display': password_display,
            'guessed_letters': sorted(game['guessed_letters']),
            'game_won': game_won,
            'correct_answers': game['correct_answers']
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/new-game', methods=['POST'])
def new_game():
    """Reset and start a new game with fresh password and questions"""
    try:
        if 'materials' not in session or not session['materials']:
            return jsonify({
                'success': False,
                'message': 'No materials available. Please add study content.'
            })
        
        combined_material = "\n".join(session['materials'])
        
        if len(combined_material) > 3000:
            combined_material = combined_material[:3000]
        
        # Generate fresh questions and password for the new game
        print("Generating new game content...")
        questions = generate_questions_with_openai(combined_material)
        
        if not questions or len(questions) < 2:
            return jsonify({
                'success': False,
                'message': 'Could not generate questions. Try adding different content.'
            })
        
        password = generate_password_with_openai(combined_material)
        print(f"Generated new password: {password}")
        
        # Create fresh game state
        session['game_state'] = {
            'questions': questions,
            'password': password,
            'guessed_letters': [],
            'current_question_idx': 0,
            'correct_answers': 0,
            'game_active': True,
            'combined_material': combined_material,
            'answered_this_round': False,
            'last_answer_correct': None
        }
        session.modified = True
        
        return jsonify({
            'success': True,
            'message': 'New game started!',
            'password_length': len(password)
        })
    
    except Exception as e:
        print(f"Error in new_game: {e}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/clear-materials', methods=['POST'])
def clear_materials():
    """Clear all materials"""
    session.pop('materials', None)
    session.pop('game_state', None)
    session.modified = True
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)
