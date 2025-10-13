from pulp import LpProblem, LpVariable, LpMinimize, lpSum, LpStatus
from sqlalchemy.orm import Session
from app.models.productsProtSep import ProductProtSep
from app.models.userMenu import UserMenu
from app.schemas.requests.dietPlanSaveRequest import DietPlanSaveRequest
from app.schemas.responses.dietPlanResponse import DietPlanListResponse, DietPlanResponse
from app.schemas.responses.generateMenuResponse import GenerateMenuResponse, ProductItem
from app.services.userProductService import get_user_products
from fastapi import HTTPException, status
from typing import Optional
from datetime import datetime

def normalize(s: str):
    return s.strip().lower()

def make_product_key(p):
    # Key based on all distinguishing attributes
    # Convert floats to rounded values for stable comparison
    return (
        p.id,
        round(p.kcal or 0, 2),
        round(p.tauki or 0, 2),
        round(p.piesatTauki or 0, 2),
        round(p.oglh or 0, 2),
        round(p.cukuri or 0, 2),
        round(p.olbv or 0, 2),
        round(p.sals or 0, 2),
        round(p.cena1kg or 0, 2),
        getattr(p, "vegan", False),
        getattr(p, "vegetarian", False),
        getattr(p, "dairyFree", False),
    )

def combine_products(db: Session, request):
    # 1. Fetch all general products
    all_products = db.query(ProductProtSep).all()

    # 2. Fetch user's products
    user_products = get_user_products(db, request.userUuid)

    for p in user_products:
        p.id = f"user_{p.id}"

    # 3. Combine and deduplicate by full product data (not just name)
    combined_dict = {}
    for p in all_products + user_products:
        key = make_product_key(p)
        if key not in combined_dict:
            combined_dict[key] = p

    # 4. Result list
    products = list(combined_dict.values())
    return products

def generate_diet_menu(db: Session, request):

    # Unpack directly from request object
    kcalTarget = request.kcal
    proteinTarget = request.protein
    fatTarget = request.fat
    satFatTarget = request.satFat
    carbsTarget = request.carbs
    sugarTarget = request.sugars
    saltTarget = request.salt
    vegan = request.vegan
    vegetarian = request.vegetarian
    dairyFree = request.dairyFree
    restrictions = request.restrictions


    if vegan and not dairyFree:
        return {"error": "Vegan diets are always dairy-free — please set dairyFree=True."}

    products = combine_products(db, request)

    if not products:
        return {"error": "No products found in database."}

    # 1.1 Filter based on user preferences
    if vegan:
        products = [p for p in products if p.vegan]
    elif vegetarian:
        products = [p for p in products if p.vegetarian or p.vegan]

    if dairyFree:
        products = [p for p in products if p.dairyFree]

    if not products:
        return {"error": "No products match dietary preferences."}

    # 1.2 Validate restrictions BEFORE creating the optimization problem
    if restrictions:
        # Create a set of normalized product names for fast lookup
        valid_product_names = {normalize(str(p.produkts)) for p in products}
        invalidProducts = []

        for r in restrictions:
            r_product = normalize(r.get("product", ""))
            if r_product and r_product not in valid_product_names:
                invalidProducts.append(r.get("product", ""))

        if invalidProducts:
            return GenerateMenuResponse(
                status="InvalidProducts",
                invalidProducts=invalidProducts,
                message=f"The following products were not found in the database: {', '.join(invalidProducts)}"
            )

    # 2. Create PuLP problem
    problem = LpProblem("Balanced_Diet", LpMinimize)

    # 3. Decision variables (grams of each product)
    x = {p.id: LpVariable(f"x_{p.id}", lowBound=0) for p in products}

    # Binary indicator variables (1 if product is used)
    y = {p.id: LpVariable(f"y_{p.id}", cat="Binary") for p in products}

    # 4. Objective: minimize total cost
    problem += lpSum([x[p.id] * p.cena100g / 100 for p in products])

    # Protein source targets
    animal_target = 0.4 * proteinTarget
    dairy_target = 0.3 * proteinTarget
    plant_target = 0.3 * proteinTarget

    # 5. Nutritional constraints
    problem += lpSum([x[p.id] * p.kcal / 100 for p in products]) >= kcalTarget * 0.9, "caloriesMin"
    problem += lpSum([x[p.id] * p.kcal / 100 for p in products]) <= kcalTarget * 1.3, "caloriesMax"

    problem += lpSum([x[p.id] * p.olbv / 100 for p in products]) >= proteinTarget * 0.9
    problem += lpSum([x[p.id] * p.olbv / 100 for p in products]) <= proteinTarget * 1.6

    # Protein source constraints (conditional)
    if not vegan and not vegetarian:
        # Omnivore
        problem += lpSum([x[p.id] * (p.dzivOlbv or 0) / 100 for p in products]) >= animal_target * 0.7
        problem += lpSum([x[p.id] * (p.dzivOlbv or 0) / 100 for p in products]) <= animal_target * 1.1

    if not vegan and not dairyFree:
        # Dairy allowed
        problem += lpSum([x[p.id] * (p.pienaOlbv or 0) / 100 for p in products]) >= dairy_target * 0.7
        problem += lpSum([x[p.id] * (p.pienaOlbv or 0) / 100 for p in products]) <= dairy_target * 1.1

    # Always include plant protein constraints (everyone can eat plants)
    problem += lpSum([x[p.id] * (p.auguOlbv or 0) / 100 for p in products]) >= plant_target * 0.7
    problem += lpSum([x[p.id] * (p.auguOlbv or 0) / 100 for p in products]) <= plant_target * 1.1


    problem += lpSum([x[p.id] * p.tauki / 100 for p in products]) >= fatTarget * 0.6, "fatMin"
    problem += lpSum([x[p.id] * p.tauki / 100 for p in products]) <= fatTarget * 1.1, "fatMax"
    problem += lpSum([x[p.id] * p.oglh / 100 for p in products]) >= carbsTarget * 0.6, "carbsMin"
    problem += lpSum([x[p.id] * p.oglh / 100 for p in products]) <= carbsTarget * 1.1, "carbsMax"
    problem += lpSum([x[p.id] * p.cukuri / 100 for p in products]) >= sugarTarget * 0.6, "sugarsMin"
    problem += lpSum([x[p.id] * p.cukuri / 100 for p in products]) <= sugarTarget * 1.1, "sugarsMax"
    problem += lpSum([x[p.id] * p.piesatTauki / 100 for p in products]) >= satFatTarget * 0.6, "saturatedFatMin"
    problem += lpSum([x[p.id] * p.piesatTauki / 100 for p in products]) <= satFatTarget * 1.1, "saturatedFatMax"
    problem += lpSum([x[p.id] * p.sals / 100 for p in products]) >= saltTarget * 0.6, "saltMin"
    problem += lpSum([x[p.id] * p.sals / 100 for p in products]) <= saltTarget * 1.1, "saltMax"


    # Big-M constraint: link x and y
    M = 400  # max grams per product
    m = 50  # min grams if product is used
    for p in products:
        problem += x[p.id] <= M * y[p.id], f"MaxLink_{p.id}"
        problem += x[p.id] >= m * y[p.id], f"MinLink_{p.id}"

    # Require at least 15 different products
    problem += lpSum([y[p.id] for p in products]) >= 15, "Min_15_Products"

    # 7. Apply custom restrictions (we already validated these exist)
    if restrictions:
        for r in restrictions:
            r_type = r.get("type")
            r_product = normalize(r.get("product", ""))
            r_value = r.get("value", None)

            for p in products:
                name = p.id
                if name == r_product:
                    if r_type == "max_weight" and r_value is not None:
                        problem += x[p.id] <= r_value, f"Limit_{p.id}"
                    elif r_type == "min_weight" and r_value is not None:
                        problem += x[p.id] >= r_value, f"Min_{p.id}"
                    elif r_type == "exclude":
                        problem += x[p.id] == 0, f"Exclude_{p.id}"
                        problem += y[p.id] == 0, f"Exclude_y_{p.id}"

    # 8. Solve problem
    problem.solve()

    if LpStatus[problem.status] != "Optimal":
        return GenerateMenuResponse(status=LpStatus[problem.status], message="No optimal solution found.", plan=[])

    result = []
    for p in products:
        grams = x[p.id].varValue
        if grams and grams > 0:
            result.append(ProductItem(
                product=str(p.produkts),
                grams=round(grams, 1),
                kcal=round(p.kcal * grams / 100, 1),
                cost=round(p.cena100g * grams / 100, 2),
                fat=round(p.tauki * grams / 100, 1),
                carbs=round(p.oglh * grams / 100, 1),
                protein=round(p.olbv * grams / 100, 1),
                dairyProtein=round((p.pienaOlbv or 0) * grams / 100, 1),
                animalProtein=round((p.dzivOlbv or 0) * grams / 100, 1),
                plantProtein=round((p.auguOlbv or 0) * grams / 100, 1),
                sugar=round(p.cukuri * grams / 100, 1),
                sat_fat=round(p.piesatTauki * grams / 100, 1),
                salt=round(p.sals * grams / 100, 1)
            ))

    totals = {
        "totalKcal": round(sum(r.kcal for r in result), 1),
        "totalCost": round(sum(r.cost for r in result), 2),
        "totalFat": round(sum(r.fat for r in result), 1),
        "totalCarbs": round(sum(r.carbs for r in result), 1),
        "totalProtein": round(sum(r.protein for r in result), 1),
        "totalDairyProtein": round(sum(r.dairyProtein for r in result), 1),
        "totalAnimalProtein": round(sum(r.animalProtein for r in result), 1),
        "totalPlantProtein": round(sum(r.plantProtein for r in result), 1),
        "totalSugar": round(sum(r.sugar for r in result), 1),
        "totalSatFat": round(sum(r.sat_fat for r in result), 1),
        "totalSalt": round(sum(r.salt for r in result), 1)
    }

    return GenerateMenuResponse(status="Optimal", plan=result, **totals)


def save_diet_menu(db: Session, plan_data: DietPlanSaveRequest):
    new_plan = UserMenu(
        userUuid=plan_data.userUuid,
        name=plan_data.name,  # <-- Save plan name
        totalKcal=plan_data.totalKcal,
        totalCost=plan_data.totalCost,
        totalFat=plan_data.totalFat,
        totalCarbs=plan_data.totalCarbs,
        totalProtein=plan_data.totalProtein,
        totalDairyProtein=plan_data.totalDairyProtein,
        totalAnimalProtein=plan_data.totalAnimalProtein,
        totalPlantProtein=plan_data.totalPlantProtein,
        totalSugar=plan_data.totalSugar,
        totalSatFat=plan_data.totalSatFat,
        totalSalt=plan_data.totalSalt,
        date=datetime.now(),
        plan=[p.model_dump() for p in plan_data.plan]
    )

    existing = (
        db.query(UserMenu)
        .filter(UserMenu.userUuid == plan_data.userUuid)  # optional, check only this user's menus
        .filter(UserMenu.name.ilike(plan_data.name.strip()))  # <-- strip the input string, not the column
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Menu '{plan_data.name}' already exists in your list - choose different name."
        )

    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)
    return "Diet plan saved successfully."


def get_user_menus(db: Session, user_uuid: int) -> DietPlanListResponse:
    """
    Retrieve all diet plans for a given user.
    """
    plans = db.query(UserMenu).filter(UserMenu.userUuid == int(user_uuid)).all()

    response: DietPlanListResponse = []
    for plan in plans:
        response.append(
            DietPlanResponse(
                id=str(plan.id),
                userUuid=str(plan.userUuid),
                name=str(plan.name),
                totalKcal=plan.totalKcal,
                totalCost=plan.totalCost,
                totalFat=plan.totalFat,
                totalCarbs=plan.totalCarbs,
                totalProtein=plan.totalProtein,
                totalDairyProtein=plan.totalDairyProtein,
                totalAnimalProtein=plan.totalAnimalProtein,
                totalPlantProtein=plan.totalPlantProtein,
                totalSugar=plan.totalSugar,
                totalSatFat=plan.totalSatFat,
                totalSalt=plan.totalSalt,
                date=plan.date,
                plan=plan.plan  # JSON -> List[ProductItem]
            )
        )
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No diet plans found for this user."
        )
    return response


def get_single_menu(db: Session, menuName: str) -> Optional[DietPlanResponse]:
    plan = db.query(UserMenu).filter(UserMenu.name == menuName).first()
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No diet plan found with '{menuName}' name."
        )
    return DietPlanResponse(
        id=str(plan.id),
        userUuid=str(plan.userUuid),
        name=plan.name,
        totalKcal=plan.totalKcal,
        totalCost=plan.totalCost,
        totalFat=plan.totalFat,
        totalCarbs=plan.totalCarbs,
        totalProtein=plan.totalProtein,
        totalDairyProtein=plan.totalDairyProtein,
        totalAnimalProtein=plan.totalAnimalProtein,
        totalPlantProtein=plan.totalPlantProtein,
        totalSugar=plan.totalSugar,
        totalSatFat=plan.totalSatFat,
        totalSalt=plan.totalSalt,
        date=plan.date,
        plan=plan.plan

    )