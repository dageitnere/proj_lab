import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import SidebarMenu from "../components/SidebarMenu.jsx";
import Footer from "../components/Footer.jsx";

/* ---------------- helpers ---------------- */
const withAuth = (path, options = {}) =>
  fetch(path, {
    credentials: "include",
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
  });

const formatNum = (n, digits = 1) => {
  const v = Number(n);
  if (Number.isNaN(v)) return "-";
  return v.toFixed(digits);
};

const formatDate = (v) => {
  if (!v) return "-";
  const d = new Date(v);
  if (Number.isNaN(d.getTime())) return String(v);
  return d.toLocaleString();
};

const parseJsonSafe = async (res) => {
  try {
    return await res.json();
  } catch {
    return null;
  }
};

const normalizeMenusList = (data) => {
  const arr = Array.isArray(data)
    ? data
    : data?.menus ?? data?.plans ?? data?.dietPlans ?? data?.items ?? [];

  if (!Array.isArray(arr)) return [];

  return arr.map((m) => ({
    id: m?.id ?? null,
    name: m?.name ?? m?.menuName ?? m?.title ?? "",
    totalKcal: m?.totalKcal ?? m?.kcal ?? m?.calories ?? 0,
    totalCost: m?.totalCost ?? m?.cost ?? 0,
    totalProtein: m?.totalProtein ?? m?.protein ?? 0,
    totalCarbs: m?.totalCarbs ?? m?.carbs ?? 0,
    totalFat: m?.totalFat ?? m?.fat ?? 0,
    date: m?.date ?? m?.createdAt ?? m?.created_at ?? null,
  }));
};

const normalizeMenuDetails = (data) => ({
  id: data?.id ?? null,
  name: data?.name ?? data?.menuName ?? data?.title ?? "Menu",
  totalKcal: data?.totalKcal ?? data?.kcal ?? data?.calories ?? 0,
  totalCost: data?.totalCost ?? data?.cost ?? 0,
  totalProtein: data?.totalProtein ?? data?.protein ?? 0,
  totalCarbs: data?.totalCarbs ?? data?.carbs ?? 0,
  totalFat: data?.totalFat ?? data?.fat ?? 0,
  totalSugar: data?.totalSugar ?? data?.sugar ?? data?.sugars ?? null,
  totalSatFat: data?.totalSatFat ?? data?.satFat ?? null,
  totalSalt: data?.totalSalt ?? data?.salt ?? null,
  date: data?.date ?? data?.createdAt ?? data?.created_at ?? null,
  vegan: !!data?.vegan,
  vegetarian: !!data?.vegetarian,
  dairyFree: !!data?.dairyFree,
  restrictions: Array.isArray(data?.restrictions) ? data.restrictions : [],
  plan: Array.isArray(data?.plan) ? data.plan : [],
});

/* ---------------- UI components ---------------- */
function Modal({ open, title, onClose, children }) {
  if (!open) return null;

  return (
    <div className="fixed inset-0 z-[60]">
      <div
        className="absolute inset-0 bg-black/40"
        onClick={onClose}
        aria-hidden="true"
      />
      <div className="absolute inset-0 flex items-center justify-center p-4">
        <div className="w-full max-w-6xl max-h-[90vh] overflow-hidden rounded-2xl bg-white shadow-xl border border-slate-200">
          <div className="flex items-center justify-between px-6 py-4 border-b border-slate-200">
            <h2 className="text-xl font-bold tracking-tight text-slate-900">
              {title}
            </h2>
            <button
              type="button"
              onClick={onClose}
              className="h-10 w-10 rounded-full bg-slate-100 text-slate-600 hover:bg-slate-200 flex items-center justify-center"
              aria-label="Close"
            >
              ✕
            </button>
          </div>

          <div className="p-6 overflow-y-auto max-h-[calc(90vh-64px)]">
            {children}
          </div>
        </div>
      </div>
    </div>
  );
}

function StatCard({ value, label }) {
  return (
    <div className="rounded-2xl bg-slate-900 text-white shadow-sm px-6 py-5 min-w-[180px]">
      <div className="text-3xl font-extrabold tracking-tight">{value}</div>
      <div className="mt-1 text-sm/5 opacity-90">{label}</div>
    </div>
  );
}

function DietTag({ children }) {
  return (
    <span className="rounded-full bg-green-50 text-green-700 border border-green-200 px-3 py-1 text-xs font-semibold">
      {children}
    </span>
  );
}

/* ---------------- page ---------------- */
export default function MyMenusPage() {
  const navigate = useNavigate();
  const [sidebarOpened, setSidebarOpened] = useState(false);
  const [menus, setMenus] = useState([]);
  const [search, setSearch] = useState("");

  const [loadingList, setLoadingList] = useState(false);
  const [viewLoadingKey, setViewLoadingKey] = useState(null);
  const [loadingDeleteName, setLoadingDeleteName] = useState("");
  const [globalError, setGlobalError] = useState("");

  const [open, setOpen] = useState(false);
  const [details, setDetails] = useState(null);
  const [currentMenuId, setCurrentMenuId] = useState(null);

  const [recipes, setRecipes] = useState([]);
  const [recipesStatus, setRecipesStatus] = useState("");
  const [recipesLoading, setRecipesLoading] = useState(false);
  const [recipesError, setRecipesError] = useState("");
  const [recipesGenerating, setRecipesGenerating] = useState(false);

  const filteredMenus = useMemo(() => {
    const q = search.trim().toLowerCase();
    if (!q) return menus;
    return menus.filter((m) => (m.name || "").toLowerCase().includes(q));
  }, [menus, search]);

  const loadMenus = async () => {
    setGlobalError("");
    setLoadingList(true);
    try {
      const res = await withAuth("/menu/getUserMenus");
      const data = await parseJsonSafe(res);

      if (!res.ok) {
        setMenus([]);
        setGlobalError(data?.detail || "Failed to load menus.");
        return;
      }

      setMenus(normalizeMenusList(data));
    } catch (e) {
      console.error(e);
      setMenus([]);
      setGlobalError("Failed to load menus.");
    } finally {
      setLoadingList(false);
    }
  };

  useEffect(() => {
    void loadMenus();
  }, []);

  const closeModal = () => {
    setOpen(false);
    setDetails(null);
    setCurrentMenuId(null);

    setRecipes([]);
    setRecipesStatus("");
    setRecipesError("");
    setRecipesLoading(false);
    setRecipesGenerating(false);
  };

  const loadRecipes = async (menuId) => {
    if (!menuId) return;

    setRecipesError("");
    setRecipesLoading(true);

    try {
      const res = await withAuth(`/recipes/${menuId}`);
      const data = await parseJsonSafe(res);

      if (!res.ok) {
        setRecipes([]);
        setRecipesStatus("");
        setRecipesError(data?.detail || "Failed to load recipes.");
        return;
      }

      const list = data?.recipes || [];
      setRecipes(list);
      setRecipesStatus(data?.status || (list.length ? "Ok" : "NoRecipes"));
    } catch (e) {
      console.error(e);
      setRecipes([]);
      setRecipesStatus("");
      setRecipesError("Failed to load recipes.");
    } finally {
      setRecipesLoading(false);
    }
  };

  const regenerateRecipes = async () => {
    if (!currentMenuId) return;

    setRecipesError("");
    setRecipesGenerating(true);

    try {
      const res = await withAuth("/recipes/regenerate", {
        method: "POST",
        body: JSON.stringify({ menuId: currentMenuId }),
      });

      const data = await parseJsonSafe(res);

      if (!res.ok) {
        setRecipesError(data?.detail || "Failed to generate recipes.");
        return;
      }

      await loadRecipes(currentMenuId);
    } catch (e) {
      console.error(e);
      setRecipesError("Failed to generate recipes.");
    } finally {
      setRecipesGenerating(false);
    }
  };

  const deleteBatch = async (batchId) => {
    if (!currentMenuId) return;

    const ok = window.confirm(`Are you sure you want to delete Batch ${batchId}?`);
    if (!ok) return;

    setRecipesError("");

    try {
      const res = await withAuth("/recipes/batch", {
        method: "DELETE",
        body: JSON.stringify({ menuId: currentMenuId, batchId }),
      });

      const data = await parseJsonSafe(res);

      if (!res.ok) {
        setRecipesError(data?.detail || "Failed to delete batch.");
        return;
      }

      await loadRecipes(currentMenuId);
    } catch (e) {
      console.error(e);
      setRecipesError("Failed to delete batch.");
    }
  };

  const handleView = async (menuName, menuId) => {
    const key = menuId ?? menuName;

    setGlobalError("");
    setViewLoadingKey(key);

    setRecipes([]);
    setRecipesStatus("");
    setRecipesError("");

    try {
      const res = await withAuth("/menu/getUserMenu", {
        method: "POST",
        body: JSON.stringify({ menuName }),
      });

      const data = await parseJsonSafe(res);

      if (!res.ok) {
        setGlobalError(data?.detail || "Failed to load menu details.");
        return;
      }

      const d = normalizeMenuDetails(data);
      setDetails(d);

      const realId = menuId ?? d.id ?? null;
      setCurrentMenuId(realId);

      setOpen(true);

      if (realId) {
        await loadRecipes(realId);
      } else {
        setRecipesStatus("NoMenuId");
        setRecipesError("Menu id not found. Recipes can't be loaded without menuId.");
      }
    } catch (e) {
      console.error(e);
      setGlobalError("Failed to load menu details.");
    } finally {
      setViewLoadingKey(null);
    }
  };

  const handleDelete = async (menuName) => {
    const ok = window.confirm(`Delete menu "${menuName}"?`);
    if (!ok) return;

    setGlobalError("");
    setLoadingDeleteName(menuName);

    try {
      const res = await withAuth("/menu/deleteMenu", {
        method: "DELETE",
        body: JSON.stringify({ menuName }),
      });

      const data = await parseJsonSafe(res);

      if (!res.ok) {
        setGlobalError(data?.detail || "Failed to delete menu.");
        return;
      }

      setMenus((prev) => prev.filter((m) => m.name !== menuName));

      if (details?.name === menuName) {
        closeModal();
      }
    } catch (e) {
      console.error(e);
      setGlobalError("Failed to delete menu.");
    } finally {
      setLoadingDeleteName("");
    }
  };

  const recipesByBatch = useMemo(() => {
    const acc = {};
    (recipes || []).forEach((r) => {
      const b = r?.recipeBatch || 1;
      acc[b] = acc[b] || [];
      acc[b].push(r);
    });
    return acc;
  }, [recipes]);

  const sortedBatchIds = useMemo(
    () => Object.keys(recipesByBatch).sort((a, b) => Number(a) - Number(b)),
    [recipesByBatch]
  );

  return (
    <div className="min-h-screen bg-noise-light text-slate-900">
      <SidebarMenu
        opened={sidebarOpened}
        setOpened={setSidebarOpened}
      />

      <div className={`transition-all duration-300 px-8 py-6 ${sidebarOpened ? "ml-72" : "ml-40"}`}>
        <div className="mt-10 mb-6 flex items-start justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">My menus</h1>
            <p className="mt-1 text-sm text-slate-600">
              Manage your personalized diet plans.
            </p>
          </div>
          <div className="flex items-center gap-3">
          <button
            type="button"
            className="rounded-xl bg-green-500 text-black font-semibold px-4 py-2 text-sm hover:bg-green-400 disabled:opacity-60 disabled:cursor-not-allowed"
            onClick={loadMenus}
            disabled={loadingList}
          >
            {loadingList ? "Refreshing..." : "Refresh"}
          </button>

          <button
            type="button"
            onClick={() => navigate("/new-page")}
            className="
              inline-flex items-center gap-2
              rounded-2xl
              bg-white/85 backdrop-blur
              border border-black/10
              px-5 py-3
              text-sm font-bold
              text-black/80
              shadow-sm
              hover:bg-white
              transition
            "
          >
            <span aria-hidden>←</span> Back
          </button>
        </div>

        </div>

        {globalError && (
          <div className="mb-4 rounded-xl border border-red-300 bg-red-50 px-4 py-3 text-sm text-red-700">
            {globalError}
          </div>
        )}

        <section className="rounded-2xl bg-white shadow-sm border border-slate-200 p-6">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <h2 className="text-xl font-semibold">My saved menus</h2>

            <input
              type="text"
              placeholder="Search..."
              className="w-full sm:w-72 rounded-xl border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>

          <div className="mt-4 h-px bg-slate-200" />

          <div className="mt-6 space-y-4">
            {loadingList && <div className="text-sm text-slate-500">Loading...</div>}

            {!loadingList && filteredMenus.length === 0 && (
              <div className="rounded-2xl border border-slate-200 bg-slate-50 px-5 py-6 text-sm text-slate-600">
                No menus saved yet.
              </div>
            )}

            {!loadingList &&
              filteredMenus.map((m) => {
                const viewKey = m.id ?? m.name;
                const isViewingThis = viewLoadingKey === viewKey;

                return (
                  <div
                    key={`${m.name}-${m.id ?? "noid"}`}
                    className="rounded-2xl bg-slate-50 border border-slate-200 p-5 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between"
                  >
                    <div className="min-w-0">
                      <div className="text-xl font-bold text-slate-900 truncate">
                        {m.name || "(no name)"}
                      </div>

                      <div className="mt-2 flex flex-wrap gap-4 text-sm text-slate-700">
                        <div>
                          <div className="text-slate-500">Calories</div>
                          <div>{formatNum(m.totalKcal, 0)} kcal</div>
                        </div>
                        <div>
                          <div className="text-slate-500">Cost</div>
                          <div>€{formatNum(m.totalCost, 2)}</div>
                        </div>
                        <div>
                          <div className="text-slate-500">Protein</div>
                          <div>{formatNum(m.totalProtein, 0)} g</div>
                        </div>
                        <div>
                          <div className="text-slate-500">Carbs</div>
                          <div>{formatNum(m.totalCarbs, 1)} g</div>
                        </div>
                        <div>
                          <div className="text-slate-500">Fat</div>
                          <div>{formatNum(m.totalFat, 1)} g</div>
                        </div>
                      </div>
                    </div>

                    <div className="flex gap-3 justify-end">
                      <button
                        type="button"
                        className="rounded-xl bg-green-500 text-black font-semibold px-5 py-2.5 text-sm hover:bg-green-400 disabled:opacity-60 disabled:cursor-not-allowed"
                        onClick={() => handleView(m.name, m.id)}
                        disabled={isViewingThis || !m.name}
                      >
                        {isViewingThis ? "Loading..." : "View"}
                      </button>

                      <button
                        type="button"
                        className="rounded-xl bg-green-500 text-black font-semibold px-5 py-2.5 text-sm hover:bg-green-400 disabled:opacity-60 disabled:cursor-not-allowed"
                        onClick={() => handleDelete(m.name)}
                        disabled={!m.name || loadingDeleteName === m.name}
                      >
                        {loadingDeleteName === m.name ? "Deleting..." : "Delete"}
                      </button>
                    </div>
                  </div>
                );
              })}
          </div>
        </section>

        <div className="mt-6">

        </div>
      </div>

      <Modal open={open} title={details?.name || "Menu"} onClose={closeModal}>
        {!details ? (
          <div className="text-sm text-slate-500">No data</div>
        ) : (
          <div className="space-y-8">
            <section>
              <h3 className="text-lg font-semibold text-slate-900">Summary</h3>
              <div className="mt-4 flex flex-wrap gap-3">
                <StatCard value={formatNum(details.totalKcal, 0)} label="Calories" />
                <StatCard value={formatNum(details.totalCost, 2)} label="Cost" />
                <StatCard value={`${formatNum(details.totalProtein, 0)} g`} label="Protein" />
                <StatCard value={`${formatNum(details.totalCarbs, 1)} g`} label="Carbs" />
                <StatCard value={`${formatNum(details.totalFat, 1)} g`} label="Fat" />
                <StatCard value={formatDate(details.date)} label="Created" />
              </div>

              <div className="mt-4 flex flex-wrap gap-2">
                {details.vegan && <DietTag>🌱 Vegan</DietTag>}
                {details.vegetarian && <DietTag>🥕 Vegetarian</DietTag>}
                {details.dairyFree && <DietTag>🥛❌ Dairy-Free</DietTag>}
                {!details.vegan && !details.vegetarian && !details.dairyFree && (
                  <span className="rounded-full bg-slate-100 text-slate-700 border border-slate-200 px-3 py-1 text-xs font-semibold">
                    No dietary restrictions
                  </span>
                )}
              </div>
            </section>

            <section>
              <h3 className="text-lg font-semibold text-slate-900">Restrictions</h3>

              {details.restrictions.length === 0 ? (
                <p className="mt-2 text-sm text-slate-600">No restrictions set.</p>
              ) : (
                <div className="mt-3 rounded-2xl border border-slate-200 bg-white p-4">
                  <ul className="space-y-2 text-sm">
                    {details.restrictions.map((r, idx) => (
                      <li
                        key={idx}
                        className="rounded-xl bg-slate-50 border border-slate-100 px-3 py-2"
                      >
                        {r.type === "exclude" && (
                          <>
                            ❌ Exclude: <strong>{r.product}</strong>
                          </>
                        )}
                        {r.type === "min_weight" && (
                          <>
                            ⚖️ Min weight for <strong>{r.product}</strong>: {r.value}g
                          </>
                        )}
                        {r.type === "max_weight" && (
                          <>
                            ⚖️ Max weight for <strong>{r.product}</strong>: {r.value}g
                          </>
                        )}
                        {!["exclude", "min_weight", "max_weight"].includes(r.type) && (
                          <>ℹ️ {JSON.stringify(r)}</>
                        )}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </section>

            <section>
              <h3 className="text-lg font-semibold text-slate-900">Menu items</h3>

              {details.plan.length === 0 ? (
                <p className="mt-2 text-sm text-slate-600">No items.</p>
              ) : (
                <div className="mt-3 space-y-3">
                  {details.plan.map((it, idx) => (
                    <div key={idx} className="rounded-2xl border border-slate-200 bg-white p-4">
                      <div className="text-lg font-bold text-slate-900">
                        {it.productName || "Unnamed Item"}
                      </div>

                      <div className="mt-2 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2 text-sm text-slate-700">
                        <div>
                          <span className="font-semibold">Amount:</span>{" "}
                          {formatNum(it.grams, 1)}g
                        </div>
                        <div>
                          <span className="font-semibold">Calories:</span>{" "}
                          {formatNum(it.kcal, 1)} kcal
                        </div>
                        <div>
                          <span className="font-semibold">Protein:</span>{" "}
                          {formatNum(it.protein, 1)}g
                        </div>
                        <div>
                          <span className="font-semibold">Cost:</span> €{formatNum(it.cost, 2)}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </section>

            <section>
              <div className="flex items-center justify-between gap-3">
                <h3 className="text-lg font-semibold text-slate-900">Recipes</h3>

                <button
                  type="button"
                  className="rounded-xl bg-green-500 text-black font-semibold px-4 py-2 text-sm hover:bg-green-400 disabled:opacity-60 disabled:cursor-not-allowed"
                  onClick={regenerateRecipes}
                  disabled={recipesGenerating || !currentMenuId}
                >
                  {recipesGenerating
                    ? "Generating..."
                    : recipes.length > 0
                    ? "Regenerate recipes"
                    : "Generate recipes"}
                </button>
              </div>

              {recipesLoading && <p className="mt-3 text-sm text-slate-500">Loading recipes...</p>}

              {recipesError && (
                <div className="mt-3 rounded-xl border border-red-300 bg-red-50 px-4 py-3 text-sm text-red-700">
                  {recipesError}
                </div>
              )}

              {!recipesLoading &&
                !recipesError &&
                (recipesStatus === "NoRecipes" || recipes.length === 0) && (
                  <div className="mt-4 rounded-2xl border border-slate-200 bg-slate-50 p-6 text-center">
                    <div className="text-slate-500 text-sm">
                      No recipes generated yet for this menu. Click “Generate recipes” to create some.
                    </div>
                  </div>
                )}

              {!recipesLoading && !recipesError && recipes.length > 0 && (
                <div className="mt-4 space-y-6">
                  {sortedBatchIds.map((batchId) => {
                    const batchRecipes = recipesByBatch[batchId] || [];
                    return (
                      <div key={batchId}>
                        <div className="flex items-center justify-between rounded-xl bg-slate-50 border border-slate-200 px-4 py-3">
                          <div className="font-semibold text-slate-800">Batch {batchId}</div>

                          <button
                            type="button"
                            className="rounded-xl bg-green-500 text-black font-semibold px-4 py-2 text-sm hover:bg-green-400 disabled:opacity-60 disabled:cursor-not-allowed"
                            onClick={() => deleteBatch(Number(batchId))}
                            disabled={!currentMenuId}
                          >
                            Delete batch
                          </button>
                        </div>

                        <div className="mt-3 grid grid-cols-1 lg:grid-cols-2 gap-4">
                          {batchRecipes.map((recipe, idx) => (
                            <div
                              key={recipe?.id ?? `${recipe?.name}-${idx}`}
                              className="rounded-2xl border border-slate-200 bg-white overflow-hidden shadow-sm"
                            >
                              <div className="flex items-center justify-between px-4 py-3 bg-slate-900 text-white">
                                <div className="text-xs uppercase tracking-wider opacity-90">
                                  {recipe.mealType || "Meal"}
                                </div>
                                <div className="font-semibold">{recipe.calories || 0} kcal</div>
                              </div>

                              {recipe.pictureBase64 && (
                                <div className="w-full h-56 bg-slate-100">
                                  <img
                                    src={`data:image/png;base64,${recipe.pictureBase64}`}
                                    alt={recipe.name || "Recipe"}
                                    className="w-full h-full object-cover"
                                  />
                                </div>
                              )}

                              <div className="p-4">
                                <div className="text-lg font-bold text-slate-900">
                                  {recipe.name || "Unnamed recipe"}
                                </div>

                                {recipe.description && (
                                  <div className="mt-1 text-sm text-slate-600 italic">
                                    {recipe.description}
                                  </div>
                                )}

                                <div className="mt-3 text-sm font-semibold text-slate-900">
                                  Instructions
                                </div>
                                <div className="mt-1 whitespace-pre-line rounded-xl bg-slate-50 border border-slate-200 p-3 text-sm text-slate-700">
                                  {recipe.instructions || "-"}
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </section>

            <section className="flex gap-3">
              <button
                type="button"
                className="rounded-xl bg-green-500 text-black font-semibold px-4 py-2 text-sm hover:bg-green-400"
                onClick={closeModal}
              >
                Close
              </button>
            </section>
          </div>
        )}
      </Modal>
    </div>
  );
}
