# 🧠 AI Quiz Generator 📝

[![Streamlit App](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=Streamlit)](https://ai-quiz-app-muntasir.streamlit.app/))
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)

This web app, built with Streamlit and the Google Gemini API, instantly generates a multiple-choice quiz from any piece of text.

## 🚀 Live Demo

### [Click here to try the app!](https://ai-quiz-app-muntasir.streamlit.app/)

---

## 📸 Demo

<img width="1901" height="882" alt="Screenshot (158)" src="https://github.com/user-attachments/assets/731d74c3-5f5d-49cb-a659-6d96de8ddb30" />
<img width="1703" height="791" alt="Screenshot (159)" src="https://github.com/user-attachments/assets/2b90bfed-eb9b-4269-8a18-0190112e95af" />

---

## ✨ Features

* **Generate from Any Text:** Paste in any article, notes, or document.
* **Variable Difficulty:** Choose from Easy, Medium, or Hard quizzes.
* **Instant Scoring:** Submitting the quiz provides an immediate score and shows the correct answers.

---

## 🔧 Tech Stack

* **Frontend:** Streamlit
* **Backend:** Python
* **AI Model:** Google Gemini API (`gemini-2.5-pro`)
* **Deployment:** Streamlit Community Cloud

---

## ⚙️ How to Run Locally

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/rizuahmed09/ai-quiz-app.git](https://github.com/rizuahmed09/ai-quiz-app.git)
    cd ai-quiz-app
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv quiz_env
    source quiz_env/bin/activate  # On Windows: quiz_env\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create your .env file:**
    Create a file named `.env` in the root folder and add your API key:
    ```
    GOOGLE_API_KEY="your-secret-api-key-here"
    ```

5.  **Run the app:**
    ```bash
    streamlit run quizapp.py
    ```
