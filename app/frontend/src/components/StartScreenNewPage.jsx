import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { FiZap, FiSliders, FiBookOpen, FiBarChart2 } from "react-icons/fi";

export default function StartScreenNewPage() {
  const navigate = useNavigate();
  const username = localStorage.getItem("username") || "username";

  const withAuth = (path, options = {}) =>
    fetch(path, {
      credentials: "include",
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...(options.headers || {}),
      },
    });

  const [loading, setLoading] = useState(true);

  const [userInfo, setUserInfo] = useState({
    goal: "Not set",
    activity: "Not set",
    calories: "—",
    macros: "—",
  });

  const gallery = useMemo(
    () => [
      "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=900&q=60",
      "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?auto=format&fit=crop&w=900&q=60",
      "https://images.unsplash.com/photo-1525351484163-7529414344d8?auto=format&fit=crop&w=900&q=60",
      "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=900&q=60",
    ],
    []
  );

  const normalizeTextOrNotSet = (v) => {
    if (v === null || v === undefined) return "Not set";
    const s = String(v).trim();
    return s ? s : "Not set";
  };

  const normalizeNumOrDash = (v) => {
    if (v === null || v === undefined || v === "") return "—";
    const n = Number(v);
    if (Number.isNaN(n)) return "—";
    return String(n);
  };

  const loadProfile = async () => {
    setLoading(true);
    try {
      const res = await withAuth("/profile/getProfileInfo");
      if (!res.ok) {
        setUserInfo({
          goal: "Not set",
          activity: "Not set",
          calories: "—",
          macros: "—",
        });
        return;
      }

      const data = await res.json();

      const goal = data?.goalDisplay ?? null;
      const activity = data?.activityFactorDisplay ?? null;

      const kcal = data?.calculatedKcal ?? null;
      const carbs = data?.calculatedCarbs ?? null;
      const protein = data?.calculatedProtein ?? null;
      const fat = data?.calculatedFat ?? null;

      const hasAnyMacro =
        (carbs !== null && carbs !== undefined) ||
        (protein !== null && protein !== undefined) ||
        (fat !== null && fat !== undefined);

      const macrosStr = hasAnyMacro
        ? `C ${normalizeNumOrDash(carbs)}g • P ${normalizeNumOrDash(
            protein
          )}g • F ${normalizeNumOrDash(fat)}g`
        : "—";

      setUserInfo({
        goal: normalizeTextOrNotSet(goal),
        activity: normalizeTextOrNotSet(activity),
        calories:
          kcal === null || kcal === undefined
            ? "—"
            : `${normalizeNumOrDash(kcal)} kcal`,
        macros: macrosStr,
      });
    } catch {
      setUserInfo({
        goal: "Not set",
        activity: "Not set",
        calories: "—",
        macros: "—",
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void loadProfile();
  }, []);

  return (
    <main className="min-h-screen bg-white">
      <div className="ml-40 px-10 py-10">
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-10 items-start">
          <section>
            <h1 className="text-4xl font-bold text-slate-900">
              Welcome, <span className="text-brandGreen">{username}</span>!
            </h1>

            <p className="mt-3 text-slate-600 max-w-xl">
              This app generates menus using a Linear Programming model based on
              your goals and nutrient constraints.
            </p>

            <div className="mt-8 rounded-2xl border border-slate-200 p-6">
              <div className="flex items-center justify-between gap-3">
                <h2 className="text-lg font-semibold text-slate-900">
                  Your profile info
                </h2>
                {loading && (
                  <span className="text-xs text-slate-500">Loading...</span>
                )}
              </div>

              <div className="mt-4 grid grid-cols-1 sm:grid-cols-2 gap-4">
                <InfoRow label="Goal" value={userInfo.goal} />
                <InfoRow label="Activity level" value={userInfo.activity} />
                <InfoRow label="Calories target" value={userInfo.calories} />
                <InfoRow label="Macros" value={userInfo.macros} />
              </div>

              <button
                type="button"
                onClick={() => navigate("/profile")}
                className="mt-5 inline-flex items-center gap-2 text-sm font-semibold text-brandGreen hover:underline"
              >
                <FiSliders />
                Update profile & constraints
              </button>
            </div>

            <div className="mt-8 grid grid-cols-1 sm:grid-cols-2 gap-4">
              <ActionCard
                title="Generate menu"
                desc="Create a menu for your goal & activity level"
                icon={<FiZap className="text-2xl" />}
                onClick={() => navigate("/generatemenu")}
              />
              <ActionCard
                title="My menus"
                desc="View your saved menus"
                icon={<FiBookOpen className="text-2xl" />}
                onClick={() => navigate("/mymenus")}
              />
              <ActionCard
                title="Statistics"
                desc="Track progress & nutrition overview"
                icon={<FiBarChart2 className="text-2xl" />}
                onClick={() => navigate("/statistics")}
              />
              <ActionCard
                title="Set constraints"
                desc="Calories, macros, allergies, preferences"
                icon={<FiSliders className="text-2xl" />}
                onClick={() => navigate("/profile")}
              />
            </div>
          </section>

          <section className="xl:pl-6">
            <div className="rounded-2xl border border-slate-200 p-6">
              <h2 className="text-lg font-semibold text-slate-900">
                Inspiration / Planning
              </h2>
              <p className="mt-2 text-slate-600">
                Examples of meals and planning ideas.
              </p>

              <div className="mt-6 grid grid-cols-2 gap-4">
                {gallery.map((src, i) => (
                  <div
                    key={i}
                    className="rounded-2xl overflow-hidden border border-slate-100 bg-slate-50"
                  >
                    <img
                      src={src}
                      alt={`Food example ${i + 1}`}
                      className="h-40 w-full object-cover hover:scale-[1.02] transition"
                      loading="lazy"
                    />
                  </div>
                ))}
              </div>

              <div className="mt-6 rounded-2xl bg-slate-50 p-4 border border-slate-200">
                <p className="text-sm text-slate-700">
                  Tip: set your constraints first — it will strongly affect the
                  generated menu.
                </p>
              </div>
            </div>
          </section>
        </div>
      </div>
    </main>
  );
}

function InfoRow({ label, value }) {
  return (
    <div className="rounded-xl bg-slate-50 border border-slate-200 p-4">
      <div className="text-xs text-slate-500">{label}</div>
      <div className="mt-1 text-base font-semibold text-slate-900">{value}</div>
    </div>
  );
}

function ActionCard({ title, desc, icon, onClick }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className="
        group w-full text-left
        rounded-2xl border border-slate-200
        p-5
        hover:bg-slate-50 transition
      "
    >
      <div className="flex items-start gap-3">
        <div className="mt-0.5 text-slate-800 group-hover:text-brandGreen transition">
          {icon}
        </div>
        <div>
          <div className="text-lg font-semibold text-slate-900">{title}</div>
          <div className="mt-1 text-sm text-slate-600">{desc}</div>
        </div>
      </div>
    </button>
  );
}
