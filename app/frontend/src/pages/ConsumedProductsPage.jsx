import { useEffect, useMemo, useState } from "react";
import SidebarMenu from "../components/SidebarMenu.jsx";
import CalendarPopup from "../components/CalendarPopup.jsx";
import Footer from "../components/Footer.jsx";

const API_BASE = "/consumedProducts";
const PRODUCTS_API = "/products";
const USER_PRODUCTS_API = "/userProducts";

export default function ConsumedProductsPage() {
  const [sidebarOpened, setSidebarOpened] = useState(false);

  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const todayISO = new Date().toISOString().split("T")[0];
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(todayISO);
  const [showStartCalendar, setShowStartCalendar] = useState(false);
  const [showEndCalendar, setShowEndCalendar] = useState(false);

  const [productName, setProductName] = useState("");
  const [amount, setAmount] = useState("");
  const [date, setDate] = useState(
    new Date().toISOString().split("T")[0]
  );
  const [showDateCalendar, setShowDateCalendar] = useState(false);

  const [productNames, setProductNames] = useState([]);
  const [userProductNames, setUserProductNames] = useState([]);

  const allProductNames = useMemo(
    () => [...new Set([...productNames, ...userProductNames])],
    [productNames, userProductNames]
  );

  const [suggestions, setSuggestions] = useState([]);
  const [currentFilter, setCurrentFilter] = useState("all");

  const [searchQuery, setSearchQuery] = useState("");
  const [selectedIds, setSelectedIds] = useState([]);

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

  const formatDateDMY = (dateStr) => {
    if (!dateStr) return "";
    const d = new Date(dateStr);
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
    loadProductNames();
    loadUserProductNames();
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

  const loadByDateRange = async () => {
      if (!startDate || !endDate) return;

      setLoading(true);
      setError("");
      setCurrentFilter("byDate");

      const start = `${startDate} 00:00:00`;
      const end = `${endDate} 23:59:59`;

      try {
        const res = await withAuth(`${API_BASE}/byDate`, {
          method: "POST",
          body: JSON.stringify({
            startDate: start,
            endDate: end,
          }),
        });

        const data = await res.json();
        setProducts(Array.isArray(data) ? data : []);
      } catch (err) {
        setError(err.message);
        setProducts([]);
      } finally {
        setLoading(false);
      }
    };

  const loadProductNames = async () => {
    try {
      const res = await withAuth(`${PRODUCTS_API}/productsNames`);
      const data = await res.json();
      setProductNames(data.productNames || []);
    } catch (e) {
      console.error(e);
    }
  };

  const loadUserProductNames = async () => {
    try {
      const res = await withAuth(`${USER_PRODUCTS_API}/userProductsNames`);
      const data = await res.json();
      setUserProductNames(data.productNames || []);
    } catch (e) {
      console.error(e);
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
        loadByDateRange();
        break;
      default:
        loadAll("/all");
    }
  };

  const handleAdd = async () => {
    if (!productName || !amount) {
      showTempMessage(setError, "Please fill in all fields");
      return;
    }

    const fullDate = `${date} ${new Date().toLocaleTimeString("en-GB", {
      hour12: false,
    })}`;

    try {
      setLoading(true);

      await withAuth(`${API_BASE}/saveConsumedProduct`, {
        method: "POST",
        body: JSON.stringify({
          productName,
          amount: Number(amount),
          date: fullDate,
        }),
      });

      setProductName("");
      setAmount("");
      setSuggestions([]);
      showTempMessage(setSuccess, "Product added successfully");
      reloadCurrentFilter();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Delete this product?")) return;

    try {
      await withAuth(`${API_BASE}/deleteProduct`, {
        method: "DELETE",
        body: JSON.stringify({ productId: id }),
      });

      reloadCurrentFilter();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleSuggest = (value) => {
    setProductName(value);

    if (!value.trim()) {
      setSuggestions([]);
      return;
    }

    setSuggestions(
      allProductNames
        .filter((p) => p.toLowerCase().includes(value.toLowerCase()))
        .slice(0, 10)
    );
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
    { label: "Amount", key: "amount" },
    { label: "Kcal", key: "kcal" },
    { label: "Protein", key: "protein" },
    { label: "Carbs", key: "carbs" },
    { label: "Fat", key: "fat" },
    { label: "Date", key: "createdAt" },
  ];

  return (
    <div className="min-h-screen bg-noise-light text-slate-900">
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
              <input
                className="w-full rounded-xl border px-3 py-2 text-sm"
                placeholder="Product name"
                value={productName}
                onChange={(e) => handleSuggest(e.target.value)}
              />

              {suggestions.length > 0 && (
                <div className="absolute z-10 mt-1 w-full rounded-lg border bg-white shadow">
                  {suggestions.map((s) => (
                    <div
                      key={s}
                      onClick={() => {
                        setProductName(s);
                        setSuggestions([]);
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
              className="rounded-xl border px-3 py-2 text-sm"
              placeholder="Amount (g)"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
            />

            <div className="relative">
              <button
                type="button"
                onClick={() => setShowDateCalendar(true)}
                className="w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm text-left hover:bg-slate-50"
              >
                {formatDateDMY(date)}
              </button>

              {showDateCalendar && (
                <div className="absolute z-50 mt-2">
                  <CalendarPopup
                    initialDate={new Date(date)}
                    onApply={(selectedDate) => {
                      setDate(selectedDate.toISOString().split("T")[0]);
                      setShowDateCalendar(false);
                    }}
                    onCancel={() => setShowDateCalendar(false)}
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
          <h3 className="mb-3 font-semibold">Filters</h3>
          <div className="flex flex-wrap gap-6 items-end">
            <div className="relative">
              <label className="block text-sm font-semibold text-slate-800 mb-1">
                Start date
              </label>
              <button
                type="button"
                onClick={() => setShowStartCalendar(true)}
                className="w-[160px] rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm text-left hover:bg-slate-50"
              >
                {startDate ? formatDateDMY(startDate) : "Select date"}
              </button>

              {showStartCalendar && (
                <div className="absolute z-50 mt-2">
                  <CalendarPopup
                    initialDate={startDate ? new Date(startDate) : new Date()}
                    onApply={(d) => {
                      setStartDate(d.toISOString().split("T")[0]);
                      setShowStartCalendar(false);
                    }}
                    onCancel={() => setShowStartCalendar(false)}
                  />
                </div>
              )}
            </div>

            <div className="relative">
              <label className="block text-sm font-semibold text-slate-800 mb-1">
                End date
              </label>
              <button
                type="button"
                onClick={() => setShowEndCalendar(true)}
                className="w-[160px] rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm text-left hover:bg-slate-50"
              >
                {endDate ? formatDateDMY(endDate) : "Select date"}
              </button>

              {showEndCalendar && (
                <div className="absolute z-50 mt-2">
                  <CalendarPopup
                    initialDate={endDate ? new Date(endDate) : new Date()}
                    onApply={(d) => {
                      setEndDate(d.toISOString().split("T")[0]);
                      setShowEndCalendar(false);
                    }}
                    onCancel={() => setShowEndCalendar(false)}
                  />
                </div>
              )}
            </div>

            <button
              disabled={!startDate || !endDate || loading}
              onClick={loadByDateRange}
              className={filterButtonClass("byDate")}
            >
              Range
            </button>

            <div className="flex gap-2">
              <button onClick={loadAll} className={filterButtonClass("all")}>
                All
              </button>
              <button
                onClick={() => {
                  setCurrentFilter("today");
                  loadProducts("/today");
                }}
                className={filterButtonClass("today")}
              >
                Today
              </button>
              <button
                onClick={() => {
                  setCurrentFilter("last7");
                  loadProducts("/last7days");
                }}
                className={filterButtonClass("last7")}
              >
                Last 7 days
              </button>
              <button
                onClick={() => {
                  setCurrentFilter("last30");
                  loadProducts("/last30days");
                }}
                className={filterButtonClass("last30")}
              >
                Last 30 days
              </button>
            </div>
          </div>
        </section>

        <section className="rounded-2xl border bg-white p-6 shadow-sm">
          <div className="relative max-h-[65vh] overflow-y-auto border-slate-200">
            <div className="mb-4 flex items-center gap-2">
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
                          ? "bg-green-100 hover:bg-green-100"
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
                        <td className="px-3 py-2">{p.protein?.toFixed(2)}</td>
                        <td className="px-3 py-2">{p.carbs?.toFixed(2)}</td>
                        <td className="px-3 py-2">{p.fat?.toFixed(2)}</td>
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
