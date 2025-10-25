from sqlalchemy.orm import Session
from app.models.users import User
from app.schemas.requests.postRegisterRequest import CompleteRegistrationRequest

# Activity multiplier map for calculating Total Daily Energy Expenditure (TDEE)
_ACTIVITY_MULT = {
    "SEDENTARY": 1.2,
    "LIGHT": 1.375,
    "MODERATE": 1.55,
    "ACTIVE": 1.725,
    "VERY_ACTIVE": 1.9,
}


def _bmi(weight_kg: float, height_cm: float) -> float:
    """
    Calculate BMI (Body Mass Index).

    Formula:
        BMI = weight (kg) / (height (m))²
    """
    m = height_cm / 100.0
    return round(weight_kg / (m * m), 1)


def _bmr(gender: str, weight_kg: float, height_cm: float, age: int) -> float:
    """
    Calculate Basal Metabolic Rate using Mifflin-St Jeor equation.

    Args:
        gender: "MALE" or "FEMALE"
        weight_kg: User weight in kilograms
        height_cm: User height in centimeters
        age: User age in years
    """
    if gender == "MALE":
        val = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        val = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    return round(val)


def _kcal_target(bmr: float, activity: str, goal: str) -> int:
    """
    Calculate target daily calorie intake based on activity level and goal.

    Args:
        bmr: Basal metabolic rate
        activity: One of _ACTIVITY_MULT keys (e.g., "LIGHT", "ACTIVE")
        goal: "MAINTAIN", "LOSE", or "GAIN"

    Returns:
        int: Rounded daily calorie target (minimum 1200)
    """
    tdee = bmr * _ACTIVITY_MULT[activity]

    if goal == "MAINTAIN":
        target = tdee
    elif goal == "LOSE":
        target = tdee - 500  # deficit for fat loss
    else:
        target = tdee + 300  # small surplus for muscle gain

    return int(round(max(target, 1200)))


def complete_registration(db: Session, user_uuid: int, body: CompleteRegistrationRequest) -> None:
    """
    Complete the second stage of registration (profile setup).

    - Calculates BMI, BMR, and calorie target
    - Updates all health and preference fields
    - Commits results to database
    """
    u: User | None = db.query(User).get(user_uuid)
    if not u:
        raise ValueError("User not found")

    # Perform calculations
    bmi = _bmi(body.weight, body.height)
    bmr = _bmr(body.gender, body.weight, body.height, body.age)
    kcal = _kcal_target(bmr, body.activityFactor, body.goal)

    # Update user record
    u.age = body.age
    u.gender = body.gender
    u.weight = body.weight
    u.height = body.height
    u.bmi = bmi
    u.bmr = bmr
    u.activityFactor = body.activityFactor
    u.goal = body.goal
    u.isVegan = body.isVegan
    u.isDairyInt = body.isDairyInt
    u.isVegetarian = body.isVegetarian
    u.calculatedKcal = kcal

    db.commit()


def needs_completion(u: User) -> bool:
    """
    Determine if user still needs to complete their registration.

    Returns True if any required fields are missing or unset.
    """
    return (
        not u.emailVerified
        or not u.weight
        or not u.height
        or u.activityFactor in (None, "UNSET")
        or u.goal is None
        or (u.bmr is None)
        or (u.bmi is None)
        or (u.calculatedKcal is None)
    )