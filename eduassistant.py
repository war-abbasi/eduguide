import os
import re
import json
import time
from typing import List, Dict, Any, Optional

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, BaseMessage
from langchain_openai import ChatOpenAI

# Load keys and settings from .env
load_dotenv()

BASE_PROMPT = (
    "You are EduGuide, a helpful academic assistant. "
    "You should only answer questions related to education: universities, "
    "scholarships, study abroad, courses, exams, and student life. "
    "If asked about something else, politely say that you only answer education-related questions.\n\n"
    "Consider any context provided (name, destination, course) when shaping your replies."
)

# ---------- Memory Handler ----------
class EduMemoryManager:
    """
    Very lightweight session manager.
    Stores chat history and extracted user details (slots).
    Persists everything to JSON so the session can be resumed.
    """

    def __init__(self, filepath: str = "edu_memory.json"):
        self.filepath = filepath
        self.session: Dict[str, Any] = {"history": [], "slots": {}}
        self._load()

    def _load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    self.session = json.load(f)
            except Exception:
                self.session = {"history": [], "slots": {}}

    def save(self):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.session, f, indent=2)

    # ----- history -----
    def add_turn(self, role: str, content: str):
        self.session["history"].append({"role": role, "content": content})
        self.save()

    def get_history(self) -> List[BaseMessage]:
        msgs: List[BaseMessage] = []
        for h in self.session["history"]:
            if h["role"] == "system":
                msgs.append(SystemMessage(content=h["content"]))
            elif h["role"] == "user":
                msgs.append(HumanMessage(content=h["content"]))
            else:
                msgs.append(AIMessage(content=h["content"]))
        return msgs

    # ----- slots -----
    def set_slot(self, key: str, value: str):
        self.session["slots"][key] = value
        self.save()

    def get_slot(self, key: str, default: Optional[str] = None) -> Optional[str]:
        return self.session["slots"].get(key, default)

    def clear(self):
        self.session = {"history": [], "slots": {}}
        self.save()


# ---------- Context Builder ----------
def build_system_context(memory: EduMemoryManager) -> str:
    name = memory.get_slot("name")
    dest = memory.get_slot("destination")
    course = memory.get_slot("course")
    details = []
    if name:
        details.append(f"User’s name: {name}")
    if dest:
        details.append(f"Preferred study destination: {dest}")
    if course:
        details.append(f"Interested course/degree: {course}")
    if details:
        return BASE_PROMPT + "\n\nContext:\n- " + "\n- ".join(details)
    return BASE_PROMPT


# ---------- Slot Extractors (rule-based, simple) ----------
patterns = {
    "name": [
        r"\bmy name is\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)",
        r"\bi am\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)",
    ],
    "destination": [
        r"\b(study|want to study|plan to study)\s+(?:in|at)\s+([A-Za-z\s]+)",
        r"\bdestination\s*:\s*([A-Za-z\s]+)",
    ],
    "course": [
        r"\b(interested in|want to study|course is)\s+([A-Za-z\s]+)",
        r"\bmajor\s*:\s*([A-Za-z\s]+)",
    ],
}

def capture_slots(user_text: str, memory: EduMemoryManager):
    for key, pats in patterns.items():
        for pat in pats:
            match = re.search(pat, user_text, flags=re.IGNORECASE)
            if match:
                value = match.groups()[-1].strip(" .!?")
                if len(value.split()) <= 6:  # avoid nonsense captures
                    memory.set_slot(key, value)
                break


# ---------- Model Setup ----------
def get_llm() -> ChatOpenAI:
    return ChatOpenAI(
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL") or None,
        model=os.getenv("MODEL_NAME") or "gpt-4o-mini",
    )


def stream_response(llm: ChatOpenAI, messages: List[BaseMessage]) -> str:
    full_text = ""
    for chunk in llm.stream(messages):
        text = getattr(chunk, "content", None)
        if text:
            print(text, end="", flush=True)
            full_text += text
            time.sleep(0.01)
    print()
    return full_text.strip()


# ---------- Main Loop ----------
def main():
    print("🎓 Welcome to EduGuide Chatbot")
    print("Ask me about study abroad, scholarships, courses, etc.")
    print("Type 'exit' to quit, 'reset' to clear memory, 'summary' to see session summary.\n")

    memory = EduMemoryManager()
    llm = get_llm()

    while True:
        try:
            user_msg = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_msg:
            continue

        if user_msg.lower() == "exit":
            print("Goodbye!")
            break

        if user_msg.lower() == "reset":
            memory.clear()
            print("✅ Memory cleared.")
            continue

        if user_msg.lower() == "summary":
            print("\n--- Session Summary ---")
            for t in memory.session["history"]:
                print(f"{t['role'].capitalize()}: {t['content']}")
            print("-----------------------\n")
            continue

        # slot filling
        capture_slots(user_msg, memory)

        # rebuild system prompt with context
        sys_context = build_system_context(memory)

        # messages
        convo = [SystemMessage(content=sys_context)]
        convo += memory.get_history()
        convo.append(HumanMessage(content=user_msg))

        memory.add_turn("user", user_msg)

        print("AI: ", end="", flush=True)
        reply = stream_response(llm, convo)
        memory.add_turn("assistant", reply)


if __name__ == "__main__":
    main()
