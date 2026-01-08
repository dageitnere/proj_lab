import { useState } from "react";
import { useNavigate } from "react-router-dom";
import SidebarMenu from "../components/SidebarMenu.jsx";
import Footer from "../components/Footer.jsx";
import Kpi from "../components/Kpi.jsx";
import AverageMacrosBar from "../components/AverageMacrosBar.jsx";
import ProteinDonutChart from "../components/ProteinDonutChart.jsx";
import FatCompositionBar from "../components/FatCompositionBar.jsx";
import SugarSaltBar from "../components/SugarSaltBar.jsx";
import CalendarPopup from "../components/CalendarPopup.jsx";

const toIsoDate = (date) => date.toISOString().split("T")[0];

export default function StatisticsPage() {
  const [sidebarOpened, setSidebarOpened] = useState(false);

  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const navigate = useNavigate();

  const [activePeriod, setActivePeriod] = useState(null);

  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(new Date());

  const [showStartCalendar, setShowStartCalendar] = useState(false);
  const [showEndCalendar, setShowEndCalendar] = useState(false);

  const fetchStats = async (url, options = {}, periodKey = null) => {
    try {
      setLoading(true);
      setError("");
      setActivePeriod(periodKey);

      const res = await fetch(url, {
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        ...options,
      });

      if (!res.ok) {
        throw new Error(`Error ${res.status}`);
      }

      const data = await res.json();
      setStats(data);
    } catch (err) {
      setError(err.message || "Failed to load statistics");
    } finally {
      setLoading(false);
    }
  };

  const periodButtonClass = (key) =>
    `rounded-xl px-4 py-2 text-sm font-semibold border transition
    focus:outline-none
    ${
      activePeriod === key
      ? "bg-green-500 text-black border-green-500"
      : "bg-white text-slate-800 border-slate-300 hover:bg-slate-50 focus:bg-white active:bg-white"
    }`;

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
        <div className="mt-8 mb-6">
          <h1 className="text-3xl font-bold tracking-tight">
            Statistics
          </h1>
          <p className="mt-1 text-base text-slate-600">
            Overview of your nutrition, costs and consumption patterns.
          </p>
        </div>

        <section className="mb-6 rounded-2xl bg-white border border-slate-200 p-6 shadow-sm space-y-5">

          <div className="flex flex-wrap gap-6 items-end relative">
            <div className="relative">
              <label className="block text-sm font-semibold text-slate-800 mb-2">
                Start date
              </label>
              <button
                type="button"
                onClick={() => setShowStartCalendar(true)}
                className="w-[160px] rounded-xl border border-slate-300 bg-white px-4 py-2 text-sm text-left hover:bg-slate-50"
              >
                {startDate ? toIsoDate(startDate) : "Select date"}
              </button>

              {showStartCalendar && (
                <div className="absolute z-50 mt-2">
                  <CalendarPopup
                    initialDate={startDate ?? new Date()}
                    onApply={(date) => {
                      setStartDate(date);
                      setShowStartCalendar(false);
                    }}
                    onCancel={() => setShowStartCalendar(false)}
                  />
                </div>
              )}
            </div>

            <div className="relative">
              <label className="block text-sm font-semibold text-slate-800 mb-2">
                End date
              </label>
              <button
                type="button"
                onClick={() => setShowEndCalendar(true)}
                className="w-[160px] rounded-xl border border-slate-300 bg-white px-4 py-2 text-sm text-left hover:bg-slate-50"
              >
                {endDate ? toIsoDate(endDate) : "Select date"}
              </button>

              {showEndCalendar && (
                <div className="absolute z-50 mt-2">
                  <CalendarPopup
                    initialDate={endDate ?? new Date()}
                    onApply={(date) => {
                      setEndDate(date);
                      setShowEndCalendar(false);
                    }}
                    onCancel={() => setShowEndCalendar(false)}
                  />
                </div>
              )}
            </div>

            <button
              disabled={loading || !startDate || !endDate}
              onClick={() =>
                fetchStats(
                  "/statistics/averageByDate",
                  {
                    method: "POST",
                    body: JSON.stringify({
                      startDate: toIsoDate(startDate),
                      endDate: toIsoDate(endDate),
                    }),
                  },
                  "range"
                )
              }
              className={periodButtonClass("range")}
            >
              Range average
            </button>
          </div>

          <div className="flex gap-2">
            <button
              className={periodButtonClass("daily")}
              disabled={loading}
              onClick={() =>
                fetchStats("/statistics/daily", {}, "daily")
              }
            >
              Daily
            </button>

            <button
              className={periodButtonClass("7")}
              disabled={loading}
              onClick={() =>
                fetchStats("/statistics/average/7days", {}, "7")
              }
            >
              Last 7 days
            </button>

            <button
              className={periodButtonClass("30")}
              disabled={loading}
              onClick={() =>
                fetchStats("/statistics/average/30days", {}, "30")
              }
            >
              Last 30 days
            </button>
          </div>

          {error && (
            <p className="text-sm font-medium text-red-600">
              {error}
            </p>
          )}
        </section>

        {loading && (
          <p className="text-slate-500">Loading statistics…</p>
        )}

        {!loading && stats && (
          <>
            <section className="mb-6">
              <Kpi stats={stats} />
            </section>

            <section className="mb-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
              <AverageMacrosBar stats={stats} />
              <ProteinDonutChart stats={stats} />
            </section>

            <section className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <FatCompositionBar stats={stats} />
              <SugarSaltBar stats={stats} />
            </section>
          </>
        )}

        <div className="mt-6">
          <Footer />
        </div>
      </main>
    </div>
  );
}
