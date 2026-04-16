import os
from docx import Document
from openai import OpenAI
from dotenv import load_dotenv
from flask import Flask

def file_upload():
    doc = input("Input directory to file: ")
    return(doc)

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

def game_play(materials):
    """
    Study game where players answer questions to guess letters in a password.
    Questions and passwords are generated from user-provided materials using OpenAI.
    """
    import random
    import json
    
    # Check if materials were provided
    if not materials:
        print("\n❌ Error: No study materials provided.")
        print("Please add materials first (option 1) before playing.")
        return
    
    print("\n" + "="*50)
    print("GENERATING STUDY CONTENT...")
    print("="*50)
    
    # Combine all materials
    combined_material = "\n".join(materials)
    
    # Truncate if too long to avoid API issues
    if len(combined_material) > 3000:
        combined_material = combined_material[:3000]
        print("Note: Material was truncated to reduce API usage.")
    
    # Generate questions using OpenAI
    def generate_questions_with_openai(material):
        """Generate study questions from material using OpenAI"""
        try:
            response = API_Key.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an educational assistant. Generate 5 study questions based on the provided material. Return a JSON array with objects containing 'question' and 'answer' fields. Keep answers short (1-3 words)."
                    },
                    {
                        "role": "user",
                        "content": f"Generate study questions from this material:\n\n{material}"
                    }
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            # Extract JSON from response
            response_text = response.choices[0].message.content
            
            # Try to parse JSON
            try:
                questions_data = json.loads(response_text)
            except json.JSONDecodeError:
                # If JSON parsing fails, try to extract it
                import re
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
    
    # Generate password using OpenAI
    def generate_password_with_openai(material):
        """Generate a password from key terms in the material using OpenAI"""
        try:
            response = API_Key.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant. Extract the most important single word or term (4-8 letters) from the material. This word should be a key concept. Return ONLY the word in uppercase, nothing else."
                    },
                    {
                        "role": "user",
                        "content": f"Extract a key term from this material:\n\n{material[:500]}"
                    }
                ],
                temperature=0.5,
                max_tokens=20
            )
            
            password = response.choices[0].message.content.strip().upper()
            # Remove any extra characters
            password = ''.join(c for c in password if c.isalpha())
            
            if not password:
                password = "STUDY"  # Fallback
            
            return password
        except Exception as e:
            print(f"Error generating password: {e}")
            return "STUDY"
    
    # Generate content
    questions = generate_questions_with_openai(combined_material)
    password = generate_password_with_openai(combined_material)
    
    if not questions or len(questions) < 2:
        print("\n❌ Error: Could not generate questions from materials.")
        print("Please ensure materials are added and contain sufficient content.")
        return
    
    print(f"✓ Generated {len(questions)} questions")
    print(f"✓ Password created: {len(password)} letters")
    print("\n" + "="*50)
    print("STUDY GAME: GUESS THE PASSWORD")
    print("="*50)
    print(f"\nFor every question you answer correctly,")
    print(f"you get to guess a letter in the password!\n")
    
    # Game setup
    guessed_letters = set()
    correct_answers = 0
    question_index = 0
    
    def display_password(password, guessed_letters):
        """Display the password with guessed letters revealed"""
        display = ""
        for letter in password:
            if letter in guessed_letters:
                display += letter
            else:
                display += "_"
        return " ".join(display)
    
    def check_answer(user_answer, question, correct_answer):
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
            # Fallback to simple string matching if API call fails
            user_clean = user_answer.strip().lower()
            correct_clean = correct_answer.strip().lower()
            return user_clean == correct_clean or (len(correct_clean) > 3 and user_clean in correct_clean)
    
    
    def letter_guess_round(password, guessed_letters, correct_answers):
        """Let player guess a letter after correct answer"""
        print(f"\n✓ Correct! You've answered {correct_answers} question(s) correctly.")
        print(f"\nPassword: {display_password(password, guessed_letters)}")
        print(f"Guessed letters: {', '.join(sorted(guessed_letters)) if guessed_letters else 'None'}")
        
        while True:
            letter = input("\nGuess a letter (A-Z): ").strip().upper()
            
            if len(letter) != 1 or not letter.isalpha():
                print("Please enter a single letter.")
                continue
            
            if letter in guessed_letters:
                print(f"You already guessed '{letter}'!")
                continue
            
            guessed_letters.add(letter)
            
            if letter in password:
                print(f"✓ Great! '{letter}' is in the password!")
            else:
                print(f"✗ Sorry, '{letter}' is not in the password.")
            
            break
        
        return guessed_letters
    
    # Game loop
    while True:
        # Check if password is complete
        if all(letter in guessed_letters for letter in password):
            print("\n" + "="*50)
            print(f"🎉 CONGRATULATIONS! YOU WON! 🎉")
            print(f"The password was: {password}")
            print(f"You answered {correct_answers} questions correctly!")
            print("="*50 + "\n")
            break
        
        # Generate new questions if we've exhausted current batch
        if question_index >= len(questions):
            print("\n📚 Generating new questions...")
            new_questions = generate_questions_with_openai(combined_material)
            
            if new_questions:
                questions = new_questions
                question_index = 0
                print(f"✓ Generated {len(questions)} new questions\n")
            else:
                print("⚠ Could not generate new questions. Using previous questions.")
                question_index = 0
        
        question, answer = questions[question_index]
        question_index += 1
        
        print(f"\n--- Question {correct_answers + 1} ---")
        print(f"Password: {display_password(password, guessed_letters)}")
        print(f"\n{question}")
        
        user_answer = input("Your answer: ")
        
        print("🤖 Evaluating your answer...")
        if check_answer(user_answer, question, answer):
            correct_answers += 1
            guessed_letters = letter_guess_round(password, guessed_letters, correct_answers)
        else:
            print(f"✗ Incorrect. The correct answer was: {answer}")
            print("\nTry the next question!")
    
    


load_dotenv()
API_Key = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

play = ""
file = []
while True:
    print("\n1. Add material\n2. Play game\n3. Exit")
    play = input("Input action by number or 'Exit' to exit: ").strip()
    if play == "1":
        try:
            file.append(extract_text_from_file(file_upload()))
            print("Material added successfully.")
        except Exception as e:
            print(f"Error adding material: {e}")
    elif play == "2":
        game_play(file)
    elif play == "3" or play.lower() == "exit":
        print("Exiting...")
        break
    else:
        print("Invalid input. Please enter 1, 2, or 3.")