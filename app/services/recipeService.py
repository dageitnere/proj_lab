from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import os, json
from groq import Groq

from app.models.userMenu import UserMenu
from app.models.recipes import Recipe
from app.models.userMenuRecipes import UserMenuRecipes
from app.schemas.requests.getRecipeRequest import RecipeProductItem
from app.schemas.responses.recipeResponse import GenerateRecipesResponse, RecipeItem

# Initialize Groq client
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY is not set in environment variables")

client = Groq(api_key=groq_api_key)


def call_ai_generate_recipes(products: list[RecipeProductItem]):
    """
    Sends the product list to Groq and returns a list of recipe dicts.
    """
    product_lines = "\n".join([f"{p.productName} ({p.grams}g, {p.kcal} kcal)" for p in products])

    prompt = f"""You are a professional chef and nutritionist. Create a balanced meal plan using ONLY these ingredients:

{product_lines}

Requirements:
1. Generate exactly 3 main meals (breakfast, lunch, dinner) and optionally 1 snack
2. Use ONLY the ingredients listed above, use them fully - do not add any unlisted ingredients, you may add water.
3. Distribute calories appropriately: breakfast (25-30%), lunch (35-40%), dinner (30-35%), snack (5-10%)
4. Each meal must include specific gram amounts from the ingredient list, calories of each meal are calculated from the amount of product used
5. Provide detailed step-by-step cooking instructions with exact times and temperatures
6. Make recipes practical and easy to follow
7. Find a photo that shows the ready food from recipe

Output ONLY valid JSON (no markdown, no code blocks) in this exact format:
[
  {{
    "mealType": "breakfast",
    "name": "Recipe Name",
    "description": "Brief appetizing description (2-3 sentences)",
    "instructions": "Step 1: ... (50g ingredient X)\\nStep 2: ... (3 minutes)\\nStep 3: ...",
    "photoUrl": null,
    "calories": 450
  }}
]"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
        )
        # Groq's API returns a list of choices similar to OpenAI
        text = response.choices[0].message.content
        return json.loads(text)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI recipe generation failed: {str(e)}"
        )


def create_recipes_from_menu(db: Session, user_menu_id: int, products: list[RecipeProductItem]) -> GenerateRecipesResponse:
    """
    Generate recipes from products and save them to DB linked to the user menu.
    """
    if not products:
        return GenerateRecipesResponse(status="Error", message="No products found to generate recipes.")

    menu = db.query(UserMenu).filter(UserMenu.id == user_menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")

    ai_recipes = call_ai_generate_recipes(products)
    response_recipes = []

    for r in ai_recipes:
        recipe = Recipe(
            name=r["name"],
            description=r.get("description"),
            instructions=r["instructions"],
            photoUrl=r.get("photoUrl"),
            calories=r.get("calories")
        )
        db.add(recipe)
        db.flush()  # Ensure recipe.id exists

        link = UserMenuRecipes(
            userMenuId=menu.id,
            recipeId=recipe.id,
            mealType=r.get("mealType", "lunch")
        )
        db.add(link)

        response_recipes.append(
            RecipeItem(
                mealType=r.get("mealType", "lunch"),
                name=r["name"],
                description=r.get("description"),
                instructions=r["instructions"],
                photoUrl=r.get("photoUrl"),
                #TODO izsauc otru AI ar receptes bildi
                calories=r.get("calories")
            )
        )

    db.commit()
    return GenerateRecipesResponse(status="Optimal", recipes=response_recipes)


def get_recipes_by_menu(db: Session, userUuid: int, menuId: int) -> GenerateRecipesResponse:
    """
    Return all recipes for a specific user menu.
    """
    links = db.query(UserMenuRecipes).join(UserMenu).filter(
        UserMenu.id == menuId,
        UserMenu.userUuid == userUuid
    ).all()

    recipes_list = []
    for link in links:
        recipe = db.query(Recipe).filter(Recipe.id == link.recipeId).first()
        if recipe:
            recipes_list.append(
                RecipeItem(
                    mealType=link.mealType,
                    name=recipe.name,
                    description=recipe.description,
                    instructions=recipe.instructions,
                    photoUrl=recipe.photoUrl,
                    calories=recipe.calories
                )
            )

    status_str = "Optimal" if recipes_list else "NoRecipes"
    return GenerateRecipesResponse(
        status=status_str,
        recipes=recipes_list if recipes_list else None,
        message=None if recipes_list else "No recipes found for this menu."
    )
