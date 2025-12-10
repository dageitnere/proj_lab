// src/pages/GenerateMenuPage.jsx
import { useEffect, useState } from "react";
import SidebarMenu from "../components/SidebarMenu.jsx";
import Footer from "../components/Footer.jsx";

export default function GenerateMenuPage() {
  // ---------- nutrition targets ----------
  const [kcal, setKcal] = useState("");
  const [protein, setProtein] = useState("");
  const [fat, setFat] = useState("");
  const [satFat, setSatFat] = useState("");
  const [carbs, setCarbs] = useState("");
  const [sugars, setSugars] = useState("");
  const [salt, setSalt] = useState("");

  // ---------- diet flags ----------
  const [vegan, setVegan] = useState(false);
  const [vegetarian, setVegetarian] = useState(false);
  const [dairyFree, setDairyFree] = useState(false);

  // ---------- restrictions ----------
  // each item: { id, type, product, value, warning }
  const [restrictions, setRestrictions] = useState([]);

  // ---------- saved menus ----------
  const [menuNames, setMenuNames] = useState([]);
  const [selectedMenuName, setSelectedMenuName] = useState("");

  // ---------- products ----------
  const [productNames, setProductNames] = useState([]);
  const [userProductNames, setUserProductNames] = useState([]);
  const [productSearch, setProductSearch] = useState("");
  const [userProductSearch, setUserProductSearch] = useState("");

  const allProductNames = [...new Set([...productNames, ...userProductNames])];

  // ---------- result ----------
  const [lastResult, setLastResult] = useState(null);

  // ---------- messages ----------
  const [validationError, setValidationError] = useState("");
  const [invalidProducts, setInvalidProducts] = useState([]);
  const [saveWarning, setSaveWarning] = useState("");
  const [saveOk, setSaveOk] = useState("");
  const [globalError, setGlobalError] = useState("");

  const [loadingInit, setLoadingInit] = useState(false);
  const [loadingGenerate, setLoadingGenerate] = useState(false);
  const [loadingSave, setLoadingSave] = useState(false);
  const [loadingDefaults, setLoadingDefaults] = useState(false);
  const [loadingMenuInfo, setLoadingMenuInfo] = useState(false);

  const withAuth = (path, options = {}) =>
    fetch(path, {
      credentials: "include",
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...(options.headers || {}),
      },
    });

  // ---------- initial load ----------
  useEffect(() => {
    const init = async () => {
      setLoadingInit(true);
      try {
        const [menusRes, productsRes, userProductsRes] = await Promise.all([
          withAuth("/menu/getUserMenusNames"),
          withAuth("/products/productsNames"),
          withAuth("/userProducts/userProductsNames"),
        ]);

        const menus = await menusRes.json();
        const products = await productsRes.json();
        const userProducts = await userProductsRes.json();

        setMenuNames(menus.menus || []);
        setProductNames(products.products || []);
        setUserProductNames(userProducts.products || []);
      } catch (err) {
        console.error(err);
        setGlobalError("Failed to load initial data (menus & products).");
      } finally {
        setLoadingInit(false);
      }
    };

    void init();
  }, []);

  const loadDefaultTargets = async () => {
    try {
      setLoadingDefaults(true);
      const res = await withAuth("/profile/getCalculatedNutritionInfo");
      if (!res.ok) throw new Error("Failed to load defaults");
      const data = await res.json();

      setKcal(data.calculatedKcal ?? "");
      setCarbs(data.calculatedCarbs ?? "");
      setProtein(data.calculatedProtein ?? "");
      setFat(data.calculatedFat ?? "");
      setSatFat(data.calculatedSatFat ?? "");
      setSugars(data.calculatedSugar ?? "");
      setSalt(data.calculatedSalt ?? "");

      const veganFlag = !!data.isVegan;
      const vegetarianFlag = veganFlag || !!data.isVegetarian;
      const dairyFlag = veganFlag || !!data.isDairyInt;

      setVegan(veganFlag);
      setVegetarian(vegetarianFlag);
      setDairyFree(dairyFlag);
    } catch (err) {
      console.error(err);
      setGlobalError("Failed to load default nutrition targets.");
    } finally {
      setLoadingDefaults(false);
    }
  };

  // ---------- restrictions logic ----------
  const addRestriction = () => {
    setRestrictions((prev) => [
      ...prev,
      {
        id: Date.now() + Math.random(),
        type: "exclude",
        product: "",
        value: "",
        warning: "",
      },
    ]);
  };

  const updateRestriction = (id, patch) => {
    setRestrictions((prev) =>
      prev.map((r) => (r.id === id ? { ...r, ...patch } : r))
    );
  };

  const removeRestriction = (id) => {
    setRestrictions((prev) => prev.filter((r) => r.id !== id));
  };

  const handleVeganChange = (checked) => {
    setVegan(checked);
    if (checked) {
      setVegetarian(true);
      setDairyFree(true);
    }
  };

  const handleVegetarianChange = (checked) => {
    if (vegan && !checked) return;
    setVegetarian(checked);
  };

  const handleDairyFreeChange = (checked) => {
    if (vegan && !checked) return;
    setDairyFree(checked);
  };

  // ---------- generate menu ----------
  const handleGenerate = async () => {
    setValidationError("");
    setInvalidProducts([]);
    setSaveWarning("");
    setSaveOk("");
    setGlobalError("");

    const body = {
      kcal: parseFloat(kcal),
      protein: parseFloat(protein),
      fat: parseFloat(fat),
      satFat: parseFloat(satFat),
      carbs: parseFloat(carbs),
      sugars: parseFloat(sugars),
      salt: parseFloat(salt),
      vegan,
      vegetarian,
      dairyFree,
      restrictions: restrictions.map((r) => {
        const base = {
          type: r.type,
          product: r.product.trim().toLowerCase(),
        };
        if (r.type !== "exclude" && r.value) {
          base.value = parseFloat(r.value);
        }
        return base;
      }),
    };

    try {
      setLoadingGenerate(true);
      const res = await withAuth("/menu/generateMenu", {
        method: "POST",
        body: JSON.stringify(body),
      });
      const result = await res.json();
      setLastResult(result);

      if (result.error) {
        setValidationError(result.error);
        return;
      }

      if (result.status === "InvalidProducts" && result.invalidProducts) {
        setInvalidProducts(result.invalidProducts);
        setRestrictions((prev) =>
          prev.map((r) => ({
            ...r,
            warning: result.invalidProducts.includes(r.product.trim())
              ? "⚠ Not in database!"
              : "",
          }))
        );
        setValidationError("Some products were not found in the database.");
        return;
      }

      setRestrictions((prev) => prev.map((r) => ({ ...r, warning: "" })));
    } catch (err) {
      console.error(err);
      setGlobalError("Error while generating menu.");
    } finally {
      setLoadingGenerate(false);
    }
  };

  // ---------- load saved menu ----------
  const handleLoadMenuInfo = async () => {
    if (!selectedMenuName) {
      alert("Please select a menu first.");
      return;
    }

    try {
      setLoadingMenuInfo(true);
      const res = await withAuth("/menu/getUserMenu", {
        method: "POST",
        body: JSON.stringify({ menuName: selectedMenuName }),
      });
      if (!res.ok) throw new Error("Failed to load menu");
      const data = await res.json();

      setKcal(data.totalKcal ?? "");
      setProtein(data.totalProtein ?? "");
      setFat(data.totalFat ?? "");
      setSatFat(data.totalSatFat ?? "");
      setCarbs(data.totalCarbs ?? "");
      setSugars(data.totalSugar ?? "");
      setSalt(data.totalSalt ?? "");

      const veganFlag = !!data.vegan;
      const vegetarianFlag = veganFlag || !!data.vegetarian;
      const dairyFlag = veganFlag || !!data.dairyFree;

      setVegan(veganFlag);
      setVegetarian(vegetarianFlag);
      setDairyFree(dairyFlag);

      const loadedRestrictions =
        (data.restrictions || []).map((r) => ({
          id: Date.now() + Math.random(),
          type: r.type || "exclude",
          product: r.product || "",
          value: r.value !== undefined ? r.value : "",
          warning: "",
        })) || [];

      setRestrictions(loadedRestrictions);
    } catch (err) {
      console.error(err);
      setGlobalError("Failed to load selected menu.");
    } finally {
      setLoadingMenuInfo(false);
    }
  };

  // ---------- save menu ----------
  const handleSaveMenu = async () => {
    setSaveWarning("");
    setSaveOk("");

    if (!lastResult || !lastResult.plan || lastResult.plan.length === 0) {
      setSaveWarning("⚠ Generate a menu before saving.");
      return;
    }

    const menuName = window.prompt("Enter menu name:");
    if (!menuName || !menuName.trim()) {
      setSaveWarning("⚠ Menu name is required.");
      return;
    }

    const body = {
      name: menuName.trim(),
      totalKcal: lastResult.totalKcal,
      totalCost: lastResult.totalCost,
      totalFat: lastResult.totalFat,
      totalCarbs: lastResult.totalCarbs,
      totalProtein: lastResult.totalProtein,
      totalDairyProtein: lastResult.totalDairyProtein || 0,
      totalAnimalProtein: lastResult.totalAnimalProtein || 0,
      totalPlantProtein: lastResult.totalPlantProtein || 0,
      totalSugar: lastResult.totalSugar,
      totalSatFat: lastResult.totalSatFat,
      totalSalt: lastResult.totalSalt,
      plan: lastResult.plan,
      vegan,
      vegetarian,
      dairyFree,
      restrictions: restrictions.map((r) => {
        const base = {
          type: r.type,
          product: r.product.trim().toLowerCase(),
        };
        if (r.type !== "exclude" && r.value) {
          base.value = parseFloat(r.value);
        }
        return base;
      }),
    };

    try {
      setLoadingSave(true);
      const res = await withAuth("/menu/saveMenu", {
        method: "POST",
        body: JSON.stringify(body),
      });
      const data = await res.json();
      if (!res.ok) {
        setSaveWarning(`⚠ ${data.detail || "Error saving menu."}`);
        return;
      }
      setSaveOk("✅ Menu saved successfully.");
      void (async () => {
        try {
          const resNames = await withAuth("/menu/getUserMenusNames");
          const dNames = await resNames.json();
          setMenuNames(dNames.menus || []);
        } catch (e) {
          console.error(e);
        }
      })();
      setTimeout(() => setSaveOk(""), 3000);
    } catch (err) {
      console.error(err);
      setSaveWarning("⚠ Error saving menu.");
    } finally {
      setLoadingSave(false);
    }
  };

  // ---------- helpers for rendering ----------
  const filteredProducts = productNames.filter((p) =>
    p.toLowerCase().includes(productSearch.toLowerCase())
  );
  const filteredUserProducts = userProductNames.filter((p) =>
    p.toLowerCase().includes(userProductSearch.toLowerCase())
  );

  const renderResult = () => {
    if (!lastResult || !lastResult.plan || lastResult.plan.length === 0) {
      return (
        <p className="text-slate-500 text-xs">
          Generated products will appear here.
        </p>
      );
    }

    const r = lastResult;

    return (
      <>
        <div className="flex flex-wrap gap-2 mb-4">
          <span className="inline-flex items-center rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-700">
            Kcal: {r.totalKcal.toFixed(1)}
          </span>
          <span className="inline-flex items-center rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-700">
            Total cost: €{r.totalCost.toFixed(2)}
          </span>
          <span className="inline-flex items-center rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-700">
            Protein: {r.totalProtein.toFixed(1)} g
          </span>
          <span className="inline-flex items-center rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-700">
            Fat: {r.totalFat.toFixed(1)} g
          </span>
          <span className="inline-flex items-center rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-700">
            Carbs: {r.totalCarbs.toFixed(1)} g
          </span>
        </div>

        <div className="border-t border-slate-200 pt-3 space-y-2 text-sm">
          <p className="text-slate-700 text-sm font-medium mb-2">
            Status: {r.status}
          </p>
          <div className="overflow-x-auto">
            <table className="min-w-full text-xs border border-slate-200">
              <thead className="bg-slate-50">
                <tr>
                  <th className="px-2 py-1 border border-slate-200 text-left">
                    Product
                  </th>
                  <th className="px-2 py-1 border border-slate-200 text-left">
                    Grams
                  </th>
                  <th className="px-2 py-1 border border-slate-200 text-left">
                    Kcal
                  </th>
                  <th className="px-2 py-1 border border-slate-200 text-left">
                    Cost (€)
                  </th>
                  <th className="px-2 py-1 border border-slate-200 text-left">
                    Fat (g)
                  </th>
                  <th className="px-2 py-1 border border-slate-200 text-left">
                    Carbs (g)
                  </th>
                  <th className="px-2 py-1 border border-slate-200 text-left">
                    Protein (g)
                  </th>
                  <th className="px-2 py-1 border border-slate-200 text-left">
                    Sugar (g)
                  </th>
                  <th className="px-2 py-1 border border-slate-200 text-left">
                    Sat. fat (g)
                  </th>
                  <th className="px-2 py-1 border border-slate-200 text-left">
                    Salt (mg)
                  </th>
                </tr>
              </thead>
              <tbody>
                {r.plan.map((item, idx) => (
                  <tr key={idx} className="odd:bg-white even:bg-slate-50">
                    <td className="px-2 py-1 border border-slate-200">
                      {item.productName}
                    </td>
                    <td className="px-2 py-1 border border-slate-200">
                      {item.grams.toFixed(1)}
                    </td>
                    <td className="px-2 py-1 border border-slate-200">
                      {item.kcal.toFixed(1)}
                    </td>
                    <td className="px-2 py-1 border border-slate-200">
                      {item.cost.toFixed(2)}
                    </td>
                    <td className="px-2 py-1 border border-slate-200">
                      {item.fat.toFixed(1)}
                    </td>
                    <td className="px-2 py-1 border border-slate-200">
                      {item.carbs.toFixed(1)}
                    </td>
                    <td className="px-2 py-1 border border-slate-200">
                      {item.protein.toFixed(1)}
                    </td>
                    <td className="px-2 py-1 border border-slate-200">
                      {item.sugars.toFixed(1)}
                    </td>
                    <td className="px-2 py-1 border border-slate-200">
                      {item.satFat.toFixed(1)}
                    </td>
                    <td className="px-2 py-1 border border-slate-200">
                      {item.salt.toFixed(1)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </>
    );
  };

  // ---------- JSX ----------
  return (
    <div className="min-h-screen bg-noise-light text-slate-900">
      <SidebarMenu />

      <main className="pl-52 px-8 py-6 pr-40">
        <div className="mt-10 mb-6 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">
              Generate diet menu
            </h1>
            <p className="mt-1 text-sm text-slate-600">
              Set your targets, apply restrictions and generate a menu.
            </p>
          </div>

          {loadingInit && (
            <span className="text-xs text-slate-500">Loading data...</span>
          )}
        </div>

        {globalError && (
          <div className="mb-4 rounded-xl border border-red-300 bg-red-50 px-4 py-3 text-sm text-red-700">
            {globalError}
          </div>
        )}

        {validationError && (
          <div className="mb-4 rounded-xl border border-red-300 bg-red-50 px-4 py-3 text-sm text-red-700">
            <p className="font-semibold mb-1">Validation error</p>
            <p>{validationError}</p>
            {invalidProducts.length > 0 && (
              <ul className="mt-2 list-disc list-inside">
                {invalidProducts.map((p) => (
                  <li key={p}>{p}</li>
                ))}
              </ul>
            )}
          </div>
        )}

        <div className="mt-4 grid grid-cols-1 lg:grid-cols-[minmax(0,2.4fr)_minmax(0,0.8fr)] gap-3">
          <div className="space-y-6">
            <section className="rounded-2xl bg-white shadow-sm border border-slate-200 p-6">
              <h2 className="text-lg font-semibold mb-4">Targets</h2>

              <div className="flex flex-col gap-3 sm:flex-row sm:items-center mb-4">
                <select
                  className="w-full sm:w-1/2 rounded-xl border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
                  value={selectedMenuName}
                  onChange={(e) => setSelectedMenuName(e.target.value)}
                >
                  <option value="">-- Select menu --</option>
                  {menuNames.map((name) => (
                    <option key={name} value={name}>
                      {name}
                    </option>
                  ))}
                </select>

                <div className="flex gap-2">
                  <button
                    type="button"
                    className="rounded-xl border border-slate-300 px-3 py-2 text-sm hover:bg-slate-50 disabled:opacity-60 disabled:cursor-not-allowed"
                    onClick={handleLoadMenuInfo}
                    disabled={loadingMenuInfo}
                  >
                    {loadingMenuInfo ? "Loading..." : "Load info"}
                  </button>
                  <button
                    type="button"
                    className="rounded-xl bg-slate-900 text-white px-3 py-2 text-sm hover:bg-slate-800 disabled:opacity-60 disabled:cursor-not-allowed"
                    onClick={loadDefaultTargets}
                    disabled={loadingDefaults}
                  >
                    {loadingDefaults ? "Loading..." : "Load defaults"}
                  </button>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="space-y-1">
                  <label className="text-sm font-medium text-slate-700">
                    Kcal target
                  </label>
                  <input
                    type="number"
                    className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
                    placeholder="e.g. 2000"
                    value={kcal}
                    onChange={(e) => setKcal(e.target.value)}
                  />
                </div>

                <div className="space-y-1">
                  <label className="text-sm font-medium text-slate-700">
                    Protein (g)
                  </label>
                  <input
                    type="number"
                    className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
                    value={protein}
                    onChange={(e) => setProtein(e.target.value)}
                  />
                </div>

                <div className="space-y-1">
                  <label className="text-sm font-medium text-slate-700">
                    Fat (g)
                  </label>
                  <input
                    type="number"
                    className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
                    value={fat}
                    onChange={(e) => setFat(e.target.value)}
                  />
                </div>

                <div className="space-y-1">
                  <label className="text-sm font-medium text-slate-700">
                    Sat fat (g)
                  </label>
                  <input
                    type="number"
                    className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
                    value={satFat}
                    onChange={(e) => setSatFat(e.target.value)}
                  />
                </div>

                <div className="space-y-1">
                  <label className="text-sm font-medium text-slate-700">
                    Carbs (g)
                  </label>
                  <input
                    type="number"
                    className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
                    value={carbs}
                    onChange={(e) => setCarbs(e.target.value)}
                  />
                </div>

                <div className="space-y-1">
                  <label className="text-sm font-medium text-slate-700">
                    Sugars (g)
                  </label>
                  <input
                    type="number"
                    className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
                    value={sugars}
                    onChange={(e) => setSugars(e.target.value)}
                  />
                </div>

                <div className="space-y-1">
                  <label className="text-sm font-medium text-slate-700">
                    Salt (mg)
                  </label>
                  <input
                    type="number"
                    className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
                    value={salt}
                    onChange={(e) => setSalt(e.target.value)}
                  />
                </div>
              </div>

              <div className="mt-5 flex flex-wrap gap-3">
                <button
                  type="button"
                  onClick={() => handleVeganChange(!vegan)}
                  className={`inline-flex items-center rounded-full border px-3 py-1 text-xs font-medium ${
                    vegan
                      ? "border-green-500 text-green-600 bg-green-50"
                      : "border-slate-300 hover:border-green-500 hover:text-green-600"
                  }`}
                >
                  Vegan
                </button>
                <button
                  type="button"
                  onClick={() => handleVegetarianChange(!vegetarian)}
                  className={`inline-flex items-center rounded-full border px-3 py-1 text-xs font-medium ${
                    vegetarian
                      ? "border-green-500 text-green-600 bg-green-50"
                      : "border-slate-300 hover:border-green-500 hover:text-green-600"
                  }`}
                >
                  Vegetarian
                </button>
                <button
                  type="button"
                  onClick={() => handleDairyFreeChange(!dairyFree)}
                  className={`inline-flex items-center rounded-full border px-3 py-1 text-xs font-medium ${
                    dairyFree
                      ? "border-green-500 text-green-600 bg-green-50"
                      : "border-slate-300 hover:border-green-500 hover:text-green-600"
                  }`}
                >
                  Dairy free
                </button>
              </div>
            </section>

            {/* Restrictions */}
            <section className="rounded-2xl bg-white shadow-sm border border-slate-200 p-6">
              <h2 className="text-lg font-semibold mb-4">Restrictions</h2>

              <datalist id="product-suggestions">
                {allProductNames.map((p) => (
                  <option key={p} value={p} />
                ))}
              </datalist>

              <div className="space-y-3">
                {restrictions.map((r) => (
                  <div
                    key={r.id}
                    className="flex flex-col gap-3 sm:flex-row sm:items-center"
                  >
                    <select
                      className="w-full sm:w-40 rounded-xl border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
                      value={r.type}
                      onChange={(e) =>
                        updateRestriction(r.id, {
                          type: e.target.value,
                        })
                      }
                    >
                      <option value="exclude">Exclude</option>
                      <option value="max_weight">Max. weight</option>
                      <option value="min_weight">Min. weight</option>
                    </select>

                    <input
                      type="text"
                      placeholder="Product name"
                      list="product-suggestions"
                      className="flex-1 rounded-xl border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
                      value={r.product}
                      onChange={(e) =>
                        updateRestriction(r.id, {
                          product: e.target.value,
                          warning: "",
                        })
                      }
                    />

                    {r.type !== "exclude" && (
                      <input
                        type="number"
                        placeholder="Value (g)"
                        className="w-full sm:w-32 rounded-xl border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
                        value={r.value}
                        onChange={(e) =>
                          updateRestriction(r.id, {
                            value: e.target.value,
                          })
                        }
                      />
                    )}

                    <button
                      type="button"
                      className="h-9 w-9 rounded-full bg-slate-100 flex items-center justify-center text-slate-500 hover:bg-slate-200"
                      onClick={() => removeRestriction(r.id)}
                    >
                      ✕
                    </button>

                    {r.warning && (
                      <p className="text-xs text-red-500 mt-1">
                        {r.warning}
                      </p>
                    )}
                  </div>
                ))}

                {restrictions.length === 0 && (
                  <p className="text-xs text-slate-500">
                    No restrictions added yet.
                  </p>
                )}
              </div>

              <button
                type="button"
                className="mt-4 w-full rounded-xl bg-slate-100 text-sm font-medium py-2 hover:bg-slate-200"
                onClick={addRestriction}
              >
                + Add restriction
              </button>
            </section>

            <section className="rounded-2xl bg-white shadow-sm border border-slate-200 p-6 space-y-4">
              <button
                type="button"
                className="w-full rounded-xl bg-green-500 text-black font-semibold py-2.5 text-sm hover:bg-green-400 disabled:opacity-60 disabled:cursor-not-allowed"
                onClick={handleGenerate}
                disabled={loadingGenerate}
              >
                {loadingGenerate ? "Generating..." : "Generate menu"}
              </button>

              <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
                <button
                  type="button"
                  className="rounded-xl bg-slate-900 text-white px-4 py-2 text-sm font-medium hover:bg-slate-800 disabled:opacity-60 disabled:cursor-not-allowed"
                  onClick={handleSaveMenu}
                  disabled={loadingSave}
                >
                  {loadingSave ? "Saving..." : "Save menu"}
                </button>
                {saveWarning && (
                  <p className="text-xs text-red-500">{saveWarning}</p>
                )}
                {saveOk && (
                  <p className="text-xs text-green-600">{saveOk}</p>
                )}
              </div>
            </section>

            <section className="rounded-2xl bg-white shadow-sm border border-slate-200 p-6 mb-4">
              <h2 className="text-lg font-semibold mb-4">Result</h2>
              {renderResult()}
            </section>
          </div>

          <div className="rounded-2xl bg-white shadow-sm border border-slate-200 p-6 flex flex-col max-h-[720px] lg:max-w-xs lg:justify-self-start">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold">All products</h2>
            </div>

            <div className="mb-3">
              <input
                type="text"
                placeholder="Search product..."
                className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
                value={productSearch}
                onChange={(e) => setProductSearch(e.target.value)}
              />
            </div>

            <div className="flex-1 overflow-y-auto border border-slate-100 rounded-xl mb-4">
              <table className="min-w-full text-sm">
                <thead className="sticky top-0 bg-slate-50">
                  <tr>
                    <th className="px-3 py-2 text-left font-medium text-slate-600">
                      Product name
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {filteredProducts.map((name) => (
                    <tr key={name} className="border-t border-slate-100">
                      <td className="px-3 py-2 text-slate-800">{name}</td>
                    </tr>
                  ))}
                  {filteredProducts.length === 0 && (
                    <tr className="border-t border-slate-100">
                      <td className="px-3 py-2 text-slate-500 text-sm">
                        No products found.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>

            <h3 className="text-sm font-semibold mb-2">
              Your own products
            </h3>
            <div className="mb-3">
              <input
                type="text"
                placeholder="Search your product..."
                className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
                value={userProductSearch}
                onChange={(e) => setUserProductSearch(e.target.value)}
              />
            </div>

            <div className="flex-1 overflow-y-auto border border-slate-100 rounded-xl">
              <table className="min-w-full text-sm">
                <thead className="sticky top-0 bg-slate-50">
                  <tr>
                    <th className="px-3 py-2 text-left font-medium text-slate-600">
                      Product name
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {filteredUserProducts.map((name) => (
                    <tr key={name} className="border-t border-slate-100">
                      <td className="px-3 py-2 text-slate-800">{name}</td>
                    </tr>
                  ))}
                  {filteredUserProducts.length === 0 && (
                    <tr className="border-t border-slate-100">
                      <td className="px-3 py-2 text-slate-500 text-sm">
                        No user products found.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <div className="mt-6">
          <Footer />
        </div>
      </main>
    </div>
  );
}
