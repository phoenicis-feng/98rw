import os
import sys
from google import genai

try:
    client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
    chat = client.chats.create(model="gemini-2.0-flash")
    response = chat.send_message("Say hello")
    print("SUCCESS")
    print(response.text)
except Exception as e:
    print(f"FAILED: {e}", file=sys.stderr)
