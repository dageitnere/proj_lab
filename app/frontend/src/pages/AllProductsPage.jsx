import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import SidebarMenu from "../components/SidebarMenu.jsx";
import Footer from "../components/Footer.jsx";

export default function AllProductsPage() {
  const [sidebarOpened, setSidebarOpened] = useState(false);
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");

  const [selectedIds, setSelectedIds] = useState([]);

  const navigate = useNavigate();

  const [sortConfig, setSortConfig] = useState({
    key: "productName",
    direction: "asc",
  });

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const res = await fetch("/products/getAllProducts", {
          credentials: "include",
        });
        if (!res.ok) throw new Error(`Error ${res.status}`);
        const data = await res.json();
        setProducts(data.products || []);
      } catch (err) {
        setError(err.message || "Failed to load products");
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
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
    let filtered = products;

    if (search.trim()) {
      const q = search.toLowerCase();
      filtered = filtered.filter((p) =>
        p.productName?.toLowerCase().includes(q)
      );
    }

    const { key, direction } = sortConfig;

    return [...filtered].sort((a, b) => {
      const aVal = a[key];
      const bVal = b[key];

      if (aVal == null && bVal == null) return 0;
      if (aVal == null) return 1;
      if (bVal == null) return -1;

      let cmp =
        typeof aVal === "number"
          ? aVal - bVal
          : String(aVal).localeCompare(String(bVal));

      return direction === "asc" ? cmp : -cmp;
    });
  }, [products, search, sortConfig]);

  const SortHeader = ({ label, column }) => (
    <button
      type="button"
      onClick={() => handleSort(column)}
      className="flex items-center gap-1 font-semibold"
    >
      {label}
      {sortConfig.key === column && (
        <span>{sortConfig.direction === "asc" ? "▲" : "▼"}</span>
      )}
    </button>
  );

  const toggleRow = (id) => {
    setSelectedIds((prev) =>
      prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
    );
  };

  const addSelectedToMyProducts = async () => {
    if (selectedIds.length === 0) return;

    const selectedProducts = products.filter((p) =>
      selectedIds.includes(p.id)
    );

    try {
      for (const p of selectedProducts) {
        const payload = {
          productName: p.productName,
          kcal: p.kcal ?? 0,
          fat: p.fat ?? 0,
          satFat: p.satFat ?? 0,
          carbs: p.carbs ?? 0,
          sugars: p.sugars ?? 0,
          protein: p.protein ?? 0,
          salt: p.salt ?? 0,
          price1kg: p.price1kg ?? 0,
          dairyProt: !!p.dairyProt,
          animalProt: !!p.animalProt,
          plantProt: !!p.plantProt,
        };

        const res = await fetch("/userProducts/addUserProduct", {
          method: "POST",
          credentials: "include",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });

        if (!res.ok) {
          const data = await res.json().catch(() => ({}));
          throw new Error(data.detail || "Failed to add product");
        }
      }

      alert(`${selectedIds.length} product(s) added to My Products`);
      setSelectedIds([]);
    } catch (err) {
      alert(err.message);
    }
  };

  return (
    <div className="relative min-h-screen bg-noise-light text-slate-900">
          <button
          type="button"
          onClick={() => navigate("/new-page")}
          className="
            absolute right-8 top-8
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
      <SidebarMenu opened={sidebarOpened} setOpened={setSidebarOpened} />

      <main
        className={`pl-56 pr-8 py-6 transition-all duration-300 ${
          sidebarOpened ? "ml-32" : "ml-0"
        }`}
      >
        <div className="mt-8 mb-6 flex items-center justify-between">
          <div className="flex flex-col gap-1">
            <h1 className="text-3xl font-bold tracking-tight">
              All products
            </h1>
            <p className="mt-1 text-base text-slate-600">
              Full list of available products and nutrition values.
            </p>
          </div>
        </div>

          {error && (
            <div className="mb-4 rounded-xl border border-red-300 bg-red-50 px-4 py-3 text-red-700">
              {error}
            </div>
          )}

          <section className="rounded-2xl bg-white border border-slate-200 p-6 shadow-sm">
            <div className="mb-4 flex items-center gap-3 p-6 pb-0">
              <input
                type="text"
                placeholder="Search product..."
                className="w-full rounded-xl border border-slate-300 px-4 py-2 outline-none focus:border-green-500 focus:ring-2 focus:ring-green-500 focus:ring-offset-0"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />

              <button
                onClick={addSelectedToMyProducts}
                disabled={selectedIds.length === 0}
                className="whitespace-nowrap rounded-xl bg-green-500 px-4 py-2 text-sm font-medium text-black hover:bg-green-400 disabled:opacity-50"
              >
                Add selected ({selectedIds.length})
              </button>
            </div>

            {loading && (
              <p className="text-slate-500">Loading products...</p>
            )}

            {!loading && (
              <div className="relative max-h-[65vh] overflow-y-auto rounded-xl border border-slate-200">
                <table className="min-w-full border-separate border-spacing-0">
                  <thead className="sticky top-0 z-10 bg-slate-100">
                    <tr>
                      <th className="px-3 py-2 border text-left text-sm">
                        <SortHeader label="Product" column="productName" />
                      </th>
                      <th className="px-3 py-2 border text-sm">
                        <SortHeader label="Kcal" column="kcal" />
                      </th>
                      <th className="px-3 py-2 border text-sm">
                        <SortHeader label="Fat (g)" column="fat" />
                      </th>
                      <th className="px-3 py-2 border text-sm">
                        <SortHeader label="Saturated fat (g)" column="satFat" />
                      </th>
                      <th className="px-3 py-2 border text-sm">
                        <SortHeader label="Carbs (g)" column="carbs" />
                      </th>
                      <th className="px-3 py-2 border text-sm">
                        <SortHeader label="Sugars (g)" column="sugars" />
                      </th>
                      <th className="px-3 py-2 border text-sm">
                        <SortHeader label="Protein (g)" column="protein" />
                      </th>
                      <th className="px-3 py-2 border text-sm">
                        <SortHeader label="Dairy protein (g)" column="dairyProt" />
                      </th>
                      <th className="px-3 py-2 border text-sm">
                        <SortHeader label="Animal protein (g)" column="animalProt" />
                      </th>
                      <th className="px-3 py-2 border text-sm">
                        <SortHeader label="Plant protein (g)" column="plantProt" />
                      </th>
                      <th className="px-3 py-2 border text-sm">
                        <SortHeader label="Salt (mg)" column="salt" />
                      </th>
                      <th className="px-3 py-2 border text-sm">
                        <SortHeader label="Price (€/kg)" column="price1kg" />
                      </th>
                      <th className="px-3 py-2 border text-sm">
                        <SortHeader label="Price (€/100g)" column="price100g" />
                      </th>
                    </tr>
                  </thead>

                  <tbody>
                    {displayedProducts.map((p) => {
                      const selected = selectedIds.includes(p.id);
                      return (
                        <tr
                          key={p.id}
                          onClick={() => toggleRow(p.id)}
                          className={`cursor-pointer transition-colors ${
                            selected
                              ? "bg-green-100 hover:bg-green-100"
                              : "odd:bg-white even:bg-slate-50 hover:bg-slate-100"
                          }`}
                        >
                          <td className="px-3 py-2 border font-medium">
                            {p.productName}
                          </td>
                          <td className="px-3 py-2 border">{p.kcal ?? "-"}</td>
                          <td className="px-3 py-2 border">{p.fat ?? "-"}</td>
                          <td className="px-3 py-2 border">{p.satFat ?? "-"}</td>
                          <td className="px-3 py-2 border">{p.carbs ?? "-"}</td>
                          <td className="px-3 py-2 border">{p.sugars ?? "-"}</td>
                          <td className="px-3 py-2 border">{p.protein ?? "-"}</td>
                          <td className="px-3 py-2 border">{p.dairyProt ?? "-"}</td>
                          <td className="px-3 py-2 border">{p.animalProt ?? "-"}</td>
                          <td className="px-3 py-2 border">{p.plantProt ?? "-"}</td>
                          <td className="px-3 py-2 border">{p.salt ?? "-"}</td>
                          <td className="px-3 py-2 border">{Number(p.price1kg).toFixed(2) ?? "-"}</td>
                          <td className="px-3 py-2 border">{Number(p.price100g).toFixed(2) ?? "-"}</td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            )}
          </section>

          <div className="mt-6">
            <Footer />
          </div>
      </main>
    </div>
  );
}
