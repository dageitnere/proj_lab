from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import os, json, requests
from groq import Groq
from app.backend.models.userMenus import UserMenu
from app.backend.models.recipes import Recipe
from app.backend.models.userMenuRecipes import UserMenuRecipes
from app.backend.schemas.requests.getRecipeRequest import RecipeProductItem
from app.backend.schemas.responses.recipeResponse import GenerateRecipesResponse, RecipeItem

# ---------------- Initialize AI Clients ----------------
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY is not set in environment variables")
client = Groq(api_key=groq_api_key)

SDXL_API_KEY = os.getenv("STABILITY_API_KEY")
SDXL_API_HOST = os.getenv("API_HOST", "https://api.stability.ai")
SDXL_ENGINE_ID = "stable-diffusion-xl-1024-v1-0"

if not SDXL_API_KEY:
    raise ValueError("STABILITY_API_KEY is not set in environment variables")

# ---------------- AI Recipe Generation ----------------
def call_ai_generate_recipes(products: list[RecipeProductItem]):
    """
        Use Groq API to generate meal recipes based on a list of food items.

        - Creates an AI prompt describing available ingredients
        - Requests exactly 3 main meals (+ optional snack)
        - Returns parsed JSON list of recipes

        Raises:
            HTTPException: If AI fails to return valid JSON
    """
    product_lines = "\n".join([f"{p.productName} ({p.grams}g, {p.kcal} kcal)" for p in products])

    prompt = f"""You are a professional chef and nutritionist. Create a balanced meal plan using ONLY these ingredients:

{product_lines}

Requirements:
1. Generate exactly 3 main meals (breakfast, lunch, dinner) and optionally 1 snack.
2. Use ONLY the ingredients listed above, you MUST use each of the ingredients.
3. Each ingredient amount MUST be used fully - you cannot leave something out the recipes.
4. Do not add any unlisted ingredients, you may add water.
5. Distribute (optionally) calories appropriately: breakfast (25-30%), lunch (35-40%), dinner (30-35%), snack (5-10%).
6. Each meal must include specific gram amounts from the ingredient list.
7. Show calories for each recipe. Sum all kcal from used products. If you use only a part of the product then calculate accordingly.
8. Provide detailed step-by-step cooking instructions with exact times and temperatures.
9. Make recipes practical and easy to follow.

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

        # Clean up the response - remove markdown code blocks if present
        text = text.strip()
        if text.startswith("```"):
            # Remove markdown code block markers
            lines = text.split('\n')
            # Remove first line (```json or ```)
            lines = lines[1:]
            # Remove last line (```)
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            text = '\n'.join(lines).strip()

        # Parse JSON
        recipes = json.loads(text)

        # Validate that it's a list
        if not isinstance(recipes, list):
            raise ValueError("AI returned invalid format - expected a list of recipes")

        return recipes
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI recipe generation failed - invalid JSON: {str(e)}. Response text: {text[:200]}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI recipe generation failed: {str(e)}"
        )


# ---------------- Stability AI Image Generation ----------------
def generate_sdxl_image_base64(prompt: str, width=1024, height=1024, steps=30, cfg_scale=7, samples=1, retries=2) -> str:
    """
        Generate a realistic recipe image via Stability AI API.

        Args:
            prompt: Text describing the food
            retries: Number of retry attempts in case of transient errors
        Returns:
            Base64-encoded image string
    """
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
    """
        Generate and store new AI recipes for a specific diet menu.

        Steps:
            1. Generate recipe data using AI
            2. Generate image for each recipe via SDXL
            3. Save recipe + menu linkage in DB
    """
    if not products:
        return GenerateRecipesResponse(status="Error", message="No products found to generate recipes.")

    menu = db.query(UserMenu).filter(UserMenu.id == user_menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")

    max_batch = db.query(UserMenuRecipes.recipeBatch).filter(
        UserMenuRecipes.userMenuId == menu.id
    ).order_by(UserMenuRecipes.recipeBatch.desc()).first()

    next_batch = (max_batch[0] + 1) if max_batch else 1

    print(f"[DEBUG] Starting recipe generation for menu {user_menu_id}, batch {next_batch}")

    try:
        ai_recipes = call_ai_generate_recipes(products)
        print(f"[DEBUG] AI generated {len(ai_recipes)} recipes")
    except Exception as e:
        print(f"[ERROR] AI recipe generation failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"AI recipe generation failed: {str(e)}"
        )

    response_recipes = []

    for idx, r in enumerate(ai_recipes):
        print(f"[DEBUG] Processing recipe {idx + 1}/{len(ai_recipes)}: {r.get('name', 'Unknown')}")
        image_prompt = f"{r['name']}: {r.get('description', '')} - appetizing food, realistic, vibrant"
        try:
            photo_base64 = generate_sdxl_image_base64(image_prompt)
            print(f"[DEBUG] Image generated successfully for recipe: {r['name']}")
        except HTTPException as e:
            # If image generation fails, use None for the image but still save the recipe
            print(f"[WARNING] Could not generate image for recipe '{r['name']}': {e.detail}")
            photo_base64 = None
        except Exception as e:
            print(f"[WARNING] Unexpected error generating image for recipe '{r['name']}': {str(e)}")
            photo_base64 = None

        recipe = Recipe(
            name=r["name"],
            description=r.get("description"),
            instructions=r["instructions"],
            pictureBase64=photo_base64,
            calories=r.get("calories")
        )
        db.add(recipe)
        db.flush()
        print(f"[DEBUG] Recipe saved to DB with ID: {recipe.id}")

        link = UserMenuRecipes(
            userMenuId=menu.id,
            recipeId=recipe.id,
            mealType=r.get("mealType", "lunch"),
            recipeBatch=next_batch
        )
        db.add(link)

        response_recipes.append(
            RecipeItem(
                mealType=r.get("mealType", "lunch"),
                name=r["name"],
                description=r.get("description"),
                instructions=r["instructions"],
                pictureBase64=photo_base64,
                calories=r.get("calories"),
                recipeBatch=next_batch
            )
        )

    try:
        db.commit()
        print(f"[DEBUG] Successfully committed {len(response_recipes)} recipes to database")
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Database commit failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Database error while saving recipes: {str(e)}"
        )

    print(f"[DEBUG] Returning response with {len(response_recipes)} recipes")
    return GenerateRecipesResponse(status="Optimal", recipes=response_recipes)


# ---------------- Get Recipes ----------------
def get_recipes_by_menu(db: Session, userUuid: int, menuId: int) -> GenerateRecipesResponse:
    """
            Get all menu recipes by menu ID.
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
                    pictureBase64=recipe.pictureBase64,
                    calories=recipe.calories,
                    recipeBatch=link.recipeBatch
                )
            )

    status_str = "Optimal" if recipes_list else "NoRecipes"
    return GenerateRecipesResponse(
        status=status_str,
        recipes=recipes_list if recipes_list else None,
        message=None if recipes_list else "No recipes found for this menu."
    )


# ---------------- Regenerate Recipes ----------------
def regenerate_menu_recipes(db: Session, userUuid: int, menuId: int) -> GenerateRecipesResponse:
    """
                Generate new recipes for the menu.
    """
    menu = db.query(UserMenu).filter(UserMenu.id == menuId, UserMenu.userUuid == userUuid).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")

    if not menu.plan or not isinstance(menu.plan, list):
        raise HTTPException(status_code=400, detail="No products found for this menu")

    try:
        product_items = [
            RecipeProductItem(**p)
            for p in menu.plan
        ]
    except Exception as e:
        # Catch unexpected data format in the JSON column
        raise HTTPException(
            status_code=500,
            detail=f"Internal Error: Could not parse product data from menu plan: {str(e)}"
        )

    try:
        new_recipes_response = create_recipes_from_menu(db, menu.id, product_items)
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Catch any unexpected errors during recipe generation
        raise HTTPException(
            status_code=500,
            detail=f"Error creating recipes: {str(e)}"
        )

    # Get all recipes including the newly created ones
    all_recipes_response = get_recipes_by_menu(db, userUuid, menuId)

    num_new_recipes = len(new_recipes_response.recipes or [])

    return GenerateRecipesResponse(
        status=all_recipes_response.status,
        recipes=all_recipes_response.recipes,
        message=f"Recipes successfully regenerated. Added {num_new_recipes} new recipes."
    )


# ---------------- Delete Recipes Batch ----------------
def delete_recipes_batch(db: Session, userUuid: int, menuId: int, batchId: int) -> dict:
    """
                Delete all recipes for the menu (by batch).
    """
    menu = db.query(UserMenu).filter(
        UserMenu.id == menuId,
        UserMenu.userUuid == userUuid
    ).first()

    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")

    recipe_links = db.query(UserMenuRecipes).filter(
        UserMenuRecipes.userMenuId == menuId,
        UserMenuRecipes.recipeBatch == batchId
    ).all()

    if not recipe_links:
        raise HTTPException(status_code=404, detail=f"No recipes found for batch {batchId}")

    recipe_ids = [link.recipeId for link in recipe_links]
    deleted_count = len(recipe_links)

    db.query(UserMenuRecipes).filter(
        UserMenuRecipes.userMenuId == menuId,
        UserMenuRecipes.recipeBatch == batchId
    ).delete(synchronize_session=False)

    for recipe_id in recipe_ids:
        # Check if this recipe is used in other menus
        other_usage = db.query(UserMenuRecipes).filter(
            UserMenuRecipes.recipeId == recipe_id
        ).first()

        if not other_usage:
            # Recipe is not used anywhere else, safe to delete
            db.query(Recipe).filter(Recipe.id == recipe_id).delete()

    db.commit()

    return {
        "status": "Success",
        "message": f"Deleted batch {batchId} ({deleted_count} recipes) from menu {menuId}"
    }