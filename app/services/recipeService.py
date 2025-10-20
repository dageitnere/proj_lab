from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import os, json, requests, base64
from groq import Groq

from app.models.userMenus import UserMenu
from app.models.recipes import Recipe
from app.models.userMenuRecipes import UserMenuRecipes
from app.schemas.requests.getRecipeRequest import RecipeProductItem
from app.schemas.responses.recipeResponse import GenerateRecipesResponse, RecipeItem

# ---------------- Initialize AI Clients ----------------
# Groq client
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY is not set in environment variables")
client = Groq(api_key=groq_api_key)

# Stability AI SDXL configuration
SDXL_API_KEY = os.getenv("STABILITY_API_KEY")
SDXL_API_HOST = os.getenv("API_HOST", "https://api.stability.ai")
SDXL_ENGINE_ID = "stable-diffusion-xl-1024-v1-0"

if not SDXL_API_KEY:
    raise ValueError("STABILITY_API_KEY is not set in environment variables")

# ---------------- AI Recipe Generation ----------------
def call_ai_generate_recipes(products: list[RecipeProductItem]):
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
    "photoBase64": null,
    "calories": 450
  }}
]"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.choices[0].message.content
        return json.loads(text)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI recipe generation failed: {str(e)}"
        )

# ---------------- Stability AI Image Generation ----------------
def generate_sdxl_image_base64(prompt: str, width=1024, height=1024, steps=30, cfg_scale=7, samples=1, retries=2) -> str:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {SDXL_API_KEY}"
    }

    payload = {
        "text_prompts": [{"text": prompt}],
        "cfg_scale": cfg_scale,
        "width": width,
        "height": height,
        "samples": samples,
        "steps": steps
    }

    last_error = None
    for attempt in range(retries):
        try:
            response = requests.post(
                f"{SDXL_API_HOST}/v1/generation/{SDXL_ENGINE_ID}/text-to-image",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            artifacts = data.get("artifacts", [])
            if not artifacts:
                last_error = f"No artifacts returned: {data}"
                continue
            artifact = artifacts[0]
            if artifact.get("finishReason") != "SUCCESS":
                last_error = f"Image generation not successful: {artifact.get('finishReason')}"
                continue
            img_base64 = artifact.get("base64")
            if not img_base64:
                last_error = "No base64 image found in artifact."
                continue
            return img_base64
        except Exception as e:
            last_error = str(e)

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Failed to generate image via SDXL: {last_error}"
    )

# ---------------- Create Recipes ----------------
def create_recipes_from_menu(db: Session, user_menu_id: int, products: list[RecipeProductItem]) -> GenerateRecipesResponse:
    if not products:
        return GenerateRecipesResponse(status="Error", message="No products found to generate recipes.")

    menu = db.query(UserMenu).filter(UserMenu.id == user_menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")

    ai_recipes = call_ai_generate_recipes(products)
    response_recipes = []

    for r in ai_recipes:
        image_prompt = f"{r['name']}: {r.get('description', '')} - appetizing food, realistic, vibrant"
        try:
            photo_base64 = generate_sdxl_image_base64(image_prompt)
        except HTTPException as e:
            raise HTTPException(
                status_code=500,
                detail=f"Cannot generate image for recipe '{r['name']}': {e.detail}"
            )

        recipe = Recipe(
            name=r["name"],
            description=r.get("description"),
            instructions=r["instructions"],
            pictureBase64=photo_base64,  # store full base64
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
                pictureBase64=photo_base64,
                calories=r.get("calories")
            )
        )

    db.commit()
    return GenerateRecipesResponse(status="Optimal", recipes=response_recipes)

# ---------------- Get Recipes ----------------
def get_recipes_by_menu(db: Session, userUuid: int, menuId: int) -> GenerateRecipesResponse:
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
                    pictureBase64=recipe.pictureBase64,  # full 1024x1024 base64
                    calories=recipe.calories
                )
            )

    status_str = "Optimal" if recipes_list else "NoRecipes"
    return GenerateRecipesResponse(
        status=status_str,
        recipes=recipes_list if recipes_list else None,
        message=None if recipes_list else "No recipes found for this menu."
    )
