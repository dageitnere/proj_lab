from pulp import LpProblem, LpVariable, LpMinimize, lpSum, LpStatus
from sqlalchemy.orm import Session
from app.models.productsProtSep import ProductProtSep
from app.models.userMenu import UserMenu
from app.schemas.requests.addDietPlanRequest import AddDietPlanRequest
from app.schemas.requests.deleteUserMenuRequest import DeleteUserMenuRequest
from app.schemas.requests.dietRequest import DietRequest
from app.schemas.requests.getMenuRequest import GetMenuRequest
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
        round(p.fat or 0, 2),
        round(p.satFat or 0, 2),
        round(p.carbs or 0, 2),
        round(p.sugars or 0, 2),
        round(p.protein or 0, 2),
        round(p.salt or 0, 2),
        round(p.price1kg or 0, 2),
        getattr(p, "vegan", False),
        getattr(p, "vegetarian", False),
        getattr(p, "dairyFree", False),
    )

def combine_products(db: Session, userUuid: int):
    # 1. Fetch all general products
    all_products = db.query(ProductProtSep).all()

    # 2. Fetch user's products
    user_products = get_user_products(db, userUuid)

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

def generate_diet_menu(db: Session, request: DietRequest, userUuid: int):

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

    products = combine_products(db, userUuid)

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
        valid_product_names = {normalize(str(p.productName)) for p in products}
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
    problem += lpSum([x[p.id] * p.price100g / 100 for p in products])

    # Protein source targets
    animal_target = 0.4 * proteinTarget
    dairy_target = 0.3 * proteinTarget
    plant_target = 0.3 * proteinTarget

    # 5. Nutritional constraints
    problem += lpSum([x[p.id] * p.kcal / 100 for p in products]) >= kcalTarget * 0.9, "caloriesMin"
    problem += lpSum([x[p.id] * p.kcal / 100 for p in products]) <= kcalTarget * 1.3, "caloriesMax"

    problem += lpSum([x[p.id] * p.protein / 100 for p in products]) >= proteinTarget * 0.9
    problem += lpSum([x[p.id] * p.protein / 100 for p in products]) <= proteinTarget * 1.6

    # Protein source constraints (conditional)
    if not vegan and not vegetarian:
        # Omnivore
        problem += lpSum([x[p.id] * (p.animalProt or 0) / 100 for p in products]) >= animal_target * 0.7
        problem += lpSum([x[p.id] * (p.animalProt or 0) / 100 for p in products]) <= animal_target * 1.1

    if not vegan and not dairyFree:
        # Dairy allowed
        problem += lpSum([x[p.id] * (p.dairyProt or 0) / 100 for p in products]) >= dairy_target * 0.7
        problem += lpSum([x[p.id] * (p.dairyProt or 0) / 100 for p in products]) <= dairy_target * 1.1

    # Always include plant protein constraints (everyone can eat plants)
    problem += lpSum([x[p.id] * (p.plantProt or 0) / 100 for p in products]) >= plant_target * 0.7
    problem += lpSum([x[p.id] * (p.plantProt or 0) / 100 for p in products]) <= plant_target * 1.1


    problem += lpSum([x[p.id] * p.fat / 100 for p in products]) >= fatTarget * 0.6, "fatMin"
    problem += lpSum([x[p.id] * p.fat / 100 for p in products]) <= fatTarget * 1.1, "fatMax"
    problem += lpSum([x[p.id] * p.carbs / 100 for p in products]) >= carbsTarget * 0.6, "carbsMin"
    problem += lpSum([x[p.id] * p.carbs / 100 for p in products]) <= carbsTarget * 1.1, "carbsMax"
    problem += lpSum([x[p.id] * p.sugars / 100 for p in products]) >= sugarTarget * 0.6, "sugarsMin"
    problem += lpSum([x[p.id] * p.sugars / 100 for p in products]) <= sugarTarget * 1.1, "sugarsMax"
    problem += lpSum([x[p.id] * p.satFat / 100 for p in products]) >= satFatTarget * 0.6, "saturatedFatMin"
    problem += lpSum([x[p.id] * p.satFat / 100 for p in products]) <= satFatTarget * 1.1, "saturatedFatMax"
    problem += lpSum([x[p.id] * p.salt / 100 for p in products]) >= saltTarget * 0.6, "saltMin"
    problem += lpSum([x[p.id] * p.salt / 100 for p in products]) <= saltTarget * 1.1, "saltMax"


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
                productName=str(p.productName),
                grams=round(grams, 1),
                kcal=round(p.kcal * grams / 100, 1),
                cost=round(p.price100g * grams / 100, 2),
                fat=round(p.fat * grams / 100, 1),
                satFat=round(p.satFat * grams / 100, 1),
                carbs=round(p.carbs * grams / 100, 1),
                protein=round(p.protein * grams / 100, 1),
                dairyProtein=round((p.dairyProt or 0) * grams / 100, 1),
                animalProtein=round((p.animalProt or 0) * grams / 100, 1),
                plantProtein=round((p.plantProt or 0) * grams / 100, 1),
                sugars=round(p.sugars * grams / 100, 1),
                salt=round(p.salt * grams / 100, 1)
            ))

    totals = {
        "totalKcal": round(sum(r.kcal for r in result), 1),
        "totalCost": round(sum(r.cost for r in result), 2),
        "totalFat": round(sum(r.fat for r in result), 1),
        "totalSatFat": round(sum(r.satFat for r in result), 1),
        "totalCarbs": round(sum(r.carbs for r in result), 1),
        "totalProtein": round(sum(r.protein for r in result), 1),
        "totalDairyProtein": round(sum(r.dairyProtein for r in result), 1),
        "totalAnimalProtein": round(sum(r.animalProtein for r in result), 1),
        "totalPlantProtein": round(sum(r.plantProtein for r in result), 1),
        "totalSugar": round(sum(r.sugars for r in result), 1),
        "totalSalt": round(sum(r.salt for r in result), 1)
    }

    return GenerateMenuResponse(status="Optimal", plan=result, **totals)


def save_diet_menu(db: Session, request: AddDietPlanRequest, userUuid: int):
    new_plan = UserMenu(
        userUuid=userUuid,
        name=request.name,  # <-- Save plan name
        totalKcal=request.totalKcal,
        totalCost=request.totalCost,
        totalFat=request.totalFat,
        totalCarbs=request.totalCarbs,
        totalProtein=request.totalProtein,
        totalDairyProtein=request.totalDairyProtein,
        totalAnimalProtein=request.totalAnimalProtein,
        totalPlantProtein=request.totalPlantProtein,
        totalSugar=request.totalSugar,
        totalSatFat=request.totalSatFat,
        totalSalt=request.totalSalt,
        date=datetime.now(),
        plan=[p.model_dump() for p in request.plan]
    )

    existing = (
        db.query(UserMenu)
        .filter(UserMenu.userUuid == userUuid)  # optional, check only this user's menus
        .filter(UserMenu.name.ilike(request.name.strip()))  # <-- strip the input string, not the column
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Menu '{request.name}' already exists in your list - choose different name."
        )

    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)
    return "Diet plan saved successfully."


def get_user_menus(db: Session, userUuid: int) -> DietPlanListResponse:
    """
    Retrieve all diet menus for a given user.
    """
    menus = db.query(UserMenu).filter(UserMenu.userUuid == int(userUuid)).all()

    response: DietPlanListResponse = []
    for menu in menus:
        response.append(
            DietPlanResponse(
                id=str(menu.id),
                userUuid=str(menu.userUuid),
                name=str(menu.name),
                totalKcal=menu.totalKcal,
                totalCost=menu.totalCost,
                totalFat=menu.totalFat,
                totalCarbs=menu.totalCarbs,
                totalProtein=menu.totalProtein,
                totalDairyProtein=menu.totalDairyProtein,
                totalAnimalProtein=menu.totalAnimalProtein,
                totalPlantProtein=menu.totalPlantProtein,
                totalSugar=menu.totalSugar,
                totalSatFat=menu.totalSatFat,
                totalSalt=menu.totalSalt,
                date=menu.date,
                plan=menu.plan  # JSON -> List[ProductItem]
            )
        )
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No diet menus found for this user."
        )
    return response


def get_single_menu(db: Session, request: GetMenuRequest, userUuid: int) -> Optional[DietPlanResponse]:
    menu = db.query(UserMenu).filter(UserMenu.name == request.menuName).filter(UserMenu.userUuid == userUuid).first()
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No diet menu found with '{request.menuName}' name."
        )
    return DietPlanResponse(
        id=str(menu.id),
        userUuid=str(menu.userUuid),
        name=menu.name,
        totalKcal=menu.totalKcal,
        totalCost=menu.totalCost,
        totalFat=menu.totalFat,
        totalCarbs=menu.totalCarbs,
        totalProtein=menu.totalProtein,
        totalDairyProtein=menu.totalDairyProtein,
        totalAnimalProtein=menu.totalAnimalProtein,
        totalPlantProtein=menu.totalPlantProtein,
        totalSugar=menu.totalSugar,
        totalSatFat=menu.totalSatFat,
        totalSalt=menu.totalSalt,
        date=menu.date,
        plan=menu.plan

    )

def delete_user_menu(db: Session, request: DeleteUserMenuRequest, userUuid: int):
    """
    Deletes a specific user menu by userUuid and menuName.
    """
    # Find the menu
    menu = (
        db.query(UserMenu)
        .filter(UserMenu.userUuid == userUuid)
        .filter(UserMenu.name.ilike(request.menuName.strip()))
        .first()
    )

    if not menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No menu found with name '{request.menuName}' for this user."
        )

    # Delete the menu
    db.delete(menu)
    db.commit()

    return {"message": f"Menu '{request.menuName}' deleted successfully."}