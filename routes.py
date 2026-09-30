from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from .database import SessionLocal, User
from .gemini_generator import generate_workout_gemini
from .gemini_flash_generator import generate_nutrition_tip_with_flash
from .updated_plan import update_workout_plan

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@router.post("/generate-workout")
async def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...)
):

    workout_plan = generate_workout_gemini(
        username,
        age,
        weight,
        goal,
        intensity
    )

    nutrition_tip = generate_nutrition_tip_with_flash(goal)

    db = SessionLocal()

    user = User(
        user_id=user_id,
        username=username,
        age=age,
        weight=str(weight),
        goal=goal,
        intensity=intensity,
        original_plan=workout_plan
    )

    db.add(user)
    db.commit()
    db.close()

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "username": username,
            "user_id": user_id,
            "age": age,
            "weight": weight,
            "goal": goal,
            "intensity": intensity,
            "workout_plan": workout_plan,
            "nutrition_tip": nutrition_tip
        }
    )


@router.post("/submit-feedback")
async def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...)
):

    db = SessionLocal()

    user = db.query(User).filter(
        User.user_id == user_id
    ).first()

    if not user:
        db.close()

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "error": "User not found."
            }
        )

    updated_plan = update_workout_plan(
        user.original_plan,
        feedback
    )

    user.updated_plan = updated_plan

    db.commit()

    username = user.username
    age = user.age
    weight = user.weight
    goal = user.goal
    intensity = user.intensity

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "username": username,
            "user_id": user_id,
            "age": age,
            "weight": weight,
            "goal": goal,
            "intensity": intensity,
            "workout_plan": updated_plan,
            "nutrition_tip": "Your workout plan has been updated based on your feedback.",
            "message": "Workout plan updated successfully."
        }
    )


@router.get("/view-all-users")
async def view_all_users(request: Request):

    db = SessionLocal()

    users = db.query(User).all()

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={
            "users": users
        }
    )