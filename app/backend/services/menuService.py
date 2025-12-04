from pulp import LpProblem, LpVariable, LpMinimize, lpSum, LpStatus
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional
from datetime import datetime
from app.backend.models.productsProtSep import ProductProtSep
from app.backend.models.userMenus import UserMenu
from app.backend.models.userMenuRecipes import UserMenuRecipes
from app.backend.models.recipes import Recipe
from app.backend.schemas.requests.postDietPlanRequest import PostDietPlanRequest
from app.backend.schemas.requests.deleteUserMenuRequest import DeleteUserMenuRequest
from app.backend.schemas.requests.dietRequest import DietRequest
from app.backend.schemas.requests.getMenuRequest import GetMenuRequest
from app.backend.schemas.responses.dietPlanResponse import DietPlanListResponse, DietPlanResponse
from app.backend.schemas.responses.generateMenuResponse import GenerateMenuResponse, ProductItem
from app.backend.schemas.responses.userMenuNamesResponse import UserMenuNamesResponse
from app.backend.services.userProductService import get_user_products


def normalize(s: str):
    """
    Normalize a string by stripping whitespace and converting to lowercase.
    Used for case-insensitive product name comparison.
    """
    return s.strip().lower()


def make_product_key(p):
    """
    Create a unique key for a product based on its nutritional and cost properties.

    Args:
        p: Product object with nutritional attributes

    Returns:
        Tuple containing all relevant product attributes for comparison
    """
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
    """
    Combine general products from the database with user-specific products.
    Deduplicates products based on their nutritional profile and properties.

    Args:
        db: Database session
        userUuid: User's unique identifier

    Returns:
        List of unique products available for diet planning
    """
    # Fetch all general products from the database
    all_products = db.query(ProductProtSep).all()

    # Fetch products specific to this user
    user_products = get_user_products(db, userUuid)

    # Prefix user product IDs to distinguish them from general products
    for p in user_products:
        p.id = f"user_{p.id}"

    # Combine and deduplicate by full product data (not just name)
    # This ensures products with identical nutritional profiles aren't duplicated
    combined_dict = {}
    for p in all_products + user_products:
        key = make_product_key(p)
        if key not in combined_dict:
            combined_dict[key] = p

    # Return deduplicated list of products
    products = list(combined_dict.values())
    return products


def generate_diet_menu(db: Session, request: DietRequest, userUuid: int):
    """
    Generate an optimized diet menu using linear programming to minimize cost
    while meeting nutritional requirements and dietary preferences.

    Uses PuLP library to solve a linear optimization problem that:
    - Minimizes total cost
    - Meets calorie, protein, fat, carb, sugar, and salt targets (with tolerance ranges)
    - Respects protein source distribution (animal/dairy/plant)
    - Ensures dietary restrictions (vegan, vegetarian, dairy-free)
    - Applies custom product restrictions (min/max weights, exclusions)
    - Requires minimum 15 different products with minimum 50g each

    Args:
        db: Database session
        request: DietRequest object with nutritional targets and preferences
        userUuid: User's unique identifier

    Returns:
        GenerateMenuResponse with optimized product list and nutritional totals,
        or error response if constraints cannot be satisfied
    """
    # Extract nutritional targets from request
    kcalTarget = request.kcal
    proteinTarget = request.protein
    fatTarget = request.fat
    satFatTarget = request.satFat
    carbsTarget = request.carbs
    sugarTarget = request.sugars
    saltTarget = request.salt

    # Extract dietary preferences
    vegan = request.vegan
    vegetarian = request.vegetarian
    dairyFree = request.dairyFree
    restrictions = request.restrictions

    # Validate that vegan diets are also marked as dairy-free
    if vegan and not (dairyFree or vegetarian):
        return {"error": "Vegan diets are always dairy-free — please set dairyFree=True."}

    # Get combined list of all available products
    products = combine_products(db, userUuid)

    if not products:
        return {"error": "No products found in database."}

    # Filter products based on dietary preferences
    if vegan:
        # Vegan users can only have vegan products
        products = [p for p in products if p.vegan]
    elif vegetarian:
        # Vegetarians can have vegetarian or vegan products
        products = [p for p in products if p.vegetarian or p.vegan]

    if dairyFree:
        # Filter out products containing dairy
        products = [p for p in products if p.dairyFree]

    if not products:
        return {"error": "No products match dietary preferences."}

    # Validate that restricted products exist in the filtered product list
    # This prevents optimization failures due to invalid restrictions
    if restrictions:
        # Create lookup set of normalized product names for validation
        valid_product_names = {normalize(str(p.productName)) for p in products}
        invalidProducts = []

        # Check each restriction against available products
        for r in restrictions:
            r_product = normalize(r.get("product", ""))
            if r_product and r_product not in valid_product_names:
                invalidProducts.append(r.get("product", ""))

        # Return error if any restricted products don't exist
        if invalidProducts:
            return GenerateMenuResponse(
                status="InvalidProducts",
                invalidProducts=invalidProducts,
                message=f"The following products were not found in the database: {', '.join(invalidProducts)}"
            )

    # Create linear programming problem to minimize cost
    problem = LpProblem("Balanced_Diet", LpMinimize)

    # Decision variables: grams of each product to include (continuous, ≥ 0)
    x = {p.id: LpVariable(f"x_{p.id}", lowBound=0) for p in products}

    # Binary indicator variables: 1 if product is used, 0 otherwise
    y = {p.id: LpVariable(f"y_{p.id}", cat="Binary") for p in products}

    # Objective function: minimize total cost of all products
    # cost = sum(grams * price_per_100g / 100) for all products
    problem += lpSum([x[p.id] * p.price100g / 100 for p in products])

    # Define protein source distribution targets
    # For balanced nutrition, aim for 40% animal, 30% dairy, 30% plant protein
    if vegan:
        animal_target = 0
        dairy_target = 0
        plant_target = proteinTarget
    elif vegetarian:
        animal_target = 0
        dairy_target = 0.6 * proteinTarget
        plant_target = 0.4 * proteinTarget
    elif dairyFree:
        dairy_target = 0
        animal_target = 0.6 * proteinTarget
        plant_target = 0.4 * proteinTarget
    else:
        # Omnivore default split
        animal_target = 0.4 * proteinTarget
        dairy_target = 0.3 * proteinTarget
        plant_target = 0.3 * proteinTarget

    # === NUTRITIONAL CONSTRAINTS ===
    # Each constraint has min/max bounds with tolerance ranges

    # Calorie constraints (90-130% of target)
    problem += lpSum([x[p.id] * p.kcal / 100 for p in products]) >= kcalTarget * 0.9, "caloriesMin"
    problem += lpSum([x[p.id] * p.kcal / 100 for p in products]) <= kcalTarget * 1.3, "caloriesMax"

    # Total protein constraints (90-160% of target)
    problem += lpSum([x[p.id] * p.protein / 100 for p in products]) >= proteinTarget * 0.9
    problem += lpSum([x[p.id] * p.protein / 100 for p in products]) <= proteinTarget * 1.6

    # Protein source distribution constraints (conditional based on diet type)
    if animal_target > 0:
        # Omnivore: enforce animal protein requirements (70-110% of target)
        problem += lpSum([x[p.id] * (p.animalProt or 0) / 100 for p in products]) >= animal_target * 0.7
        problem += lpSum([x[p.id] * (p.animalProt or 0) / 100 for p in products]) <= animal_target * 1.1

    if dairy_target > 0:
        # Dairy allowed: enforce dairy protein requirements (70-110% of target)
        problem += lpSum([x[p.id] * (p.dairyProt or 0) / 100 for p in products]) >= dairy_target * 0.7
        problem += lpSum([x[p.id] * (p.dairyProt or 0) / 100 for p in products]) <= dairy_target * 1.1

    # Plant protein constraints apply to all diets (70-110% of target)
    problem += lpSum([x[p.id] * (p.plantProt or 0) / 100 for p in products]) >= plant_target * 0.7
    problem += lpSum([x[p.id] * (p.plantProt or 0) / 100 for p in products]) <= plant_target * 1.1

    # Fat constraints (60-110% of target)
    problem += lpSum([x[p.id] * p.fat / 100 for p in products]) >= fatTarget * 0.6, "fatMin"
    problem += lpSum([x[p.id] * p.fat / 100 for p in products]) <= fatTarget * 1.1, "fatMax"

    # Carbohydrate constraints (60-110% of target)
    problem += lpSum([x[p.id] * p.carbs / 100 for p in products]) >= carbsTarget * 0.6, "carbsMin"
    problem += lpSum([x[p.id] * p.carbs / 100 for p in products]) <= carbsTarget * 1.1, "carbsMax"

    # Sugar constraints (60-110% of target)
    problem += lpSum([x[p.id] * p.sugars / 100 for p in products]) >= sugarTarget * 0.6, "sugarsMin"
    problem += lpSum([x[p.id] * p.sugars / 100 for p in products]) <= sugarTarget * 1.1, "sugarsMax"

    # Saturated fat constraints (60-110% of target)
    problem += lpSum([x[p.id] * p.satFat / 100 for p in products]) >= satFatTarget * 0.6, "saturatedFatMin"
    problem += lpSum([x[p.id] * p.satFat / 100 for p in products]) <= satFatTarget * 1.1, "saturatedFatMax"

    # Salt constraints (60-110% of target)
    problem += lpSum([x[p.id] * p.salt / 100 for p in products]) >= saltTarget * 0.6, "saltMin"
    problem += lpSum([x[p.id] * p.salt / 100 for p in products]) <= saltTarget * 1.1, "saltMax"

    # === BIG-M CONSTRAINTS ===
    # Link continuous variable x (grams) with binary variable y (used/not used)
    M = 400  # Maximum grams per product (upper bound)
    m = 50  # Minimum grams if product is used (ensures meaningful portions)

    for p in products:
        # If product is not used (y=0), then x must be 0
        # If product is used (y=1), then x can be up to M grams
        problem += x[p.id] <= M * y[p.id], f"MaxLink_{p.id}"

        # If product is used (y=1), then x must be at least m grams
        # This ensures we don't include tiny amounts of products
        problem += x[p.id] >= m * y[p.id], f"MinLink_{p.id}"

    # Require at least 15 different products for diet variety
    problem += lpSum([y[p.id] for p in products]) >= 10, "Min_15_Products"

    # Apply user-defined custom restrictions (already validated above)
    if restrictions:
        for r in restrictions:
            r_type = r.get("type")
            r_product = normalize(r.get("product", ""))
            r_value = r.get("value", None)

            # Find matching product and apply restriction
            for p in products:
                name = normalize(p.productName)
                if name == r_product:
                    if r_type == "max_weight" and r_value is not None:
                        # Limit maximum grams for this product
                        problem += x[p.id] <= r_value, f"Limit_{p.id}"
                    elif r_type == "min_weight" and r_value is not None:
                        # Require minimum grams for this product
                        problem += x[p.id] >= r_value, f"Min_{p.id}"
                    elif r_type == "exclude":
                        # Completely exclude this product from the diet
                        problem += x[p.id] == 0, f"Exclude_{p.id}"
                        problem += y[p.id] == 0, f"Exclude_y_{p.id}"

    # Solve the optimization problem
    problem.solve()

    # Check if an optimal solution was found
    if LpStatus[problem.status] != "Optimal":
        return GenerateMenuResponse(
            status=LpStatus[problem.status],
            message="No optimal solution found.",
            plan=[]
        )

    # Extract solution: build list of products with non-zero quantities
    result = []
    for p in products:
        grams = x[p.id].varValue
        if grams and grams > 0:
            # Calculate nutritional values based on selected grams
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

    # Calculate total nutritional values across all selected products
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

    # Return successful response with optimized menu
    return GenerateMenuResponse(status="Optimal", plan=result, **totals)


def save_diet_menu(db: Session, request: PostDietPlanRequest, userUuid: int):
    """
    Save a generated diet menu to the database and automatically create recipes.
    Args:
        db: Database session
        request: PostDietPlanRequest containing menu name, products, and totals
        userUuid: User's unique identifier
    Returns:
        Success message dict
    Raises:
        HTTPException: If a menu with the same name already exists for this user
    """
    # Create new menu record with all nutritional totals
    new_plan = UserMenu(
        userUuid=userUuid,
        name=request.name.strip().title(), # Normalize name (strip whitespace, title case)
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
        plan=[p.model_dump() for p in request.plan], # Convert Pydantic models to dicts
        vegan=request.vegan,
        vegetarian=request.vegetarian,
        dairyFree=request.dairyFree,
        restrictions=request.restrictions
    )

    existing = (
        db.query(UserMenu)
        .filter(UserMenu.userUuid == userUuid)
        .filter(UserMenu.name.ilike(request.name.strip()))
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Menu '{request.name}' already exists in your list - choose different name."
        )
    # Save menu to database
    db.add(new_plan)
    db.commit()
    # db.refresh(new_plan) # Refresh to get the auto-generated ID
    # Note: Recipes are NOT automatically generated here to avoid timeout issues.
    # Users can generate recipes manually using the "Regenerate Recipes" button
    # in the menu detail view, which calls the /recipes/regenerate endpoint.
    return {"message": "Diet plan saved successfully. Use 'Regenerate Recipes' button to create recipes."}

def get_user_menus_names(db: Session, userUuid: int) -> UserMenuNamesResponse:
    """
    Retrieve the names of all saved diet menus for a specific user.

    Args:
        db: Database session
        userUuid: User's unique identifier

    Returns:
        UserMenuNamesResponse: A response object containing a list of menu names.
    """
    menus = db.query(UserMenu.name).filter(UserMenu.userUuid == int(userUuid)).all()

    menu_names = [menu.name for menu in menus]

    return UserMenuNamesResponse(menus=menu_names)

def get_user_menus(db: Session, userUuid: int) -> DietPlanListResponse:
    """
    Retrieve all saved diet menus for a specific user.

    Args:
        db: Database session
        userUuid: User's unique identifier

    Returns:
        List of DietPlanResponse objects containing all menu details

    Raises:
        HTTPException: If no menus are found for the user
    """
    # Query all menus for this user
    menus = db.query(UserMenu).filter(UserMenu.userUuid == int(userUuid)).all()

    # Convert database models to response objects
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
                plan=menu.plan,  # JSON stored in DB is automatically deserialized
                vegan=menu.vegan,
                vegetarian=menu.vegetarian,
                dairyFree=menu.dairyFree,
                restrictions=menu.restrictions
            )
        )

    # Return 404 if user has no saved menus
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No diet menus found for this user."
        )
    return response


def get_single_menu(db: Session, request: GetMenuRequest, userUuid: int) -> Optional[DietPlanResponse]:
    """
    Retrieve a specific diet menu by name for a user.
    Args:
        db: Database session
        request: GetMenuRequest containing the menu name
        userUuid: User's unique identifier
    Returns:
        DietPlanResponse object with menu details
    Raises:
        HTTPException: If menu is not found
    """
    # Query for menu by name and user
    menu = db.query(UserMenu).filter(
        UserMenu.name == request.menuName
    ).filter(
        UserMenu.userUuid == userUuid
    ).first()
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No diet menu found with '{request.menuName}' name."
        )
    # Convert database model to response object
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
        plan=menu.plan,
        vegan=menu.vegan,
        vegetarian=menu.vegetarian,
        dairyFree=menu.dairyFree,
        restrictions=menu.restrictions or []
    )


def delete_user_menu(db: Session, request: DeleteUserMenuRequest, userUuid: int):
    """
    Delete a user's diet menu and clean up associated recipes.

    This function:
    1. Finds and deletes the specified menu
    2. Removes links between the menu and its recipes
    3. Deletes recipes that are no longer linked to any menu (orphaned recipes)

    Args:
        db: Database session
        request: DeleteUserMenuRequest containing the menu name
        userUuid: User's unique identifier

    Returns:
        Success message dict

    Raises:
        HTTPException: If menu is not found
    """
    # Find menu by name and user (case-insensitive)
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

    # Get all recipe IDs linked to this menu before deletion
    linked_recipe_ids = [
        link.recipeId
        for link in db.query(UserMenuRecipes).filter(UserMenuRecipes.userMenuId == menu.id).all()
    ]

    # Delete all menu-recipe links for this menu
    db.query(UserMenuRecipes).filter(UserMenuRecipes.userMenuId == menu.id).delete()

    # Delete the menu itself
    db.delete(menu)
    db.commit()

    # Clean up orphaned recipes (recipes not linked to any other menu)
    for recipe_id in linked_recipe_ids:
        # Check if this recipe is still linked to other menus
        still_used = (
            db.query(UserMenuRecipes)
            .filter(UserMenuRecipes.recipeId == recipe_id)
            .count()
        )
        # If recipe is orphaned, delete it
        if still_used == 0:
            db.query(Recipe).filter(Recipe.id == recipe_id).delete()

    db.commit()

    return {"message": f"Menu '{request.menuName}' and unused recipes deleted successfully."}