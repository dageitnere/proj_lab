from pulp import LpProblem, LpVariable, LpMinimize, lpSum, LpStatus
from sqlalchemy.orm import Session
from app.models.product import Product

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
    products = db.query(Product).all()
    if not products:
        return {"error": "No products found in database."}

    # 2. Create PuLP problem
    problem = LpProblem("Balanced_Diet", LpMinimize)

    # 3. Decision variables (grams of each product)
    x = {p.ID: LpVariable(f"x_{p.ID}", lowBound=0) for p in products}

    # Binary indicator variables (1 if product is used)
    y = {p.ID: LpVariable(f"y_{p.ID}", cat="Binary") for p in products}

    # 4. Objective: minimize total cost
    problem += lpSum([x[p.ID] * p.Cena_100g / 100 for p in products])

    # 5. Nutritional constraints
    problem += lpSum([x[p.ID] * p.kcal / 100 for p in products]) >= kcalTarget, "caloriesMin"
    problem += lpSum([x[p.ID] * p.kcal / 100 for p in products]) <= kcalTarget * 1.5, "caloriesMax"
    problem += lpSum([x[p.ID] * p.Olb_v / 100 for p in products]) >= proteinTarget, "proteinMin"
    problem += lpSum([x[p.ID] * p.Olb_v / 100 for p in products]) <= proteinTarget * 1.8, "proteinMax"
    problem += lpSum([x[p.ID] * p.Tauki / 100 for p in products]) >= fatTarget * 0.5, "fatMin"
    problem += lpSum([x[p.ID] * p.Tauki / 100 for p in products]) <= fatTarget, "fatMax"
    problem += lpSum([x[p.ID] * p.Oglh / 100 for p in products]) >= carbsTarget * 0.5, "carbsMin"
    problem += lpSum([x[p.ID] * p.Oglh / 100 for p in products]) <= carbsTarget, "carbsMax"
    problem += lpSum([x[p.ID] * p.Cukuri / 100 for p in products]) >= sugarTarget * 0.6, "sugarsMin"
    problem += lpSum([x[p.ID] * p.Cukuri / 100 for p in products]) <= sugarTarget, "sugarsMax"
    problem += lpSum([x[p.ID] * p.Piesat_Tauki / 100 for p in products]) >= satFatTarget * 0.6, "saturatedFatMin"
    problem += lpSum([x[p.ID] * p.Piesat_Tauki / 100 for p in products]) <= satFatTarget, "saturatedFatMax"
    problem += lpSum([x[p.ID] * p.Sals / 100 for p in products]) >= saltTarget * 0.6, "saltMin"
    problem += lpSum([x[p.ID] * p.Sals / 100 for p in products]) <= saltTarget, "saltMax"


    # Big-M constraint: link x and y
    M = 400  # max grams per product
    m = 50  # min grams if product is used
    for p in products:
        problem += x[p.ID] <= M * y[p.ID], f"MaxLink_{p.ID}"
        problem += x[p.ID] >= m * y[p.ID], f"MinLink_{p.ID}"

    # Require at least 10 different products
    problem += lpSum([y[p.ID] for p in products]) >= 15, "Min_10_Products"

    # 7. Apply custom restrictions
    if restrictions:
        for r in restrictions:
            r_type = r.get("type")
            r_product = normalize(r.get("product", ""))
            r_value = r.get("value", None)

            for p in products:
                name = normalize(str(p.Produkts))
                if name == r_product:
                    if r_type == "max_weight" and r_value is not None:
                        problem += x[p.ID] <= r_value, f"Limit_{p.Produkts}"
                    elif r_type == "min_weight" and r_value is not None:
                        problem += x[p.ID] >= r_value, f"Min_{p.Produkts}"
                    elif r_type == "exclude":
                        problem += x[p.ID] == 0, f"Exclude_{p.Produkts}"
                        problem += y[p.ID] == 0

    # 8. Solve problem
    problem.solve()

    # 10. Handle result
    if LpStatus[problem.status] != "Optimal":
        return {"status": LpStatus[problem.status], "message": "No optimal solution found."}

    result = []
    for p in products:
        grams = x[p.ID].varValue
        if grams and grams > 0:
            result.append({
                "product": p.Produkts,
                "grams": round(grams, 1),
                "kcal": round(p.kcal * grams / 100, 1),
                "cost": round(p.Cena_100g * grams / 100, 2),
                "fat": round(p.Tauki * grams / 100, 1),
                "carbs": round(p.Oglh * grams / 100, 1),
                "protein": round(p.Olb_v * grams / 100, 1),
                "sugar": round(p.Cukuri * grams / 100, 1),
                "sat_fat": round(p.Piesat_Tauki * grams / 100, 1),
                "salt": round(p.Sals * grams / 100, 1)
            })

    totals = {
        "total_kcal": round(sum(r["kcal"] for r in result), 1),
        "total_cost": round(sum(r["cost"] for r in result), 2),
        "total_fat": round(sum(r["fat"] for r in result), 1),
        "total_carbs": round(sum(r["carbs"] for r in result), 1),
        "total_protein": round(sum(r["protein"] for r in result), 1),
        "total_sugar": round(sum(r["sugar"] for r in result), 1),
        "total_sat_fat": round(sum(r["sat_fat"] for r in result), 1),
        "total_salt": round(sum(r["salt"] for r in result), 1)
    }

    return {"status": "Optimal", **totals, "plan": result}
