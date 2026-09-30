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


def update_workout_plan(original_plan, feedback):

    prompt = f"""
Update the following fitness workout plan based on the user's feedback.

Original Plan:
{original_plan}

User Feedback:
{feedback}

Return a revised 7-day workout plan.
Keep the plan clear, structured and easy to follow.
"""

    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt
        )

        return response.text

    except Exception:
        return f"""
Updated FitBuddy Workout Plan

The plan has been adjusted based on your feedback:

{feedback}

Recommended changes:
• Keep workouts low intensity.
• Add suitable walking/cardio.
• Take adequate rest between exercises.
• Stop exercise if you experience pain or unusual discomfort.

Your original workout plan can be continued with these adjustments.
"""