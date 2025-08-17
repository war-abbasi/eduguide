# 🎓 EduGuide – Education Chatbot with Memory

EduGuide is a simple conversational AI assistant focused on **education-related queries** such as:

* Studying abroad 🌍
* University admissions 🏫
* Scholarships 💰
* Courses & majors 📚
* Exams & academic life ✏️

The chatbot can **remember context during a session** (like your name, study destination, and preferred course), so conversations feel more natural.

---

## ✨ Features

* **Conversational memory** – remembers previous user messages during a session.
* **Context slots** – automatically extracts:

  * Name
  * Study destination
  * Course/degree of interest
* **Session persistence** – chat history is saved in a JSON file so you can resume later.
* **Commands**:

  * `reset` → clear memory
  * `summary` → show a summary of the session
  * `exit` → quit the chatbot
* **Typing effect** – replies are streamed word by word for a natural feel.

---

## 🛠️ Tech Stack

* [Python 3](https://www.python.org/)
* [LangChain](https://www.langchain.com/) for conversation management
* [OpenAI / OpenRouter](https://openrouter.ai/) compatible models for responses
* Simple JSON-based memory store

---

## 📂 Project Structure

```
EduGuide-Chatbot/
│── edu_assistant.py      # Main chatbot file
│── requirements.txt      # Dependencies
│── .env.example          # Example environment variables
│── edu_memory.json       # Auto-created file to save memory
│── README.md             # Project documentation
```

---

## ⚙️ Setup Instructions

1. **Clone the repo**

   ```bash
   git clone https://github.com/your-username/EduGuide-Chatbot.git
   cd EduGuide-Chatbot
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Setup environment**

   * Copy `.env.example` → `.env`
   * Add your API key:

     ```
     OPENAI_API_KEY=sk-xxxx
     # Optional (if using OpenRouter):
     OPENAI_BASE_URL=https://openrouter.ai/api/v1
     MODEL_NAME=deepseek/deepseek-r1-0528:free
     ```

4. **Run the chatbot**

   ```bash
   python edu_assistant.py
   ```

---

## 🖼️ Screenshots (to add later)

* **Startup screen**
* **Asking for a scholarship**
* **Session summary example**

👉 Just take terminal screenshots after running and paste them here.

---

## 🚀 Example Conversation

```
🎓 Welcome to EduGuide Chatbot
Ask me about study abroad, scholarships, courses, etc.
Type 'exit' to quit, 'reset' to clear memory, 'summary' to see session summary.

You: Hi, my name is Ayesha
AI: Nice to meet you, Ayesha! How can I help with your studies today?

You: I want to study in Canada
AI: That’s great! Canada has many strong universities. Are you looking into undergraduate or postgraduate options?

You: I am interested in Computer Science
AI: Perfect! Computer Science in Canada is a very popular choice. Let me tell you about scholarships available...
```

---

## 📌 Future Improvements

* Replace JSON with SQLite for more robust storage.
* Add a web interface using **Streamlit** or **FastAPI**.
* Expand slot extraction with NLP instead of regex.

---

## 👩‍🎓 Author

This project was developed as part of my learning in **AI + LangChain**.
EduGuide aims to help students explore educational opportunities in a friendly, conversational way.

