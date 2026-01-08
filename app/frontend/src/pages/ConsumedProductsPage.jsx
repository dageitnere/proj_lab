import { useEffect, useMemo, useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import SidebarMenu from "../components/SidebarMenu.jsx";
import CalendarPopup from "../components/CalendarPopup.jsx";
import Footer from "../components/Footer.jsx";

const API_BASE = "/consumedProducts";

export default function ConsumedProductsPage() {
  const [sidebarOpened, setSidebarOpened] = useState(false);

  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const todayISO = new Date().toISOString().split("T")[0];

  const [productName, setProductName] = useState("");
  const [mass, setMass] = useState("");

  const [addDate, setAddDate] = useState(todayISO);
  const [filterDate, setFilterDate] = useState(todayISO);
  const [showAddCalendar, setShowAddCalendar] = useState(false);
  const [showFilterCalendar, setShowFilterCalendar] = useState(false);

  const [allNames, setAllNames] = useState([]);
  const [suggestions, setSuggestions] = useState([]);
  const [currentFilter, setCurrentFilter] = useState("all");

  const [searchQuery, setSearchQuery] = useState("");
  const [selectedIds, setSelectedIds] = useState([]);

  const navigate = useNavigate();

  const inputRef = useRef(null);

  const [sortConfig, setSortConfig] = useState({
    key: "createdAt",
    direction: "desc",
  });

  const withAuth = async (path, options = {}) => {
    const res = await fetch(path, {
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        "X-Requested-With": "XMLHttpRequest",
      },
      ...options,
    });

    if (res.redirected) {
      throw new Error("Authentication failed (redirected to HTML)");
    }

    const contentType = res.headers.get("content-type");
    if (!contentType || !contentType.includes("application/json")) {
      const text = await res.text();
      console.error("NOT JSON RESPONSE:", text);
      throw new Error("Server returned HTML instead of JSON");
    }

    return res;
  };

  const formatDateDMY = (date) => {
    if (!date) return "";
    const d = new Date(date);
    const dd = String(d.getDate()).padStart(2, "0");
    const mm = String(d.getMonth() + 1).padStart(2, "0");
    const yyyy = d.getFullYear();
    return `${dd}/${mm}/${yyyy}`;
  };


  const showTempMessage = (setter, msg) => {
    setter(msg);
    setTimeout(() => setter(""), 5000);
  };

  useEffect(() => {
    loadAll();
    loadNames()
  }, []);

  const loadAll = async () => {
    setCurrentFilter("all");

        try {
          setLoading(true);
          const res = await withAuth(`${API_BASE}/list`);
          const data = await res.json();
          setProducts(data.products || []);
        } catch (err) {
          setError(err.message);
          setProducts([]);
        } finally {
          setLoading(false);
        }
      };

    const loadNames = async () => {
      try {
        const [a, b] = await Promise.all([
          withAuth("/products/productsNames"),
          withAuth("/userProducts/userProductsNames"),
        ]);

        const aData = await a.json();
        const bData = await b.json();

        const all = [
          ...(aData.products || []),
          ...(bData.products || []),
        ];

        setAllNames([...new Set(all)]);
      } catch (e) {
        console.error("Failed to load product names", e);
      }
    };

      const loadProducts = async (endpoint) => {
        setLoading(true);
        setError("");

      try {
        const res = await withAuth(`${API_BASE}${endpoint}`);
        const data = await res.json();

        if (Array.isArray(data)) {
          setProducts(data);
        } else if (Array.isArray(data?.products)) {
          setProducts(data.products);
        } else {
          setProducts([]);
        }
      } catch (err) {
        setError(err.message);
        setProducts([]);
      } finally {
        setLoading(false);
      }
    };

  const toLocalISODate = (date) => {
    const d = new Date(date);
    const yyyy = d.getFullYear();
    const mm = String(d.getMonth() + 1).padStart(2, "0");
    const dd = String(d.getDate()).padStart(2, "0");
    return `${yyyy}-${mm}-${dd}`;
  };

  const loadBySingleDate = async () => {
  if (!filterDate) return;

  setLoading(true);
  setError("");
  setCurrentFilter("byDate");

  console.log("SENDING DATE:", filterDate);

  try {
    const res = await withAuth(`${API_BASE}/byDate`, {
      method: "POST",
      body: JSON.stringify({ date: filterDate }),
    });

    const data = await res.json();

    console.log("RECEIVED:", data);

    setProducts(Array.isArray(data) ? data : []);
  } catch (err) {
    setError(err.message);
    setProducts([]);
  } finally {
    setLoading(false);
  }
};


  const reloadCurrentFilter = () => {
    switch (currentFilter) {
      case "today":
        loadProducts("/today");
        break;
      case "last7":
        loadProducts("/last7days");
        break;
      case "last30":
        loadProducts("/last30days");
        break;
      case "byDate":
        loadBySingleDate();
        break;
      default:
        loadAll("/all");
    }
  };

  const handleAdd = async () => {
    if (!productName || !mass) {
      showTempMessage(setError, "Please fill in all fields");
      return;
    }

    const fullDate = `${addDate} ${new Date().toLocaleTimeString("en-GB", {
      hour12: false,
    })}`;

    try {
      setLoading(true);
      setError("");

      const res = await withAuth(`${API_BASE}/saveConsumedProduct`, {
        method: "POST",
        body: JSON.stringify({
          productName: productName.trim(),
          amount: Number(mass),
          date: fullDate,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || "Failed to add product");
      }

      setProductName("");
      setMass("");
      setSuggestions([]);

      showTempMessage(setSuccess, "Product added successfully");
      reloadCurrentFilter();

    } catch (err) {
      showTempMessage(setError, err.message || "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  const handleSuggest = (value) => {
    setProductName(value);

    const v = value.trim().toLowerCase();

    if (!v) {
      setSuggestions(allNames.slice(0, 10));
      return;
    }

    setSuggestions(allNames.filter((p) => p.toLowerCase().includes(v)).slice(0, 10));
  };

  const filterButtonClass = (key) =>
    `rounded-xl px-3 py-1.5 text-sm font-semibold border transition
     focus:outline-none
     ${
       currentFilter === key
         ? "bg-green-500 text-black border-green-500"
         : "bg-white text-slate-800 border-slate-300 hover:bg-slate-50"
     }`;

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

  const handleRowClick = (p) => {
      setSelectedIds((prev) =>
        prev.includes(p.id)
          ? prev.filter((id) => id !== p.id)
          : [...prev, p.id]
      );
    };

  const displayedProducts = useMemo(() => {
      let filtered = products;

      const q = searchQuery.trim().toLowerCase();
      if (q) {
        filtered = filtered.filter((p) =>
          p.productName?.toLowerCase().includes(q)
        );
      }

      const { key, direction } = sortConfig;
      if (!key) return filtered;

      return [...filtered].sort((a, b) => {
        const aVal = a[key];
        const bVal = b[key];

        let cmp = 0;

        if (aVal == null && bVal == null) cmp = 0;
        else if (aVal == null) cmp = 1;
        else if (bVal == null) cmp = -1;
        else if (key === "createdAt") {
          cmp = new Date(aVal) - new Date(bVal);
        } else if (typeof aVal === "number") {
          cmp = aVal - bVal;
        } else {
          cmp = String(aVal).localeCompare(String(bVal));
        }

        return direction === "asc" ? cmp : -cmp;
      });
    }, [products, searchQuery, sortConfig]);

  const handleDeleteSelected = async () => {
      if (selectedIds.length === 0) return;

      const confirmed = window.confirm(
        `Delete ${selectedIds.length} consumed products?`
      );
      if (!confirmed) return;

      try {
        for (const id of selectedIds) {
          await withAuth(`${API_BASE}/deleteProduct`, {
            method: "DELETE",
            body: JSON.stringify({ productId: id }),
          });
        }

        setSelectedIds([]);
        reloadCurrentFilter();
      } catch (err) {
        setError(err.message);
      }
    };

  const columns = [
    { label: "Product", key: "productName" },
    { label: "Mass", key: "mass" },
    { label: "Kcal", key: "kcal" },
    { label: "Fat (g)", key: "fat" },
    { label: "Carbs (g)", key: "carbs" },
    { label: "Protein (g)", key: "protein" },
    { label: "Date", key: "createdAt" },
  ];

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
        className={`px-8 py-6 transition-all duration-300 ${
          sidebarOpened ? "ml-72" : "ml-40"
        }`}
      >
        <div className="mt-8 mb-6">
          <h1 className="text-3xl font-bold tracking-tight">
            Consumed products
          </h1>
          <p className="mt-1 text-base text-slate-600">
            Track what you have eaten over time.
          </p>
        </div>

        {error && (
          <div className="mb-4 rounded-xl border border-red-300 bg-red-50 px-4 py-3 text-sm text-red-700">
            {error}
          </div>
        )}

        {success && (
          <div className="mb-4 rounded-xl border border-green-300 bg-green-50 px-4 py-3 text-sm text-green-700">
            {success}
          </div>
        )}

        <section className="mb-6 rounded-2xl border bg-white p-6 shadow-sm">
          <h3 className="mb-3 font-semibold">Add new product</h3>

          <div className="grid grid-cols-1 gap-4 lg:grid-cols-4">
            <div className="relative">
              <input ref={inputRef}
                className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm
                           focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
                placeholder="Product name"
                value={productName}
                onChange={(e) => handleSuggest(e.target.value)}
                onFocus={() => {
                  setSuggestions(allNames.slice(0, 10));
                }}
                onBlur={() => {
                  setTimeout(() => setSuggestions([]), 150);
                }}
              />

              {suggestions.length > 0 && (
                <div className="absolute z-10 mt-1 w-full rounded-lg border bg-white shadow max-h-64 overflow-y-auto">
                  {suggestions.map((s) => (
                    <div
                      key={s}
                      onMouseDown={(e) => {
                        e.preventDefault();
                        setProductName(s);
                        setSuggestions([]);
                        inputRef.current?.blur();
                      }}
                      className="cursor-pointer px-3 py-2 text-sm hover:bg-slate-100"
                    >
                      {s}
                    </div>
                  ))}
                </div>
              )}
            </div>

            <input
              type="number"
              className="rounded-xl border border-slate-300 px-3 py-2 text-sm
                         focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 "
              placeholder="Mass (g)"
              value={mass}
              onChange={(e) => setMass(e.target.value)}
            />

            <div className="relative">
              <button
                type="button"
                onClick={() => setShowAddCalendar(true)}
                className="w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm text-left hover:bg-slate-50"
              >
                {formatDateDMY(addDate)}
              </button>

              {showAddCalendar && (
                <div className="absolute z-50 mt-2">
                  <CalendarPopup
                    initialDate={new Date(addDate)}
                    onApply={(selectedDate) => {
                      setAddDate(toLocalISODate(selectedDate));
                      setShowAddCalendar(false);
                    }}
                    onCancel={() => setShowAddCalendar(false)}
                  />
                </div>
              )}
            </div>

            <button
              onClick={handleAdd}
              className="rounded-xl bg-green-500 py-2 text-sm font-semibold text-black hover:bg-green-400"
            >
              Add product
            </button>
          </div>
        </section>

        <section className="mb-6 rounded-2xl border bg-white p-6 shadow-sm">
          <h3 className="mb-3 font-semibold">Filter by date</h3>

          <div className="flex flex-wrap gap-4 items-end">
            <div className="relative">
              <label className="block text-sm font-semibold mb-1">Date</label>

              <button
                type="button"
                onClick={() => setShowFilterCalendar(true)}
                className="w-[160px] rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm text-left hover:bg-slate-50"
              >
                {filterDate ? formatDateDMY(filterDate) : "Select date"}
              </button>

              {showFilterCalendar && (
                <div className="absolute z-50 mt-2">
                  <CalendarPopup
                    initialDate={new Date(filterDate)}
                    onApply={(d) => {
                      setFilterDate(toLocalISODate(d));
                      setShowFilterCalendar(false);
                    }}
                    onCancel={() => setShowFilterCalendar(false)}
                  />
                </div>
              )}
            </div>

            <button
              onClick={loadBySingleDate}
              disabled={!filterDate || loading}
              className={filterButtonClass("byDate")}
            >
              Search
            </button>

            <div className="flex gap-2">
              <button onClick={loadAll} className={filterButtonClass("all")}>All</button>
              <button onClick={() => { setCurrentFilter("today"); loadProducts("/today"); }} className={filterButtonClass("today")}>Today</button>
              <button onClick={() => { setCurrentFilter("last7"); loadProducts("/last7days"); }} className={filterButtonClass("last7")}>Last 7 days</button>
              <button onClick={() => { setCurrentFilter("last30"); loadProducts("/last30days"); }} className={filterButtonClass("last30")}>Last 30 days</button>
            </div>
          </div>
        </section>

        <section className="rounded-2xl border bg-white p-6 shadow-sm">
          <div className="relative max-h-[65vh] overflow-y-auto border-slate-200">
            <div className="ml-3 mt-2 mb-4 flex items-center gap-2">
              <input
                type="text"
                placeholder="Search in consumed products..."
                className="
                  flex-1
                  rounded-xl
                  border border-slate-300
                  bg-slate-50
                  px-3 py-2
                  text-sm text-slate-900
                  focus:outline-none
                  focus:ring-2 focus:ring-green-500
                "
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />

              <button
                type="button"
                onClick={handleDeleteSelected}
                disabled={selectedIds.length === 0}
                className="
                  rounded-xl
                  border border-red-300
                  bg-red-50
                  px-3 py-2
                  text-xs font-medium
                  text-red-700
                  hover:bg-red-100
                  disabled:cursor-not-allowed
                  disabled:opacity-60
                "
              >
                Delete selected ({selectedIds.length})
              </button>
            </div>
            <table className="min-w-full border-collapse text-base">
              <thead className="sticky top-0 z-10 bg-slate-100">
                <tr>
                  {columns.map((col) => (
                    <th
                      key={col.label}
                      className="px-3 py-2 text-left text-sm font-semibold"
                    >
                      {col.key ? (
                        <button
                          type="button"
                          onClick={() => handleSort(col.key)}
                          className="flex items-center gap-1 hover:underline"
                        >
                          {col.label}
                          {sortConfig.key === col.key && (
                            <span className="text-xs">
                              {sortConfig.direction === "asc" ? "▲" : "▼"}
                            </span>
                          )}
                        </button>
                      ) : (
                        col.label
                      )}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                  {displayedProducts.map((p) => {
                    const isSelected = selectedIds.includes(p.id);

                    const rowClass = `
                      cursor-pointer transition-colors
                      ${
                        isSelected
                          ? "bg-green-100 hover:bg-green-100 "
                          : "odd:bg-white even:bg-slate-50 hover:bg-slate-100"
                      }
                    `;

                    return (
                      <tr
                        key={p.id}
                        className={rowClass}
                        onClick={() => handleRowClick(p)}
                      >
                        <td className="px-3 py-2 font-medium">
                          {p.productName}
                        </td>
                        <td className="px-3 py-2">{p.amount}</td>
                        <td className="px-3 py-2">{p.kcal?.toFixed(2)}</td>
                        <td className="px-3 py-2">{p.fat?.toFixed(2)}</td>
                        <td className="px-3 py-2">{p.carbs?.toFixed(2)}</td>
                        <td className="px-3 py-2">{p.protein?.toFixed(2)}</td>
                        <td className="px-3 py-2">
                          {formatDateDMY(p.createdAt)}
                        </td>
                      </tr>
                    );
                  })}

                {!loading && products.length === 0 && (
                  <tr>
                    <td
                      colSpan={8}
                      className="px-4 py-6 text-center text-slate-500"
                    >
                      No consumed products found
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </section>

        <div className="mt-6">
          <Footer />
        </div>
      </main>
    </div>
  );
}
