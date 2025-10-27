import streamlit as st
import json
import os
from dotenv import load_dotenv
import google.generativeai as genai
import google.api_core.exceptions 

# --- Constants ---
DEFAULT_MODEL_NAME = 'gemini-2.5-pro' 

# --- Load Environment Variables ---
load_dotenv()

# --- Configure Google Gemini Client ---
def configure_google_ai():
    """Configures the Google Generative AI client."""
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        st.error("⚠️ Google API Key not found. Please set the GOOGLE_API_KEY in your .env file.")
        return False
    try:
        genai.configure(api_key=google_api_key)
        return True
    except Exception as e:
        st.error(f"Fatal error during Google AI configuration: {e}")
        return False

# --- API Call Function ---
def fetch_questions(text_content, quiz_level, model_name=DEFAULT_MODEL_NAME):
    """Fetches MCQ questions from the Google Gemini API."""
    
    # Prompt with the JSON guide inlined
    prompt = f"""
    Text: {text_content}

    You are an expert in generating MCQ quizzes based on provided content.
    Given the above text, create a quiz of exactly 3 multiple choice questions with a difficulty level of {quiz_level}.

    Ensure the questions are unique, directly answerable from the text, and appropriate for the difficulty level.

    You MUST format your response as a single, valid JSON object. Do not include ANY text, comments, or markdown formatting (like ```json) before or after the JSON object.
    Your response must follow this structure precisely:
    {json.dumps({
      "mcqs": [
        {"mcq": "question1", "options": {"a": "c1", "b": "c2", "c": "c3", "d": "c4"}, "correct": "a"},
        {"mcq": "question2", "options": {"a": "c1", "b": "c2", "c": "c3", "d": "c4"}, "correct": "b"},
        {"mcq": "question3", "options": {"a": "c1", "b": "c2", "c": "c3", "d": "c4"}, "correct": "c"}
      ]
    }, indent=2)}
    """

    generation_config = genai.GenerationConfig(
        temperature=0.3,
        max_output_tokens=1500,
        response_mime_type="application/json",
    )

    extracted_response = ""
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt, generation_config=generation_config)
        
        if not response.parts:
             block_reason = response.prompt_feedback.block_reason if response.prompt_feedback else "Unknown"
             st.error(f"Failed to generate quiz. Response was empty or blocked. Reason: {block_reason}")
             return []

        extracted_response = response.text
        
        # Clean potential markdown wrappers (```json ... ```)
        cleaned_response = extracted_response.strip().removeprefix("```json").removesuffix("```").strip()

        quiz_data = json.loads(cleaned_response)
        mcqs = quiz_data.get("mcqs", [])

        if not isinstance(mcqs, list) or len(mcqs) == 0:
             st.error("API returned unexpected JSON structure or empty MCQs list.")
             return []

        return mcqs

    except json.JSONDecodeError:
        st.error(f"Failed to parse the API response as JSON. Check console log for raw response.")
        print(f"RAW API RESPONSE (JSON PARSE FAILED):\n{extracted_response}")
        return []

    # --- ADD THIS NEW BLOCK ---
    except google.api_core.exceptions.ResourceExhausted as e:
        st.error("🚦 Rate limit exceeded. The API is busy. Please wait a minute and try again.")
        print(f"RATE LIMIT ERROR: {e}")
        return []
    # --- END NEW BLOCK ---

    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        print(f"UNEXPECTED ERROR: {e}") # Log to console for debugging
        return []

# --- Main Streamlit Application Logic ---
def main():
    st.set_page_config(page_title="Quiz Generator App", layout="wide")
    st.title("🧠 Quiz Generator App 📝")
    st.markdown("Paste text, select difficulty, and generate a 3-question MCQ quiz!")

    # Use setdefault to initialize session state keys concisely
    st.session_state.setdefault('questions', [])
    st.session_state.setdefault('corrected_answers', [])

    if not configure_google_ai():
        st.stop() # Stop if configuration fails

    # --- User Inputs ---
    col1, col2 = st.columns([3, 1])
    with col1:
        text_content = st.text_area("Paste the text content here:", height=300)
    with col2:
        quiz_level = st.selectbox("Select quiz level:", ["Easy", "Medium", "Hard"])
        generate_button = st.button("✨ Generate Quiz")

    # --- Quiz Generation Logic ---
    if generate_button:
        # Reset previous quiz state
        st.session_state.questions = []
        st.session_state.corrected_answers = []

        if text_content:
            with st.spinner("🤖 Generating your quiz..."):
                questions = fetch_questions(text_content, quiz_level.lower())
                if questions:
                    st.session_state.questions = questions
                    try:
                        # Extract correct answers
                        st.session_state.corrected_answers = [
                            q["options"][q["correct"]] for q in questions
                        ]
                        st.success("Quiz generated successfully!")
                    except KeyError as e:
                        st.error(f"Error processing generated questions: Invalid structure ({e}).")
                        st.session_state.questions = [] # Clear invalid state
        else:
            st.error("⚠️ Please paste some text content to generate a quiz.")

    # --- Display Quiz Form (if questions exist in session state) ---
    if st.session_state.questions:
        with st.form("quiz_form"):
            st.header("📋 Here is your quiz:")
            st.markdown("---")
            user_selections = {}

            for i, q in enumerate(st.session_state.questions):
                 st.subheader(f"Question {i+1}: {q.get('mcq', 'Missing question text')}")
                 options = list(q.get("options", {}).values())
                 user_selections[i] = st.radio(
                     "Choose one:", options, index=None, key=f"q_{i}"
                 )
            
            st.markdown("---")
            submitted = st.form_submit_button("✅ Submit Answers")

            if submitted:
                # Check if any question was left unanswered
                if None in user_selections.values():
                    st.warning("⚠️ Please answer all questions before submitting.")
                else:
                    marks = 0
                    st.header("📊 Quiz Result:")
                    st.markdown("---")

                    for i, question in enumerate(st.session_state.questions):
                        selected = user_selections.get(i)
                        correct = st.session_state.corrected_answers[i]

                        st.subheader(f"Question {i+1}: {question['mcq']}")
                        st.write(f"Your answer: **{selected}**")
                        st.write(f"Correct answer: **{correct}**")

                        if str(selected).strip().lower() == str(correct).strip().lower():
                            marks += 1
                            st.success("✔️ Correct!")
                        else:
                            st.error("❌ Incorrect.")
                        st.markdown("---")

                    st.subheader(f"🏁 Your Final Score: {marks} out of {len(st.session_state.questions)}")
                    
                    # Clear session state and rerun to show a fresh app state
                    # del st.session_state.questions
                    # del st.session_state.corrected_answers
                    # st.rerun()

# --- Main execution block ---
if __name__ == "__main__":
    main()