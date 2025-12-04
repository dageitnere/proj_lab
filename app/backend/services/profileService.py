from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from app.backend.models.users import User
from app.backend.schemas.requests.postChangeDailyNutritionRequest import PostChangeDailyNutritionRequest
from app.backend.schemas.requests.postChangeProfileInfoRequest import PostChangeProfileInfoRequest
from app.backend.schemas.responses.ProfileResponse import ProfileResponse
from app.backend.schemas.requests.postRegisterRequest import CompleteRegistrationRequest
from app.backend.schemas.responses.calculatedNutritionInfoResponse import CalculatedNutritionInfoResponse

# Activity multiplier map for calculating Total Daily Energy Expenditure (TDEE)
_ACTIVITY_MULT = {
    "SEDENTARY": 1.15,
    "LIGHT": 1.3,
    "MODERATE": 1.45,
    "ACTIVE": 1.6,
    "VERY_ACTIVE": 1.75,
}

def _bmi(weight_kg: float, height_cm: float) -> float:
    """
    Calculate BMI (Body Mass Index).

    Formula:
        BMI = weight (kg) / (height (m))^2
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
        target = tdee - 200  # deficit for fat loss
    else:
        target = tdee + 300  # small surplus for muscle gain

    return int(round(max(target, 1200)))

def _macro_distribution(activity: str, goal: str) -> dict:
    """
    Returns recommended macro ratios (percent of total kcal) based on
    activity level and goal.
    """

    # Base defaults for MAINTAIN
    protein = 0.25
    carbs = 0.45
    fat = 0.30

    # Adjust by goal
    if goal == "LOSE":
        protein += 0.03    # more protein to preserve lean mass
        carbs -= 0.07      # carb reduction
        fat  -= 0.03
    elif goal == "GAIN":
        protein += 0.03
        carbs += 0.09

    # Adjust by activity
    if activity in ("ACTIVE", "VERY_ACTIVE"):
        carbs += 0.08
        protein += 0.02
        fat += 0.02
    elif activity in ("SEDENTARY", "LIGHT"):
        protein += 0.01
        carbs -= 0.03
        fat -= 0.02

    # Normalize if needed
    total = protein + carbs + fat
    protein /= total
    carbs /= total
    fat /= total

    return {
        "protein": protein,
        "carbs": carbs,
        "fat": fat
    }

def _macro_grams(total_kcal: int, activity: str, goal: str) -> dict:
    """
    Converts macro calorie percentages to actual gram targets.
    """

    ratios = _macro_distribution(activity, goal)

    kcal_protein = total_kcal * ratios["protein"]
    kcal_carbs   = total_kcal * ratios["carbs"]
    kcal_fat     = total_kcal * ratios["fat"]

    protein_g = round(kcal_protein / 4)
    carbs_g   = round(kcal_carbs / 4)
    fat_g     = round(kcal_fat / 9)

    sat_fat_g = round(fat_g * 0.45)

    sugar_g = round(carbs_g * 0.18)
    # Salt by activity level (mg)
    salt_map = {
        "SEDENTARY": 2500,
        "LIGHT": 2500,
        "MODERATE": 3500,
        "ACTIVE": 4500,
        "VERY_ACTIVE": 5500,
    }

    salt_g = salt_map.get(activity, 2500)  # default fallback

    return {
        "protein_g": protein_g,
        "carbs_g": carbs_g,
        "fat_g": fat_g,
        "sat_fat_g": sat_fat_g,
        "sugar_g": sugar_g,
        "salt_g": salt_g,
    }

def _get_dietary_preferences(user: User) -> list[str]:
    """Get list of active dietary preferences."""
    preferences = []

    if user.isVegan:
        preferences.append("Vegan")
    elif user.isVegetarian:
        preferences.append("Vegetarian")
    else:
        preferences.append("Omnivore")

    if user.isDairyInt:
        preferences.append("Dairy Intolerant")
    else:
        preferences.append("No Dairy Intolerance")

    return preferences

def _complete_registration(db: Session, user_uuid: int, request: CompleteRegistrationRequest) -> None:
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
    bmi = _bmi(request.weight, request.height)
    bmr = _bmr(request.gender, request.weight, request.height, request.age)
    kcal = _kcal_target(bmr, request.activityFactor, request.goal)
    macros = _macro_grams(kcal, request.activityFactor, request.goal)

    # Update user record
    u.age = request.age
    u.gender = request.gender
    u.weight = request.weight
    u.height = request.height
    u.bmi = bmi
    u.bmr = bmr
    u.activityFactor = request.activityFactor
    u.goal = request.goal
    u.isVegan = request.isVegan
    u.isDairyInt = request.isDairyInt
    u.isVegetarian = request.isVegetarian
    u.calculatedKcal = kcal
    u.calculatedProtein = macros["protein_g"]
    u.calculatedCarbs = macros["carbs_g"]
    u.calculatedFat = macros["fat_g"]
    u.calculatedSatFat = macros["sat_fat_g"]
    u.calculatedSugar = macros["sugar_g"]
    u.calculatedSalt = macros["salt_g"]
    db.commit()

def complete_info_submit(db: Session, request: CompleteRegistrationRequest, userUuid: int):
    try:
        _complete_registration(db, userUuid, request)
        return JSONResponse({"ok": True})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

def get_user_profile_data(db: Session, userUuid) -> tuple[User, ProfileResponse]:
    """
    Get the user and formatted profile data.

    Args:
        db: Database session
        request: FastAPI request object containing cookies

    Returns:
        Tuple of (User object, GetProfileRequest with formatted data)

    Raises:
        HTTPException: If user is not authenticated or not found
    """
    user = db.query(User).filter(User.uuid == userUuid).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return ProfileResponse(
        username=user.username,
        email=user.email,
        emailVerified=user.emailVerified,
        age=user.age,
        gender=user.gender,
        weight=user.weight,
        height=user.height,
        bmi=user.bmi,
        bmr=user.bmr,
        calculatedKcal=user.calculatedKcal,
        calculatedCarbs=user.calculatedCarbs,
        calculatedProtein=user.calculatedProtein,
        calculatedFat=user.calculatedFat,
        calculatedSatFat=user.calculatedSatFat,
        calculatedSugar=user.calculatedSugar,
        calculatedSalt=user.calculatedSalt,
        activityFactorDisplay=user.activityFactor,
        goalDisplay=user.goal,
        isVegan=user.isVegan,
        isVegetarian=user.isVegetarian,
        dairyIntolerance=user.isDairyInt
    )

def change_profile_info(db: Session, request: PostChangeProfileInfoRequest, userUuid: int):
    """
    Update selected user profile attributes.
    Only provided fields are updated.
    BMI, BMR, and macros are recalculated when necessary.
    """
    user = db.query(User).filter(User.uuid == userUuid).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Track if recalculation is needed
    recalc_needed = False

    # ---- UPDATE BASIC ATTRIBUTES ----
    if request.age is not None:
        user.age = request.age
        recalc_needed = True

    if request.weight is not None:
        user.weight = request.weight
        recalc_needed = True

    if request.height is not None:
        user.height = request.height
        recalc_needed = True

    if request.activityLevel is not None:
        user.activityFactor = request.activityLevel
        recalc_needed = True

    if request.goal is not None:
        user.goal = request.goal
        recalc_needed = True

    # ---- UPDATE DIETARY PREFERENCES ----
    if request.isVegan is not None:
        user.isVegan = request.isVegan
        if request.isVegan:
            user.isVegetarian = True
            user.isDairyInt = True

    if request.isVegetarian is not None:
        user.isVegetarian = request.isVegetarian

    if request.isDairyInt is not None:
        user.isDairyInt = request.isDairyInt

    # ---- RECALCULATE BMI / BMR / MACROS ----
    if recalc_needed and request.resetDailyNutrition:
        calculate_daily_nutrition(db, userUuid)

    db.commit()

    return {"message": "Profile updated successfully"}

def change_daily_nutrition(db: Session, request: PostChangeDailyNutritionRequest, userUuid: int,):
    """
    Update the user's daily calculated nutrition values (manual override).

    Only updates the fields that are provided in the request.
    """

    # Fetch the user
    user: User | None = db.query(User).filter(User.uuid == userUuid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update fields only if they are not None
    if request.calculatedKcal is not None:
        user.calculatedKcal = request.calculatedKcal
    if request.calculatedCarbs is not None:
        user.calculatedCarbs = request.calculatedCarbs
    if request.calculatedProtein is not None:
        user.calculatedProtein = request.calculatedProtein
    if request.calculatedFat is not None:
        user.calculatedFat = request.calculatedFat
    if request.calculatedSatFat is not None:
        user.calculatedSatFat = request.calculatedSatFat
    if request.calculatedSugar is not None:
        user.calculatedSugar = request.calculatedSugar
    if request.calculatedSalt is not None:
        user.calculatedSalt = request.calculatedSalt

    db.commit()

    return {"message": "Daily nutrition values updated successfully"}

def calculate_daily_nutrition(db: Session, userUuid: int):
    """
    Recalculate all calculated nutrition values (kcal, macros, satFat, sugar, salt)
    based on current profile info: weight, height, age, gender, activityFactor, goal.
    """

    user: User | None = db.query(User).filter(User.uuid == userUuid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # BMI and BMR
    user.bmi = _bmi(user.weight, user.height)
    user.bmr = _bmr(user.gender, user.weight, user.height, user.age)

    # Kcal target
    calculated_kcal = _kcal_target(user.bmr, user.activityFactor, user.goal)
    macros = _macro_grams(calculated_kcal, user.activityFactor, user.goal)

    # Update all nutrition fields
    user.calculatedKcal = calculated_kcal
    user.calculatedProtein = macros["protein_g"]
    user.calculatedCarbs = macros["carbs_g"]
    user.calculatedFat = macros["fat_g"]
    user.calculatedSatFat = macros["sat_fat_g"]
    user.calculatedSugar = macros["sugar_g"]
    user.calculatedSalt = macros["salt_g"]

    db.commit()

    return {"message": "Daily nutrition recalculated successfully"}

def calculated_nutrition_info(db: Session, userUuid: int):
    """
        Return all calculated nutrition info and diet restrictions for the user.
    """
    user: User | None = db.query(User).filter(User.uuid == userUuid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return CalculatedNutritionInfoResponse(
        calculatedKcal=user.calculatedKcal,
        calculatedCarbs=user.calculatedCarbs,
        calculatedProtein=user.calculatedProtein,
        calculatedFat=user.calculatedFat,
        calculatedSatFat=user.calculatedSatFat,
        calculatedSugar=user.calculatedSugar,
        calculatedSalt=user.calculatedSalt,
        isVegetarian=user.isVegetarian,
        isVegan=user.isVegan,
        isDairyInt=user.isDairyInt
    )