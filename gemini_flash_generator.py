import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.8-flash"
)


def generate_nutrition_tip_with_flash(goal):

    prompt = f"""
Give one concise and practical nutrition or recovery tip
for a person whose fitness goal is: {goal}

Keep it simple and actionable.
"""

    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt
        )

        return response.text

    except Exception:
        return f"""
For your {goal} goal, focus on balanced meals,
adequate protein, vegetables, fruits, whole grains,
and enough water. Maintain consistent sleep and recovery.
"""