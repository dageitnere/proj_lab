from pulp import LpProblem, LpVariable, LpMinimize, lpSum, LpStatus
from sqlalchemy.orm import Session
from app.models.productProtSep import ProductProtSep

def normalize(s: str):
    return s.strip().lower()


def generate_diet_plan(
    db: Session,
    kcalTarget: float,
    proteinTarget: float,
    fatTarget: float,
    satFatTarget: float,
    carbsTarget: float,
    sugarTarget: float,
    saltTarget: float,
    restrictions: list[dict] = None
):
    # 1. Fetch products
    products = db.query(ProductProtSep).all()
    if not products:
        return {"error": "No products found in database."}

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

    problem += lpSum([x[p.id] * p.olbv / 100 for p in products]) >= proteinTarget * 0.9, "proteinMin"
    problem += lpSum([x[p.id] * p.olbv / 100 for p in products]) <= proteinTarget * 1.6, "proteinMax"

    problem += lpSum([x[p.id] * (p.dzivOlbv or 0) / 100 for p in products]) >= animal_target * 0.7, "animalProtMin"
    problem += lpSum([x[p.id] * (p.dzivOlbv or 0) / 100 for p in products]) <= animal_target * 1.1, "animalProtMax"

    problem += lpSum([x[p.id] * (p.pienaOlbv or 0) / 100 for p in products]) >= dairy_target * 0.7, "dairyProtMin"
    problem += lpSum([x[p.id] * (p.pienaOlbv or 0) / 100 for p in products]) <= dairy_target * 1.1, "dairyProtMax"

    problem += lpSum([x[p.id] * (p.auguOlbv or 0) / 100 for p in products]) >= plant_target * 0.7, "plantProtMin"
    problem += lpSum([x[p.id] * (p.auguOlbv or 0) / 100 for p in products]) <= plant_target * 1.1, "plantProtMax"

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

    # 7. Apply custom restrictions
    if restrictions:
        for r in restrictions:
            r_type = r.get("type")
            r_product = normalize(r.get("product", ""))
            r_value = r.get("value", None)

            for p in products:
                name = normalize(str(p.produkts))
                if name == r_product:
                    if r_type == "max_weight" and r_value is not None:
                        problem += x[p.id] <= r_value, f"Limit_{p.produkts}"
                    elif r_type == "min_weight" and r_value is not None:
                        problem += x[p.id] >= r_value, f"Min_{p.produkts}"
                    elif r_type == "exclude":
                        problem += x[p.id] == 0, f"Exclude_{p.produkts}"
                        problem += y[p.id] == 0

    # 8. Solve problem
    problem.solve()

    # 10. Handle result
    if LpStatus[problem.status] != "Optimal":
        return {"status": LpStatus[problem.status], "message": "No optimal solution found."}

    result = []
    for p in products:
        grams = x[p.id].varValue
        if grams and grams > 0:
            result.append({
                "product": p.produkts,
                "grams": round(grams, 1),
                "kcal": round(p.kcal * grams / 100, 1),
                "cost": round(p.cena100g * grams / 100, 2),
                "fat": round(p.tauki * grams / 100, 1),
                "carbs": round(p.oglh * grams / 100, 1),
                "protein": round(p.olbv * grams / 100, 1),
                "dairyProtein": round((p.pienaOlbv or 0) * grams / 100, 1),
                "animalProtein": round((p.dzivOlbv or 0) * grams / 100, 1),
                "plantProtein": round((p.auguOlbv or 0) * grams / 100, 1),
                "sugar": round(p.cukuri * grams / 100, 1),
                "sat_fat": round(p.piesatTauki * grams / 100, 1),
                "salt": round(p.sals * grams / 100, 1)
            })

    totals = {
        "totalKcal": round(sum(r["kcal"] for r in result), 1),
        "totalCost": round(sum(r["cost"] for r in result), 2),
        "totalFat": round(sum(r["fat"] for r in result), 1),
        "totalCarbs": round(sum(r["carbs"] for r in result), 1),
        "totalProtein": round(sum(r["protein"] for r in result), 1),
        "totalDairyProtein": round(sum(r["dairyProtein"] for r in result), 1),
        "totalAnimalProtein": round(sum(r["animalProtein"] for r in result), 1),
        "totalPlantProtein": round(sum(r["plantProtein"] for r in result), 1),
        "totalSugar": round(sum(r["sugar"] for r in result), 1),
        "totalSatFat": round(sum(r["sat_fat"] for r in result), 1),
        "totalSalt": round(sum(r["salt"] for r in result), 1)
    }

    return {"status": "Optimal", **totals, "plan": result}
