import { useEffect, useMemo, useState } from "react";
import SidebarMenu from "../components/SidebarMenu.jsx";
import Footer from "../components/Footer.jsx";

const API_BASE = "/userProducts";

function EditModal({ product, onClose, onSubmit }) {
  const [fields, setFields] = useState({
    productName: "",
    kcal: "",
    fat: "",
    satFat: "",
    carbs: "",
    sugars: "",
    protein: "",
    salt: "",
    price1kg: "",
    proteinType: "",
  });

  useEffect(() => {
    if (!product) return;

    setFields({
      productName: product.productName ?? "",
      kcal: product.kcal ?? "",
      fat: product.fat ?? "",
      satFat: product.satFat ?? "",
      carbs: product.carbs ?? "",
      sugars: product.sugars ?? "",
      protein: product.protein ?? "",
      salt: product.salt ?? "",
      price1kg: product.price1kg ?? "",
      proteinType: product.dairyProt
        ? "dairy" : product.animalProt
        ? "animal" : product.plantProt
        ? "plant" : "",
      });
    }, [product]);


  const handleChange = (key, value) => {
    setFields((prev) => ({ ...prev, [key]: value }));
  };

    const handleSubmit = () => {
      const payload = {
        oldProductName: product.productName,
        productName: fields.productName.trim() || null,
        kcal: fields.kcal !== "" ? Number(fields.kcal) : null,
        fat: fields.fat !== "" ? Number(fields.fat) : null,
        satFat: fields.satFat !== "" ? Number(fields.satFat) : null,
        carbs: fields.carbs !== "" ? Number(fields.carbs) : null,
        sugars: fields.sugars !== "" ? Number(fields.sugars) : null,
        protein: fields.protein !== "" ? Number(fields.protein) : null,
        salt: fields.salt !== "" ? Number(fields.salt) : null,
        price1kg: fields.price1kg !== "" ? Number(fields.price1kg) : null,
      };

      if (fields.proteinType) {
        payload.dairyProtein = fields.proteinType === "dairy" ? true : null;
        payload.animalProtein = fields.proteinType === "animal" ? true : null;
        payload.plantProtein = fields.proteinType === "plant" ? true : null;
      }


      onSubmit(payload);
    };

  if (!product) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div className="relative w-full max-w-2xl rounded-2xl bg-white p-6 shadow-xl">
        <button
          onClick={onClose}
          className="absolute right-3 top-3 text-slate-500 hover:text-black"
        >
          ✕
        </button>

        <h2 className="mb-1 text-xl font-semibold text-slate-900">
          Edit product
        </h2>

        <div className="mb-4 rounded-xl bg-slate-50 px-3 py-2 text-xs text-slate-700">
          Current product:{" "}
          <span className="font-semibold text-slate-900">
            {product.productName}
          </span>
        </div>

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div className="space-y-1">
            <label className="text-xs font-medium text-slate-700">
              New name
            </label>
            <input
              className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-green-500"
              placeholder={product.productName}
              value={fields.productName}
              onChange={(e) => handleChange("productName", e.target.value)}
            />
          </div>

          <div className="space-y-1">
            <label className="text-xs font-medium text-slate-700">Kcal</label>
            <input
              type="number"
              className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-green-500"
              placeholder={
                product.kcal !== null && product.kcal !== undefined
                  ? String(product.kcal)
                  : "-"
              }
              value={fields.kcal}
              onChange={(e) => handleChange("kcal", e.target.value)}
            />
          </div>

          <div className="space-y-1">
            <label className="text-xs font-medium text-slate-700">
              Protein (g)
            </label>
            <input
              type="number"
              className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-green-500"
              placeholder={
                product.protein !== null && product.protein !== undefined
                  ? String(product.protein)
                  : "-"
              }
              value={fields.protein}
              onChange={(e) => handleChange("protein", e.target.value)}
            />
          </div>

          <div className="space-y-1">
            <label className="text-xs font-medium text-slate-700">
              Fat (g)
            </label>
            <input
              type="number"
              className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-green-500"
              placeholder={
                product.fat !== null && product.fat !== undefined
                  ? String(product.fat)
                  : "-"
              }
              value={fields.fat}
              onChange={(e) => handleChange("fat", e.target.value)}
            />
          </div>

          <div className="space-y-1">
            <label className="text-xs font-medium text-slate-700">
              Sat. fat (g)
            </label>
            <input
              type="number"
              className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-green-500"
              placeholder={
                product.satFat !== null && product.satFat !== undefined
                  ? String(product.satFat)
                  : "-"
              }
              value={fields.satFat}
              onChange={(e) => handleChange("satFat", e.target.value)}
            />
          </div>

          <div className="space-y-1">
            <label className="text-xs font-medium text-slate-700">
              Carbs (g)
            </label>
            <input
              type="number"
              className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-green-500"
              placeholder={
                product.carbs !== null && product.carbs !== undefined
                  ? String(product.carbs)
                  : "-"
              }
              value={fields.carbs}
              onChange={(e) => handleChange("carbs", e.target.value)}
            />
          </div>

          <div className="space-y-1">
            <label className="text-xs font-medium text-slate-700">
              Sugars (g)
            </label>
            <input
              type="number"
              className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-green-500"
              placeholder={
                product.sugars !== null && product.sugars !== undefined
                  ? String(product.sugars)
                  : "-"
              }
              value={fields.sugars}
              onChange={(e) => handleChange("sugars", e.target.value)}
            />
          </div>

          <div className="space-y-1">
            <label className="text-xs font-medium text-slate-700">
              Salt (mg)
            </label>
            <input
              type="number"
              className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-green-500"
              placeholder={
                product.salt !== null && product.salt !== undefined
                  ? String(product.salt)
                  : "-"
              }
              value={fields.salt}
              onChange={(e) => handleChange("salt", e.target.value)}
            />
          </div>

          <div className="space-y-1">
            <label className="text-xs font-medium text-slate-700">
              Price per 1kg (€)
            </label>
            <input
              type="number"
              className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-green-500"
              placeholder={
                product.price1kg !== null && product.price1kg !== undefined
                  ? String(product.price1kg)
                  : "-"
              }
              value={fields.price1kg}
              onChange={(e) => handleChange("price1kg", e.target.value)}
            />
          </div>

          <div className="space-y-1 sm:col-span-2">
            <label className="text-xs font-medium text-slate-700">
              Protein type <span className="text-slate-400">(optional)</span>
            </label>
            <div className="flex flex-wrap gap-2">
              <button
                type="button"
                onClick={() => handleChange("proteinType", "dairy")}
                className={`inline-flex items-center rounded-full border px-3 py-1 text-xs font-medium ${
                  fields.proteinType === "dairy"
                    ? "border-green-500 bg-green-50 text-green-700 shadow-sm"
                    : "border-slate-300 text-slate-700 hover:border-green-500 hover:text-green-600"
                }`}
              >
                Dairy protein
              </button>
              <button
                type="button"
                onClick={() => handleChange("proteinType", "animal")}
                className={`inline-flex items-center rounded-full border px-3 py-1 text-xs font-medium ${
                  fields.proteinType === "animal"
                    ? "border-green-500 bg-green-50 text-green-700 shadow-sm"
                    : "border-slate-300 text-slate-700 hover:border-green-500 hover:text-green-600"
                }`}
              >
                Animal protein
              </button>
              <button
                type="button"
                onClick={() => handleChange("proteinType", "plant")}
                className={`inline-flex items-center rounded-full border px-3 py-1 text-xs font-medium ${
                  fields.proteinType === "plant"
                    ? "border-green-500 bg-green-50 text-green-700 shadow-sm"
                    : "border-slate-300 text-slate-700 hover:border-green-500 hover:text-green-600"
                }`}
              >
                Plant protein
              </button>
              {fields.proteinType && (
                <button
                  type="button"
                  onClick={() => handleChange("proteinType", "")}
                  className="inline-flex items-center rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-medium text-slate-600 hover:bg-slate-100"
                >
                  Clear
                </button>
              )}
            </div>
          </div>
        </div>

        <div className="mt-5 flex justify-end gap-2">
          <button
            type="button"
            onClick={onClose}
            className="rounded-xl border border-slate-300 bg-slate-50 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100"
          >
            Cancel
          </button>
          <button
            type="button"
            onClick={handleSubmit}
            className="rounded-xl bg-green-500 px-4 py-2 text-sm font-semibold text-black hover:bg-green-400"
          >
            Save changes
          </button>
        </div>
      </div>
    </div>
  );
}

export default function MyProductsPage() {
  const [sidebarOpened, setSidebarOpened] = useState(false);
  const [products, setProducts] = useState([]);
  const [loadingProducts, setLoadingProducts] = useState(false);
  const [globalError, setGlobalError] = useState("");
  const [searchQuery, setSearchQuery] = useState("");
  const [activeTab, setActiveTab] = useState("manual");
  const [selectedIds, setSelectedIds] = useState([]);
  const [sortConfig, setSortConfig] = useState({
    key: "productName",
    direction: "asc",
  });

  const [manual, setManual] = useState({
    productName: "",
    kcal: "",
    fat: "",
    satFat: "",
    carbs: "",
    sugars: "",
    protein: "",
    salt: "",
    price1kg: "",
    proteinType: "",
    vegan: false,
    vegetarian: false,
    dairyFree: false,
  });

  const [rimi, setRimi] = useState({
    url: "",
    mass_g: "",
    productName: "",
    proteinType: "",
    vegan: false,
    vegetarian: false,
    dairyFree: false,
  });

  const [nv, setNv] = useState({
    url: "",
    productName: "",
    price1kg: "",
    pricePerUnit: "",
    massPerUnit: "",
    proteinType: "",
    vegan: false,
    vegetarian: false,
    dairyFree: false,
  });

  const [manualMessage, setManualMessage] = useState(null);
  const [rimiMessage, setRimiMessage] = useState(null);
  const [nvMessage, setNvMessage] = useState(null);

  const [editProduct, setEditProduct] = useState(null);
  const [loadingEdit, setLoadingEdit] = useState(false);

  const withAuth = (path, options = {}) =>
    fetch(path, {
      credentials: "include",
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...(options.headers || {}),
      },
    });

  const loadProducts = async () => {
    setGlobalError("");
    setLoadingProducts(true);
    try {
      const res = await withAuth(`${API_BASE}/getUserProducts`);
      const data = await res.json().catch(() => []);

      if (!res.ok) {
        throw new Error(
          (data && data.detail) || "Failed to load user products"
        );
      }

      setProducts(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error(err);
      setGlobalError(err.message || "Failed to load user products");
    } finally {
      setLoadingProducts(false);
    }
  };

  useEffect(() => {
    void loadProducts();
  }, []);

  const handleSort = (key) => {
    setSortConfig((prev) => {
      if (prev.key === key) {
        return {
          key,
          direction: prev.direction === "asc" ? "desc" : "asc",
        };
      }
      return { key, direction: "asc" };
    });
  };

  const displayedProducts = useMemo(() => {
    const q = searchQuery.trim().toLowerCase();
    let filtered = products;

    if (q) {
      filtered = products.filter((p) =>
        p.productName?.toLowerCase().includes(q)
      );
    }

    if (!sortConfig.key) return filtered;

    const sorted = [...filtered].sort((a, b) => {
      const { key, direction } = sortConfig;
      const aVal = a[key];
      const bVal = b[key];

      let cmp = 0;

      if (aVal == null && bVal == null) {
        cmp = 0;
      } else if (aVal == null) {
        cmp = 1;
      } else if (bVal == null) {
        cmp = -1;
      } else if (
        typeof aVal === "number" &&
        typeof bVal === "number"
      ) {
        cmp = aVal - bVal;
      } else {
        cmp = String(aVal).localeCompare(String(bVal));
      }

      return direction === "asc" ? cmp : -cmp;
    });

    return sorted;
  }, [products, searchQuery, sortConfig]);

  const resetMessages = () => {
    setManualMessage(null);
    setRimiMessage(null);
    setNvMessage(null);
    setGlobalError("");
  };

  const handleManualSubmit = async (e) => {
    e.preventDefault();
    resetMessages();

    const missing = [];
    if (!manual.productName.trim()) missing.push("productName");
    if (!manual.proteinType) missing.push("proteinType");

    if (missing.length > 0) {
      setManualMessage({
        type: "error",
        text: `Please fill required fields: ${missing.join(", ")}`,
      });
      return;
    }

    const payload = {
      productName: manual.productName.trim(),
      kcal: manual.kcal !== "" ? Number(manual.kcal) : 0,
      fat: manual.fat !== "" ? Number(manual.fat) : 0,
      satFat: manual.satFat !== "" ? Number(manual.satFat) : 0,
      carbs: manual.carbs !== "" ? Number(manual.carbs) : 0,
      sugars: manual.sugars !== "" ? Number(manual.sugars) : 0,
      protein: manual.protein !== "" ? Number(manual.protein) : 0,
      salt: manual.salt !== "" ? Number(manual.salt) : 0,
      price1kg: manual.price1kg !== "" ? Number(manual.price1kg) : 0,
      dairyProt: manual.proteinType === "dairy",
      animalProt: manual.proteinType === "animal",
      plantProt: manual.proteinType === "plant",
      vegan: !!manual.vegan,
      vegetarian: !!manual.vegetarian,
      dairyFree: !!manual.dairyFree,
    };

    try {
      const res = await withAuth(`${API_BASE}/addUserProduct`, {
        method: "POST",
        body: JSON.stringify(payload),
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        throw new Error(data.detail || "Failed to add product");
      }

      setManual({
        productName: "",
        kcal: "",
        fat: "",
        satFat: "",
        carbs: "",
        sugars: "",
        protein: "",
        salt: "",
        price1kg: "",
        proteinType: "",
        vegan: false,
        vegetarian: false,
        dairyFree: false,
      });
      setManualMessage({
        type: "success",
        text: "Product added successfully.",
      });
      setSelectedIds([]);
      void loadProducts();
    } catch (err) {
      console.error(err);
      setManualMessage({
        type: "error",
        text: err.message || "Failed to add product",
      });
    }
  };

  const handleRimiSubmit = async (e) => {
    e.preventDefault();
    resetMessages();

    if (!rimi.url.trim()) {
      setRimiMessage({
        type: "error",
        text: "Rimi product URL is required.",
      });
      return;
    }
    if (!rimi.proteinType) {
      setRimiMessage({
        type: "error",
        text: "Please select protein type.",
      });
      return;
    }

    const payload = {
      url: rimi.url.trim(),
      productName: rimi.productName.trim() || "",
      vegan: !!rimi.vegan,
      vegetarian: !!rimi.vegetarian,
      dairyFree: !!rimi.dairyFree,
    };

    if (rimi.proteinType === "dairy") {
      payload.dairyProtein = true;
    }

    if (rimi.proteinType === "animal") {
      payload.animalProtein = true;
    }

    if (rimi.proteinType === "plant") {
      payload.plantProtein = true;
    }

    if (rimi.mass_g !== "") {
      payload.mass_g = Number(rimi.mass_g);
    }

    try {
      const res = await withAuth(`${API_BASE}/addUserProductUrlRimi`, {
        method: "POST",
        body: JSON.stringify(payload),
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        throw new Error(data.detail || "Failed to add product from Rimi");
      }

      setRimi({
        url: "",
        mass_g: "",
        productName: "",
        proteinType: "",
        vegan: false,
        vegetarian: false,
        dairyFree: false,
      });
      setRimiMessage({
        type: "success",
        text: "Product added from Rimi.",
      });
      setSelectedIds([]);
      void loadProducts();
    } catch (err) {
      console.error(err);
      setRimiMessage({
        type: "error",
        text: err.message || "Failed to add product from Rimi",
      });
    }
  };

  const handleNvSubmit = async (e) => {
    e.preventDefault();
    resetMessages();

    if (!nv.url.trim()) {
      setNvMessage({
        type: "error",
        text: "NutritionValue URL is required.",
      });
      return;
    }
    if (!nv.proteinType) {
      setNvMessage({
        type: "error",
        text: "Please select protein type.",
      });
      return;
    }

    const payload = {
      url: nv.url.trim(),
      productName: nv.productName.trim() || "",
      dairyProtein: nv.proteinType === "dairy",
      animalProtein: nv.proteinType === "animal",
      plantProtein: nv.proteinType === "plant",
      vegan: !!nv.vegan,
      vegetarian: !!nv.vegetarian,
      dairyFree: !!nv.dairyFree,
    };


    if (nv.price1kg !== "") {
      payload.price1kg = Number(nv.price1kg);
    }
    if (nv.pricePerUnit !== "") {
      payload.pricePerUnit = Number(nv.pricePerUnit);
    }
    if (nv.massPerUnit !== "") {
      payload.massPerUnit = Number(nv.massPerUnit);
    }

    try {
      const res = await withAuth(
        `${API_BASE}/addUserProductUrlNutritionValue`,
        {
          method: "POST",
          body: JSON.stringify(payload),
        }
      );
      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        throw new Error(
          data.detail || "Failed to add product from NutritionValue"
        );
      }

      setNv({
        url: "",
        productName: "",
        price1kg: "",
        pricePerUnit: "",
        massPerUnit: "",
        proteinType: "",
        vegan: false,
        vegetarian: false,
        dairyFree: false,
      });
      setNvMessage({
        type: "success",
        text: "Product added from NutritionValue.",
      });
      setSelectedIds([]);
      void loadProducts();
    } catch (err) {
      console.error(err);
      setNvMessage({
        type: "error",
        text: err.message || "Failed to add product from NutritionValue",
      });
    }
  };

  const renderMessage = (msg) => {
    if (!msg) return null;
    const base = "mb-3 rounded-xl px-3 py-2 text-xs border";
    if (msg.type === "error") {
      return (
        <div
          className={`${base} border-red-300 bg-red-50 text-red-700`}
        >
          {msg.text}
        </div>
      );
    }
    if (msg.type === "success") {
      return (
        <div
          className={`${base} border-green-300 bg-green-50 text-green-700`}
        >
          {msg.text}
        </div>
      );
    }
    return (
      <div
        className={`${base} border-slate-300 bg-slate-50 text-slate-700`}
      >
        {msg.text}
      </div>
    );
  };

  const handleRowClick = (p) => {
    const id = p.id;
    setSelectedIds((prev) =>
      prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
    );
  };

  const handleEditClick = () => {
    if (selectedIds.length !== 1) return;
    const productToEdit = products.find((p) => p.id === selectedIds[0]);
    if (productToEdit) {
      setEditProduct(productToEdit);
    }
  };

  const handleEditSubmit = async (payload) => {
    resetMessages();
    setLoadingEdit(true);

    try {
      const res = await withAuth("/userProducts/updateUserProduct", {
        method: "PUT",
        body: JSON.stringify(payload),
      });

      const data = await res.json().catch(() => ({}));

      if (!res.ok) {
        throw new Error(data.detail || "Failed to update product");
      }

      setEditProduct(null);
      setSelectedIds([]);
      await loadProducts();
    } catch (err) {
      console.error(err);
      setGlobalError(err.message || "Failed to update product");
    } finally {
      setLoadingEdit(false);
    }
  };

  const handleDeleteSelected = async () => {
    resetMessages();
    if (selectedIds.length === 0) return;

    const selectedProducts = products.filter((p) =>
      selectedIds.includes(p.id)
    );
    const names = selectedProducts
      .map((p) => p.productName)
      .filter(Boolean);

    if (names.length === 0) return;

    const label =
      names.length === 1
        ? `Delete product "${names[0]}"?`
        : `Delete ${names.length} products?`;

    const confirmed = window.confirm(label);
    if (!confirmed) return;

    try {
      for (const name of names) {
        const res = await withAuth(`${API_BASE}/deleteUserProduct`, {
          method: "DELETE",
          body: JSON.stringify({ productName: name }),
        });
        const data = await res.json().catch(() => ({}));
        if (!res.ok) {
          throw new Error(data.detail || `Failed to delete "${name}"`);
        }
      }
      setSelectedIds([]);
      void loadProducts();
    } catch (err) {
      console.error(err);
      setGlobalError(
        err.message || "Failed to delete selected products"
      );
    }
  };

  const canEdit = selectedIds.length === 1 && !loadingEdit;
  const canDelete = selectedIds.length > 0;

  return (
    <div className="min-h-screen text-slate-900">
      <SidebarMenu opened={sidebarOpened} setOpened={setSidebarOpened} />

      <main
        className={`px-8 py-6 transition-all duration-300 ${
          sidebarOpened ? "ml-72" : "ml-40"
        }`}
      >
        <div className="mt-8 mb-6 flex items-center justify-between">
          <div className="flex flex-col gap-1">
            <h1 className="text-3xl font-bold tracking-tight">
              My products
            </h1>
            <p className="mt-1 text-base text-slate-600">
              Products you’ve added to your personal list.
            </p>
          </div>

          {loadingProducts && (
            <span className="text-xs text-slate-500">
              Loading products...
            </span>
          )}
        </div>

        {globalError && (
          <div className="mb-4 rounded-xl border border-red-300 bg-red-50 px-4 py-3 text-sm text-red-700">
            {globalError}
          </div>
        )}

        <div className="mt-4 grid grid-cols-1 gap-3 lg:grid-cols-[minmax(0,2.2fr)_minmax(0,1fr)]">
          <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="mb-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
              <div className="flex flex-1 gap-2">
                <input
                  type="text"
                  placeholder="Search in products..."
                  className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-green-500"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
              </div>
              <div className="flex gap-2">
                <button
                  type="button"
                  onClick={handleEditClick}
                  disabled={!canEdit}
                  className="rounded-xl border border-slate-300 bg-slate-50 px-3 py-2 text-xs font-medium text-slate-800 hover:bg-slate-100 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  {loadingEdit ? "Editing..." : "Edit selected"}
                </button>
                <button
                  type="button"
                  onClick={handleDeleteSelected}
                  disabled={!canDelete}
                  className="rounded-xl border border-red-300 bg-red-50 px-3 py-2 text-xs font-medium text-red-700 hover:bg-red-100 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  Delete selected ({selectedIds.length})
                </button>
              </div>
            </div>

            <div className="relative max-h-[65vh] overflow-y-auto rounded-xl border border-slate-200">
              <table className="min-w-full border-collapse text-base">
                <thead className="sticky top-0 z-10 bg-slate-100">
                  <tr>
                    <th className="px-3 py-2 border text-left text-sm">
                      <button
                        type="button"
                        onClick={() => handleSort("productName")}
                        className="flex items-center gap-1"
                      >
                        Name
                        {sortConfig.key === "productName" && (
                          <span>
                            {sortConfig.direction === "asc"
                              ? "▲"
                              : "▼"}
                          </span>
                        )}
                      </button>
                    </th>
                    <th className="px-3 py-2 border text-left text-sm">
                      <button
                        type="button"
                        onClick={() => handleSort("kcal")}
                        className="flex items-center gap-1"
                      >
                        Kcal
                        {sortConfig.key === "kcal" && (
                          <span>
                            {sortConfig.direction === "asc"
                              ? "▲"
                              : "▼"}
                          </span>
                        )}
                      </button>
                    </th>
                    <th className="px-3 py-2 border text-left text-sm">
                      <button
                        type="button"
                        onClick={() => handleSort("fat")}
                        className="flex items-center gap-1"
                      >
                        Fat
                        {sortConfig.key === "fat" && (
                          <span>
                            {sortConfig.direction === "asc"
                              ? "▲"
                              : "▼"}
                          </span>
                        )}
                      </button>
                    </th>
                    <th className="px-3 py-2 border text-left text-sm">
                      <button
                        type="button"
                        onClick={() => handleSort("carbs")}
                        className="flex items-center gap-1"
                      >
                        Carbs
                        {sortConfig.key === "carbs" && (
                          <span>
                            {sortConfig.direction === "asc"
                              ? "▲"
                              : "▼"}
                          </span>
                        )}
                      </button>
                    </th>
                    <th className="px-3 py-2 border text-left text-sm">
                      <button
                        type="button"
                        onClick={() => handleSort("protein")}
                        className="flex items-center gap-1"
                      >
                        Protein
                        {sortConfig.key === "protein" && (
                          <span>
                            {sortConfig.direction === "asc"
                              ? "▲"
                              : "▼"}
                          </span>
                        )}
                      </button>
                    </th>
                    <th className="px-3 py-2 border text-left text-sm">
                      <button
                        type="button"
                        onClick={() => handleSort("price1kg")}
                        className="flex items-center gap-1"
                      >
                        Price (€/kg)
                        {sortConfig.key === "price1kg" && (
                          <span>
                            {sortConfig.direction === "asc"
                              ? "▲"
                              : "▼"}
                          </span>
                        )}
                      </button>
                    </th>
                    <th className="px-3 py-2 border text-left text-sm">
                      URL
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {displayedProducts.map((p) => {
                    const isSelected = selectedIds.includes(p.id);
                    const rowClass = `
                      cursor-pointer transition-colors
                      ${isSelected
                        ? "bg-green-100 hover:bg-green-100"
                        : "odd:bg-white even:bg-slate-50 hover:bg-slate-100"}
                    `;
                    return (
                      <tr
                        key={p.id}
                        className={rowClass}
                        onClick={() => handleRowClick(p)}
                      >
                        <td className="px-3 py-2">
                          <span className="text-sm font-medium">
                            {p.productName}
                          </span>
                        </td>
                        <td className="px-3 py-2">
                          {p.kcal ?? "-"}
                        </td>
                        <td className="px-3 py-2">
                          {p.fat ?? "-"}
                        </td>
                        <td className="px-3 py-2">
                          {p.carbs ?? "-"}
                        </td>
                        <td className="px-3 py-2">
                          {p.protein ?? "-"}
                        </td>
                        <td className="px-3 py-2">
                          {p.price1kg !== null &&
                          p.price1kg !== undefined
                            ? `€${Number(p.price1kg).toFixed(2)}`
                            : "-"}
                        </td>
                        <td className="px-3 py-2">
                          {p.URL ? (
                            <a
                              href={p.URL}
                              target="_blank"
                              rel="noreferrer"
                              onClick={(e) => e.stopPropagation()}
                              className="text-xs text-brandGreen underline"
                            >
                              Open
                            </a>
                          ) : (
                            <span className="text-xs text-slate-400">
                              -
                            </span>
                          )}
                        </td>
                      </tr>
                    );
                  })}

                  {displayedProducts.length === 0 && (
                    <tr>
                      <td
                        colSpan={7}
                        className="px-3 py-4 text-center text-sm text-slate-500"
                      >
                        No products found.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </section>

          <section className="self-start rounded-2xl border border-slate-200 bg-white p-6 shadow-sm lg:sticky lg:top-24">
            <div className="mb-4 flex gap-4 border-b border-slate-200 pb-2">
              {["manual", "rimi", "nv"].map((tab) => (
                <button
                  key={tab}
                  type="button"
                  onClick={() => {
                    resetMessages();
                    setActiveTab(tab);
                  }}
                  className={`pb-1 text-sm font-medium ${
                    activeTab === tab
                      ? "border-b-2 border-green-500 text-green-600"
                      : "text-slate-500 hover:text-slate-800"
                  }`}
                >
                  {tab === "manual" && "Add manually"}
                  {tab === "rimi" && "Add from Rimi"}
                  {tab === "nv" && "Add from NutritionValue"}
                </button>
              ))}
            </div>

            <div className="max-h-[580px] overflow-y-auto pr-1 pl-2">
              {activeTab === "manual" && (
                <form onSubmit={handleManualSubmit} className="space-y-3">
                  {renderMessage(manualMessage)}

                  <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
                    <div className="space-y-1">
                      <label className="text-xs font-medium text-slate-700">
                        Product name *
                      </label>
                      <input
                        className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-green-500"
                        value={manual.productName}
                        onChange={(e) =>
                          setManual((prev) => ({
                            ...prev,
                            productName: e.target.value,
                          }))
                        }
                      />
                    </div>

                    <div className="space-y-1">
                      <label className="text-xs font-medium text-slate-700">
                        Kcal
                      </label>
                      <input
                        type="number"
                        className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-green-500"
                        value={manual.kcal}
                        onChange={(e) =>
                          setManual((prev) => ({
                            ...prev,
                            kcal: e.target.value,
                          }))
                        }
                      />
                    </div>

                    <div className="space-y-1">
                      <label className="text-xs font-medium text-slate-700">
                        Fat (g)
                      </label>
                      <input
                        type="number"
                        className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-green-500"
                        value={manual.fat}
                        onChange={(e) =>
                          setManual((prev) => ({
                            ...prev,
                            fat: e.target.value,
                          }))
                        }
                      />
                    </div>

                    <div className="space-y-1">
                      <label className="text-xs font-medium text-slate-700">
                        Saturated fat (g)
                      </label>
                      <input
                        type="number"
                        className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-green-500"
                        value={manual.satFat}
                        onChange={(e) =>
                          setManual((prev) => ({
                            ...prev,
                            satFat: e.target.value,
                          }))
                        }
                      />
                    </div>

                    <div className="space-y-1">
                      <label className="text-xs font-medium text-slate-700">
                        Carbs (g)
                      </label>
                      <input
                        type="number"
                        className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-green-500"
                        value={manual.carbs}
                        onChange={(e) =>
                          setManual((prev) => ({
                            ...prev,
                            carbs: e.target.value,
                          }))
                        }
                      />
                    </div>

                    <div className="space-y-1">
                      <label className="text-xs font-medium text-slate-700">
                        Sugars (g)
                      </label>
                      <input
                        type="number"
                        className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-green-500"
                        value={manual.sugars}
                        onChange={(e) =>
                          setManual((prev) => ({
                            ...prev,
                            sugars: e.target.value,
                          }))
                        }
                      />
                    </div>

                    <div className="space-y-1">
                      <label className="text-xs font-medium text-slate-700">
                        Protein (g)
                      </label>
                      <input
                        type="number"
                        className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-green-500"
                        value={manual.protein}
                        onChange={(e) =>
                          setManual((prev) => ({
                            ...prev,
                            protein: e.target.value,
                          }))
                        }
                      />
                    </div>

                    <div className="space-y-1">
                      <label className="text-xs font-medium text-slate-700">
                        Salt (mg)
                      </label>
                      <input
                        type="number"
                        className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-green-500"
                        value={manual.salt}
                        onChange={(e) =>
                          setManual((prev) => ({
                            ...prev,
                            salt: e.target.value,
                          }))
                        }
                      />
                    </div>

                    <div className="space-y-1">
                      <label className="text-xs font-medium text-slate-700">
                        Price per 1kg (€)
                      </label>
                      <input
                        type="number"
                        className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-green-500"
                        value={manual.price1kg}
                        onChange={(e) =>
                          setManual((prev) => ({
                            ...prev,
                            price1kg: e.target.value,
                          }))
                        }
                      />
                    </div>
                  </div>

                  <div className="space-y-1">
                    <label className="text-xs font-medium text-slate-700">
                      Protein type *
                    </label>
                    <div className="flex flex-wrap gap-2">
                      <button
                        type="button"
                        onClick={() =>
                          setManual((prev) => ({
                            ...prev,
                            proteinType: "dairy",
                          }))
                        }
                        className={`inline-flex items-center rounded-full border px-3 py-1 text-xs font-medium ${
                          manual.proteinType === "dairy"
                            ? "border-green-500 bg-green-50 text-green-700 shadow-sm"
                            : "border-slate-300 text-slate-700 hover:border-green-500 hover:text-green-600"
                        }`}
                      >
                        Dairy protein
                      </button>
                      <button
                        type="button"
                        onClick={() =>
                          setManual((prev) => ({
                            ...prev,
                            proteinType: "animal",
                          }))
                        }
                        className={`inline-flex items-center rounded-full border px-3 py-1 text-xs font-medium ${
                          manual.proteinType === "animal"
                            ? "border-green-500 bg-green-50 text-green-700 shadow-sm"
                            : "border-slate-300 text-slate-700 hover:border-green-500 hover:text-green-600"
                        }`}
                      >
                        Animal protein
                      </button>
                      <button
                        type="button"
                        onClick={() =>
                          setManual((prev) => ({
                            ...prev,
                            proteinType: "plant",
                          }))
                        }
                        className={`inline-flex items-center rounded-full border px-3 py-1 text-xs font-medium ${
                          manual.proteinType === "plant"
                            ? "border-green-500 bg-green-50 text-green-700 shadow-sm"
                            : "border-slate-300 text-slate-700 hover:border-green-500 hover:text-green-600"
                        }`}
                      >
                        Plant protein
                      </button>
                      {manual.proteinType && (
                        <button
                          type="button"
                          onClick={() =>
                            setManual((prev) => ({
                              ...prev,
                              proteinType: "",
                            }))
                          }
                          className="inline-flex items-center rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-medium text-slate-600 hover:bg-slate-100"
                        >
                          Clear
                        </button>
                      )}
                    </div>
                  </div>

                  <div className="space-y-1">
                    <div className="flex flex-wrap gap-4">
                      <label className="inline-flex items-center gap-2 text-xs text-slate-700">
                        <input
                          type="checkbox"
                          className="h-4 w-4 rounded border-slate-300 text-green-600 focus:ring-green-500"
                          checked={manual.vegan}
                          onChange={(e) =>
                            setManual((prev) => ({
                              ...prev,
                              vegan: e.target.checked,
                            }))
                          }
                        />
                        Vegan
                      </label>
                      <label className="inline-flex items-center gap-2 text-xs text-slate-700">
                        <input
                          type="checkbox"
                          className="h-4 w-4 rounded border-slate-300 text-green-600 focus:ring-green-500"
                          checked={manual.vegetarian}
                          onChange={(e) =>
                            setManual((prev) => ({
                              ...prev,
                              vegetarian: e.target.checked,
                            }))
                          }
                        />
                        Vegetarian
                      </label>
                      <label className="inline-flex items-center gap-2 text-xs text-slate-700">
                        <input
                          type="checkbox"
                          className="h-4 w-4 rounded border-slate-300 text-green-600 focus:ring-green-500"
                          checked={manual.dairyFree}
                          onChange={(e) =>
                            setManual((prev) => ({
                              ...prev,
                              dairyFree: e.target.checked,
                            }))
                          }
                        />
                        Dairy free
                      </label>
                    </div>
                  </div>

                  <button
                    type="submit"
                    className="mt-2 w-full rounded-xl bg-green-500 py-2 text-sm font-semibold text-black hover:bg-green-400"
                  >
                    Add product
                  </button>
                </form>
              )}

              {activeTab === "rimi" && (
                <form onSubmit={handleRimiSubmit} className="space-y-3">
                  {renderMessage(rimiMessage)}

                  <div className="space-y-1">
                    <label className="text-xs font-medium text-slate-700">
                      Rimi product URL *
                    </label>
                    <input
                      type="url"
                      className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-green-500"
                      placeholder="https://www.rimi.lv/..."
                      value={rimi.url}
                      onChange={(e) =>
                        setRimi((prev) => ({
                          ...prev,
                          url: e.target.value,
                        }))
                      }
                    />
                  </div>

                  <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
                    <div className="space-y-1">
                      <label className="text-xs font-medium text-slate-700">
                        Mass (g)
                      </label>
                      <input
                        type="number"
                        className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-green-500"
                        value={rimi.mass_g}
                        onChange={(e) =>
                          setRimi((prev) => ({
                            ...prev,
                            mass_g: e.target.value,
                          }))
                        }
                      />
                    </div>
                    <div className="space-y-1">
                      <label className="text-xs font-medium text-slate-700">
                        Product name
                      </label>
                      <input
                        className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-green-500"
                        value={rimi.productName}
                        onChange={(e) =>
                          setRimi((prev) => ({
                            ...prev,
                            productName: e.target.value,
                          }))
                        }
                      />
                    </div>
                  </div>

                  <div className="space-y-1">
                    <label className="text-xs font-medium text-slate-700">
                      Protein type *
                    </label>
                    <div className="flex flex-wrap gap-2">
                      <button
                        type="button"
                        onClick={() =>
                          setRimi((prev) => ({
                            ...prev,
                            proteinType: "dairy",
                          }))
                        }
                        className={`inline-flex items-center rounded-full border px-3 py-1 text-xs font-medium ${
                          rimi.proteinType === "dairy"
                            ? "border-green-500 bg-green-50 text-green-700 shadow-sm"
                            : "border-slate-300 text-slate-700 hover:border-green-500 hover:text-green-600"
                        }`}
                      >
                        Dairy protein
                      </button>
                      <button
                        type="button"
                        onClick={() =>
                          setRimi((prev) => ({
                            ...prev,
                            proteinType: "animal",
                          }))
                        }
                        className={`inline-flex items-center rounded-full border px-3 py-1 text-xs font-medium ${
                          rimi.proteinType === "animal"
                            ? "border-green-500 bg-green-50 text-green-700 shadow-sm"
                            : "border-slate-300 text-slate-700 hover-border-green-500 hover:text-green-600"
                        }`}
                      >
                        Animal protein
                      </button>
                      <button
                        type="button"
                        onClick={() =>
                          setRimi((prev) => ({
                            ...prev,
                            proteinType: "plant",
                          }))
                        }
                        className={`inline-flex items-center rounded-full border px-3 py-1 text-xs font-medium ${
                          rimi.proteinType === "plant"
                            ? "border-green-500 bg-green-50 text-green-700 shadow-sm"
                            : "border-slate-300 text-slate-700 hover:border-green-500 hover:text-green-600"
                        }`}
                      >
                        Plant protein
                      </button>
                      {rimi.proteinType && (
                        <button
                          type="button"
                          onClick={() =>
                            setRimi((prev) => ({
                              ...prev,
                              proteinType: "",
                            }))
                          }
                          className="inline-flex items-center rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-medium text-slate-600 hover:bg-slate-100"
                        >
                          Clear
                        </button>
                      )}
                    </div>
                  </div>

                  <div className="space-y-1">
                    <div className="flex flex-wrap gap-4">
                      <label className="inline-flex items-center gap-2 text-xs text-slate-700">
                        <input
                          type="checkbox"
                          className="h-4 w-4 rounded border-slate-300 text-green-600 focus:ring-green-500"
                          checked={rimi.vegan}
                          onChange={(e) =>
                            setRimi((prev) => ({
                              ...prev,
                              vegan: e.target.checked,
                            }))
                          }
                        />
                        Vegan
                      </label>
                      <label className="inline-flex items-center gap-2 text-xs text-slate-700">
                        <input
                          type="checkbox"
                          className="h-4 w-4 rounded border-slate-300 text-green-600 focus:ring-green-500"
                          checked={rimi.vegetarian}
                          onChange={(e) =>
                            setRimi((prev) => ({
                              ...prev,
                              vegetarian: e.target.checked,
                            }))
                          }
                        />
                        Vegetarian
                      </label>
                      <label className="inline-flex items-center gap-2 text-xs text-slate-700">
                        <input
                          type="checkbox"
                          className="h-4 w-4 rounded border-slate-300 text-green-600 focus:ring-green-500"
                          checked={rimi.dairyFree}
                          onChange={(e) =>
                            setRimi((prev) => ({
                              ...prev,
                              dairyFree: e.target.checked,
                            }))
                          }
                        />
                        Dairy free
                      </label>
                    </div>
                  </div>

                  <button
                    type="submit"
                    className="mt-2 w-full rounded-xl bg-green-500 py-2 text-sm font-semibold text-black hover:bg-green-400"
                  >
                    Add from Rimi
                  </button>
                </form>
              )}

              {activeTab === "nv" && (
                <form onSubmit={handleNvSubmit} className="space-y-3">
                  {renderMessage(nvMessage)}

                  <div className="space-y-1">
                    <label className="text-xs font-medium text-slate-700">
                      NutritionValue URL *
                    </label>
                    <input
                      type="url"
                      className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-green-500"
                      placeholder="https://www.nutritionvalue.org/..."
                      value={nv.url}
                      onChange={(e) =>
                        setNv((prev) => ({
                          ...prev,
                          url: e.target.value,
                        }))
                      }
                    />
                  </div>

                  <div className="space-y-1">
                    <label className="text-xs font-medium text-slate-700">
                      Product name
                    </label>
                    <input
                      className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-green-500"
                      value={nv.productName}
                      onChange={(e) =>
                        setNv((prev) => ({
                          ...prev,
                          productName: e.target.value,
                        }))
                      }
                    />
                  </div>

                  <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
                    <div className="space-y-1">
                      <label className="text-xs font-medium text-slate-700">
                        Price per 1kg (€)
                      </label>
                      <input
                        type="number"
                        className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-green-500"
                        value={nv.price1kg}
                        onChange={(e) =>
                          setNv((prev) => ({
                            ...prev,
                            price1kg: e.target.value,
                          }))
                        }
                      />
                    </div>
                    <div className="space-y-1">
                      <label className="text-xs font-medium text-slate-700">
                        Price per unit (€)
                      </label>
                      <input
                        type="number"
                        className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-green-500"
                        value={nv.pricePerUnit}
                        onChange={(e) =>
                          setNv((prev) => ({
                            ...prev,
                            pricePerUnit: e.target.value,
                          }))
                        }
                      />
                    </div>
                    <div className="space-y-1">
                      <label className="text-xs font-medium text-slate-700">
                        Mass per unit (g)
                      </label>
                      <input
                        type="number"
                        className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-green-500"
                        value={nv.massPerUnit}
                        onChange={(e) =>
                          setNv((prev) => ({
                            ...prev,
                            massPerUnit: e.target.value,
                          }))
                        }
                      />
                    </div>
                  </div>

                  <div className="space-y-1">
                    <label className="text-xs font-medium text-slate-700">
                      Protein type *
                    </label>
                    <div className="flex flex-wrap gap-2">
                      <button
                        type="button"
                        onClick={() =>
                          setNv((prev) => ({
                            ...prev,
                            proteinType: "dairy",
                          }))
                        }
                        className={`inline-flex items-center rounded-full border px-3 py-1 text-xs font-medium ${
                          nv.proteinType === "dairy"
                            ? "border-green-500 bg-green-50 text-green-700 shadow-sm"
                            : "border-slate-300 text-slate-700 hover:border-green-500 hover:text-green-600"
                        }`}
                      >
                        Dairy protein
                      </button>
                      <button
                        type="button"
                        onClick={() =>
                          setNv((prev) => ({
                            ...prev,
                            proteinType: "animal",
                          }))
                        }
                        className={`inline-flex items-center rounded-full border px-3 py-1 text-xs font-medium ${
                          nv.proteinType === "animal"
                            ? "border-green-500 bg-green-50 text-green-700 shadow-sm"
                            : "border-slate-300 text-slate-700 hover:border-green-500 hover:text-green-600"
                        }`}
                      >
                        Animal protein
                      </button>
                      <button
                        type="button"
                        onClick={() =>
                          setNv((prev) => ({
                            ...prev,
                            proteinType: "plant",
                          }))
                        }
                        className={`inline-flex items-center rounded-full border px-3 py-1 text-xs font-medium ${
                          nv.proteinType === "plant"
                            ? "border-green-500 bg-green-50 text-green-700 shadow-sm"
                            : "border-slate-300 text-slate-700 hover:border-green-500 hover:text-green-600"
                        }`}
                      >
                        Plant protein
                      </button>
                      {nv.proteinType && (
                        <button
                          type="button"
                          onClick={() =>
                            setNv((prev) => ({
                              ...prev,
                              proteinType: "",
                            }))
                          }
                          className="inline-flex items-center rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-medium text-slate-600 hover:bg-slate-100"
                        >
                          Clear
                        </button>
                      )}
                    </div>
                  </div>

                  <div className="space-y-1">
                    <div className="flex flex-wrap gap-4">
                      <label className="inline-flex items-center gap-2 text-xs text-slate-700">
                        <input
                          type="checkbox"
                          className="h-4 w-4 rounded border-slate-300 text-green-600 focus:ring-green-500"
                          checked={nv.vegan}
                          onChange={(e) =>
                            setNv((prev) => ({
                              ...prev,
                              vegan: e.target.checked,
                            }))
                          }
                        />
                        Vegan
                      </label>
                      <label className="inline-flex items-center gap-2 text-xs text-slate-700">
                        <input
                          type="checkbox"
                          className="h-4 w-4 rounded border-slate-300 text-green-600 focus:ring-green-500"
                          checked={nv.vegetarian}
                          onChange={(e) =>
                            setNv((prev) => ({
                              ...prev,
                              vegetarian: e.target.checked,
                            }))
                          }
                        />
                        Vegetarian
                      </label>
                      <label className="inline-flex items-center gap-2 text-xs text-slate-700">
                        <input
                          type="checkbox"
                          className="h-4 w-4 rounded border-slate-300 text-green-600 focus:ring-green-500"
                          checked={nv.dairyFree}
                          onChange={(e) =>
                            setNv((prev) => ({
                              ...prev,
                              dairyFree: e.target.checked,
                            }))
                          }
                        />
                        Dairy free
                      </label>
                    </div>
                  </div>

                  <button
                    type="submit"
                    className="mt-2 w-full rounded-xl bg-green-500 py-2 text-sm font-semibold text-black hover:bg-green-400"
                  >
                    Add from URL
                  </button>
                </form>
              )}
            </div>
          </section>
        </div>

        <div className="mt-6">
          <Footer />
        </div>
      </main>

      {editProduct && (
        <EditModal
          product={editProduct}
          onClose={() => setEditProduct(null)}
          onSubmit={handleEditSubmit}
        />
      )}
    </div>
  );
}
