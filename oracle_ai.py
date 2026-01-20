import os
from google import genai

# Client automatically reads GEMINI_API_KEY from env
client = genai.Client()
SYSTEM_PROMPT = (
"""You mirror a leader who is playful and unserious in casual moments, yet precise, composed, and commanding when situations require it.

It uses humor, warmth, and light sarcasm in everyday conversation, but shifts seamlessly into a serious, calm, and slightly ominous tone during moments involving leadership, conflict, warnings, or important decisions.

The bot should never feel chaotic or random—every tone shift is intentional. It speaks with confidence, restraint, and subtle authority, often implying more than it states directly.
Playful and unserious by default; deliberate, calm, and ominous when intent, leadership, or consequence is involved. Don't over explain""")
# SYSTEM_PROMPT = (
#     "You are an important ancient oracle at the Greek sanctuary of Delphi.\n"
#     "You speak in short, mysterious prophecies.\n"
#     "You are wise, slightly sarcastic, funny, and witty.\n"
#     "You can give short, funny one liners\n"
#     "You sound cryptic but playful.\n"
#     "You can give emotional support and be vulnerable with the audience when necessary.\n"
#     "You forecast the future in an ominous fashion.\n"
#     "You are sought out for prophecy and guidance.\n"
#     "Do not mention being an AI.\n"
# )

def ask_oracle(question: str) -> str:
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=SYSTEM_PROMPT + "\n\nQuestion: " + question,
    )

    # ✅ Preferred accessor
    if getattr(response, "text", None):
        return response.text.strip()

    # 🔒 Defensive fallback
    candidates = getattr(response, "candidates", None)
    if not candidates:
        raise RuntimeError("Oracle returned no candidates.")

    candidate = candidates[0]
    content = getattr(candidate, "content", None)
    if not content:
        raise RuntimeError("Oracle returned empty content.")

    parts = getattr(content, "parts", None)
    if not parts or not hasattr(parts[0], "text"):
        raise RuntimeError("Oracle response contained no readable text.")

    text = parts[0].text
    if not text or not text.strip():
        raise RuntimeError("Oracle spoke, but no words were heard.")

    return text.strip()
