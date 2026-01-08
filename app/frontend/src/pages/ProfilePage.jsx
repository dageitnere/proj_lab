import { memo, useCallback, useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";


const Card = memo(function Card({ title, children, className = "" }) {
  return (
    <section
      className={`rounded-2xl bg-white/85 backdrop-blur border border-black/10 shadow-sm p-6 ${className}`}
    >
      <h2 className="text-lg sm:text-xl font-bold text-black">{title}</h2>
      <div className="mt-4">{children}</div>
    </section>
  );
});

const Row = memo(function Row({ label, value }) {
  return (
    <div className="flex items-center justify-between gap-6 py-3 border-b border-black/5 last:border-b-0">
      <div className="text-sm sm:text-base text-black/80">{label}</div>
      <div className="text-sm sm:text-base font-semibold text-black/80 text-right">
        {value}
      </div>
    </div>
  );
});

const Pill = memo(function Pill({ children, tone = "neutral", onClick, disabled = false }) {
  const toneClass =
    tone === "green"
      ? "border-brandGreen/30 bg-brandGreen/10 text-brandGreen"
      : "border-black/10 bg-white text-black/80";

  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      className={[
        "inline-flex items-center rounded-full border px-3 py-1 text-xs font-semibold transition",
        toneClass,
        disabled ? "opacity-60 cursor-not-allowed" : "hover:opacity-90",
      ].join(" ")}
    >
      {children}
    </button>
  );
});

const MetricCard = memo(function MetricCard({ label, value }) {
  return (
    <div className="rounded-2xl border border-black/10 bg-white p-5 shadow-sm text-center">
      <div className="text-3xl font-extrabold text-black/80">{value}</div>
      <div className="mt-1 text-xs font-semibold text-black/80">{label}</div>
    </div>
  );
});

const Bar = memo(function Bar({ label, value, unit }) {
  return (
    <div className="space-y-2">
      <div className="flex items-baseline justify-between">
        <div className="text-sm font-semibold text-black/80">{label}</div>
        <div className="text-sm font-semibold text-black/80">
          {value} {unit}
        </div>
      </div>

      <div className="h-3 w-full rounded-full bg-black/10 overflow-hidden">
        <div className="h-full rounded-full bg-brandGreen" style={{ width: "100%" }} />
      </div>
    </div>
  );
});

const InputRow = memo(function InputRow({
  label,
  name,
  placeholder,
  value,
  onValueChange,
}) {
  return (
    <div className="flex items-center justify-between gap-6 py-3 border-b border-black/5 last:border-b-0">
      <div className="text-sm sm:text-base text-black/80">{label}</div>
      <input
        name={name}
        value={value}
        onChange={(e) => onValueChange(name, e.target.value)}
        placeholder={placeholder}
        inputMode="numeric"
        className="
          w-44 sm:w-56
          rounded
          border border-black/30
          bg-white
          px-3 py-1.5
          text-sm text-black/80
          focus:outline-none focus:ring-2 focus:ring-brandGreen/60
        "
      />
    </div>
  );
});

const InputRowProfile = memo(function InputRowProfile({
  label,
  name,
  type = "text",
  step,
  min,
  max,
  value,
  onValueChange,
}) {
  return (
    <div className="flex items-center justify-between gap-6 py-3 border-b border-black/5 last:border-b-0">
      <div className="text-sm sm:text-base text-black/80">{label}</div>
      <input
        type={type}
        value={value}
        onChange={(e) => onValueChange(name, e.target.value)}
        step={step}
        min={min}
        max={max}
        className="
          w-44 sm:w-56
          rounded
          border border-black/30
          bg-white
          px-3 py-1.5
          text-sm text-black/80
          focus:outline-none focus:ring-2 focus:ring-brandGreen/60
        "
      />
    </div>
  );
});

const SelectRowProfile = memo(function SelectRowProfile({
  label,
  name,
  options,
  value,
  onValueChange,
}) {
  return (
    <div className="flex items-center justify-between gap-6 py-3 border-b border-black/5 last:border-b-0">
      <div className="text-sm sm:text-base text-black/80">{label}</div>
      <select
        value={value}
        onChange={(e) => onValueChange(name, e.target.value)}
        className="
          w-44 sm:w-56
          rounded
          border border-black/30
          bg-white
          px-3 py-1.5
          text-sm text-black/80
          focus:outline-none focus:ring-2 focus:ring-brandGreen/60
        "
      >
        {options.map((o) => (
          <option key={o.value} value={o.value}>
            {o.label}
          </option>
        ))}
      </select>
    </div>
  );
});


export default function ProfilePage() {
  const navigate = useNavigate();

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
  const [actionLoading, setActionLoading] = useState(false);
  const [error, setError] = useState("");

  const [profile, setProfile] = useState({
    username: "—",
    email: "—",
    emailVerified: false,

    age: null,
    gender: null,
    weight: null,
    height: null,
    activityFactorDisplay: null,
    goalDisplay: null,

    bmi: null,
    bmr: null,

    isVegan: false,
    isVegetarian: false,
    dairyIntolerance: false,

    calculatedKcal: null,
    calculatedCarbs: null,
    calculatedProtein: null,
    calculatedFat: null,
    calculatedSatFat: null,
    calculatedSugar: null,
    calculatedSalt: null,
  });

  const [editMode, setEditMode] = useState(false);
  const [resetDailyNutrition, setResetDailyNutrition] = useState(false);

  const [editProfile, setEditProfile] = useState({
    age: "",
    weight: "",
    height: "",
    activityLevel: "",
    goal: "",
    isVegan: false,
    isVegetarian: false,
    isDairyInt: false,
  });

  const [originalProfile, setOriginalProfile] = useState({
    age: null,
    weight: null,
    height: null,
    activityLevel: null,
    goal: null,
    isVegan: false,
    isVegetarian: false,
    isDairyInt: false,
  });

  const [editTargets, setEditTargets] = useState({
    kcal: "",
    carbs: "",
    protein: "",
    fat: "",
    satFat: "",
    sugar: "",
    salt: "",
  });

  const initials = useMemo(() => {
    const s = (profile.username || "").trim();
    return s ? s.charAt(0).toUpperCase() : "?";
  }, [profile.username]);

  const toFixedOrDash = (v, digits = 1) => {
    if (v === null || v === undefined || v === "") return "—";
    const n = Number(v);
    if (Number.isNaN(n)) return "—";
    return n.toFixed(digits);
  };

  const parseNumOrNull = (v) => {
    if (v === null || v === undefined) return null;
    const s = String(v).trim();
    if (!s) return null;
    const n = Number(s);
    return Number.isFinite(n) ? n : null;
  };

  const loadProfile = async () => {
    setError("");
    setLoading(true);
    try {
      const res = await withAuth("/profile/getProfileInfo");
      if (!res.ok) {
        const text = await res.text();
        throw new Error(text || `Failed to load profile (${res.status})`);
      }
      const data = await res.json();
      setProfile(data);

      const snapshot = {
        age: data.age ?? null,
        weight: data.weight ?? null,
        height: data.height ?? null,
        activityLevel: data.activityFactorDisplay ?? null,
        goal: data.goalDisplay ?? null,
        isVegan: !!data.isVegan,
        isVegetarian: !!data.isVegetarian,
        isDairyInt: !!data.dairyIntolerance,
      };
      setOriginalProfile(snapshot);

      setEditProfile({
        age: data.age ?? "",
        weight: data.weight ?? "",
        height: data.height ?? "",
        activityLevel: data.activityFactorDisplay ?? "SEDENTARY",
        goal: data.goalDisplay ?? "MAINTAIN",
        isVegan: !!data.isVegan,
        isVegetarian: !!data.isVegetarian,
        isDairyInt: !!data.dairyIntolerance,
      });

      setEditTargets({
        kcal: data.calculatedKcal ?? "",
        carbs: data.calculatedCarbs ?? "",
        protein: data.calculatedProtein ?? "",
        fat: data.calculatedFat ?? "",
        satFat: data.calculatedSatFat ?? "",
        sugar: data.calculatedSugar ?? "",
        salt:
          data.calculatedSalt !== null && data.calculatedSalt !== undefined
            ? (Number(data.calculatedSalt) / 1000).toFixed(2)
            : "",
      });
    } catch (e) {
      console.error(e);
      setError(e.message || "Failed to load profile.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void loadProfile();
  }, []);


  const onTargetChange = useCallback((name, value) => {
    setEditTargets((p) => ({ ...p, [name]: value }));
  }, []);

  const onProfileFieldChange = useCallback((name, value) => {
    setEditProfile((p) => ({ ...p, [name]: value }));
  }, []);

  // --- Edit profile ---
  const onEditProfile = () => {
    setError("");
    setResetDailyNutrition(false);
    setEditMode((v) => !v);
  };

  const onCancelEditProfile = () => {
    setEditMode(false);
    setResetDailyNutrition(false);
    setEditProfile({
      age: originalProfile.age ?? "",
      weight: originalProfile.weight ?? "",
      height: originalProfile.height ?? "",
      activityLevel: originalProfile.activityLevel ?? "SEDENTARY",
      goal: originalProfile.goal ?? "MAINTAIN",
      isVegan: !!originalProfile.isVegan,
      isVegetarian: !!originalProfile.isVegetarian,
      isDairyInt: !!originalProfile.isDairyInt,
    });
  };

  const onToggleDiet = (key) => {
    if (!editMode) return;

    setEditProfile((p) => {
      if (key === "isVegan") {
        const nextVegan = !p.isVegan;
        return {
          ...p,
          isVegan: nextVegan,
          isVegetarian: nextVegan ? true : false,
          isDairyInt: nextVegan ? true : false,
        };
      }
      if (key === "isVegetarian") {
        if (p.isVegan) return p;
        return { ...p, isVegetarian: !p.isVegetarian };
      }
      if (key === "isDairyInt") {
        if (p.isVegan) return p;
        return { ...p, isDairyInt: !p.isDairyInt };
      }
      return p;
    });
  };

  const buildChangeInfoPayload = () => {
    const payload = {};

    const nextAge = parseNumOrNull(editProfile.age);
    const nextWeight = parseNumOrNull(editProfile.weight);
    const nextHeight = parseNumOrNull(editProfile.height);

    if (nextAge !== null && nextAge !== originalProfile.age) payload.age = nextAge;
    if (nextWeight !== null && nextWeight !== originalProfile.weight)
      payload.weight = nextWeight;
    if (nextHeight !== null && nextHeight !== originalProfile.height)
      payload.height = nextHeight;

    if (
      editProfile.activityLevel &&
      editProfile.activityLevel !== originalProfile.activityLevel
    ) {
      payload.activityLevel = editProfile.activityLevel;
    }

    if (editProfile.goal && editProfile.goal !== originalProfile.goal) {
      payload.goal = editProfile.goal;
    }

    if (editProfile.isVegan !== originalProfile.isVegan) payload.isVegan = editProfile.isVegan;
    if (editProfile.isVegetarian !== originalProfile.isVegetarian)
      payload.isVegetarian = editProfile.isVegetarian;
    if (editProfile.isDairyInt !== originalProfile.isDairyInt)
      payload.isDairyInt = editProfile.isDairyInt;

    if (resetDailyNutrition) payload.resetDailyNutrition = true;

    return payload;
  };

  const onSaveProfileChanges = async () => {
    setError("");

    const payload = buildChangeInfoPayload();
    if (Object.keys(payload).length === 0) {
      setEditMode(false);
      setResetDailyNutrition(false);
      return;
    }

    try {
      setActionLoading(true);
      const res = await withAuth("/profile/changeInfo", {
        method: "POST",
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(text || `Failed to save (${res.status})`);
      }

      await loadProfile();
      setEditMode(false);
      setResetDailyNutrition(false);
    } catch (e) {
      console.error(e);
      setError(e.message || "Failed to update profile.");
    } finally {
      setActionLoading(false);
    }
  };

  const onSaveEditTargets = async (e) => {
    e.preventDefault();
    setError("");

    const calculatedKcal = parseNumOrNull(editTargets.kcal);
    const calculatedCarbs = parseNumOrNull(editTargets.carbs);
    const calculatedProtein = parseNumOrNull(editTargets.protein);
    const calculatedFat = parseNumOrNull(editTargets.fat);
    const calculatedSatFat = parseNumOrNull(editTargets.satFat);
    const calculatedSugar = parseNumOrNull(editTargets.sugar);

    const saltG = parseNumOrNull(editTargets.salt);
    const calculatedSalt = saltG === null ? null : Math.round(saltG * 1000);

    const payload = {
      calculatedKcal,
      calculatedCarbs,
      calculatedProtein,
      calculatedFat,
      calculatedSatFat,
      calculatedSugar,
      calculatedSalt,
    };

    try {
      setActionLoading(true);
      const res = await withAuth("/profile/changeDailyNutrition", {
        method: "POST",
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(text || `Failed to save (${res.status})`);
      }

      await loadProfile();
    } catch (e2) {
      console.error(e2);
      setError(e2.message || "Failed to save daily nutrition.");
    } finally {
      setActionLoading(false);
    }
  };

  const onResetNutrition = async () => {
    setError("");
    try {
      setActionLoading(true);
      const res = await withAuth("/profile/calculateDailyNutrition", {
        method: "POST",
        body: JSON.stringify({}),
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(text || `Failed to reset (${res.status})`);
      }

      await loadProfile();
    } catch (e) {
      console.error(e);
      setError(e.message || "Failed to reset nutrition.");
    } finally {
      setActionLoading(false);
    }
  };

  const targets = {
    kcal: profile.calculatedKcal ?? "—",
    carbs: profile.calculatedCarbs ?? "—",
    protein: profile.calculatedProtein ?? "—",
    fat: profile.calculatedFat ?? "—",
    satFat: profile.calculatedSatFat ?? "—",
    sugar: profile.calculatedSugar ?? "—",
    salt:
      profile.calculatedSalt !== null && profile.calculatedSalt !== undefined
        ? (Number(profile.calculatedSalt) / 1000).toFixed(2)
        : "—",
  };

  const activityOptions = [
    { value: "SEDENTARY", label: "Sedentary" },
    { value: "LIGHT", label: "Light" },
    { value: "MODERATE", label: "Moderate" },
    { value: "ACTIVE", label: "Active" },
    { value: "VERY_ACTIVE", label: "Very active" },
  ];

  const goalOptions = [
    { value: "LOSE", label: "Lose" },
    { value: "MAINTAIN", label: "Maintain" },
    { value: "GAIN", label: "Gain" },
  ];

  return (
    <div className="min-h-screen bg-noise-light text-black">
      <div className="relative z-10 max-w-6xl mx-auto px-5 pt-8 pb-14">
        <button
          type="button"
          onClick={() => navigate("/new-page")}
          className="
            absolute right-5 top-8
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

        {error && (
          <div className="mb-5 rounded-2xl border border-red-300 bg-red-50 px-4 py-3 text-sm text-red-700">
            {error}
          </div>
        )}

        {/* Header */}
        <div className="flex flex-col items-center text-center pt-2">
          <div className="h-36 w-36 sm:h-44 sm:w-44 rounded-full bg-brandGreen text-white flex items-center justify-center text-5xl sm:text-6xl font-extrabold border-4 border-white shadow-md">
            {initials}
          </div>

          <div className="mt-3">
            <div className="text-2xl sm:text-3xl font-extrabold text-black">
              {loading ? "Loading..." : profile.username}
            </div>

            <div className="mt-1 flex items-center justify-center gap-2">
              <div className="text-sm text-black/80">{profile.email}</div>
              {profile.emailVerified && (
                <span className="inline-flex items-center rounded-full border border-brandGreen/30 bg-brandGreen/10 px-3 py-1 text-xs font-semibold text-brandGreen">
                  Verified
                </span>
              )}
            </div>

            <div className="mt-3 flex justify-center">
              <button
                type="button"
                onClick={onEditProfile}
                className="rounded-xl border border-black/15 bg-white/80 px-5 py-2 text-sm font-bold text-black/80 hover:bg-white transition"
              >
                {editMode ? "Editing..." : "Edit profile"}
              </button>
            </div>
          </div>
        </div>

        <div className="mt-8 grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
          <Card title="Personal Information" className="lg:col-span-2">
            {editMode ? (
              <>
                <InputRowProfile
                  label="Age"
                  name="age"
                  type="number"
                  min={1}
                  max={120}
                  value={editProfile.age}
                  onValueChange={onProfileFieldChange}
                />
                <Row label="Gender" value={profile.gender ?? "—"} />
                <InputRowProfile
                  label="Weight (kg)"
                  name="weight"
                  type="number"
                  step="0.1"
                  min={1}
                  max={500}
                  value={editProfile.weight}
                  onValueChange={onProfileFieldChange}
                />
                <InputRowProfile
                  label="Height (cm)"
                  name="height"
                  type="number"
                  step="0.1"
                  min={50}
                  max={300}
                  value={editProfile.height}
                  onValueChange={onProfileFieldChange}
                />
                <SelectRowProfile
                  label="Activity Level"
                  name="activityLevel"
                  options={activityOptions}
                  value={editProfile.activityLevel}
                  onValueChange={onProfileFieldChange}
                />
                <SelectRowProfile
                  label="Goal"
                  name="goal"
                  options={goalOptions}
                  value={editProfile.goal}
                  onValueChange={onProfileFieldChange}
                />

                <div className="pt-4 flex flex-col gap-3">
                  <div className="text-sm font-bold text-black">Dietary Preferences</div>
                  <div className="flex flex-wrap gap-2 justify-center lg:justify-start">
                    <Pill
                      tone={editProfile.isVegan ? "green" : "neutral"}
                      onClick={() => onToggleDiet("isVegan")}
                    >
                      {editProfile.isVegan ? "Vegan" : "Not vegan"}
                    </Pill>

                    <Pill
                      tone={editProfile.isVegetarian ? "green" : "neutral"}
                      onClick={() => onToggleDiet("isVegetarian")}
                      disabled={editProfile.isVegan}
                    >
                      {editProfile.isVegetarian ? "Vegetarian" : "Not vegetarian"}
                    </Pill>

                    <Pill
                      tone={editProfile.isDairyInt ? "green" : "neutral"}
                      onClick={() => onToggleDiet("isDairyInt")}
                      disabled={editProfile.isVegan}
                    >
                      {editProfile.isDairyInt ? "Dairy intolerance" : "No dairy intolerance"}
                    </Pill>
                  </div>

                  <label className="mt-2 inline-flex items-center gap-2 text-sm text-black/80">
                    <input
                      type="checkbox"
                      checked={resetDailyNutrition}
                      onChange={(e) => setResetDailyNutrition(e.target.checked)}
                      className="h-4 w-4"
                    />
                    Recalculate daily nutrition
                  </label>

                  <div className="pt-2 flex flex-wrap gap-2">
                    <button
                      type="button"
                      onClick={onSaveProfileChanges}
                      disabled={actionLoading}
                      className="rounded-xl bg-brandGreen px-5 py-2.5 text-sm font-bold text-white hover:opacity-90 transition disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {actionLoading ? "Saving..." : "Save changes"}
                    </button>

                    <button
                      type="button"
                      onClick={onCancelEditProfile}
                      disabled={actionLoading}
                      className="rounded-xl border border-black/15 bg-white/80 px-5 py-2.5 text-sm font-bold text-black/80 hover:bg-white transition disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              </>
            ) : (
              <>
                <Row label="Age" value={profile.age ? `${profile.age} years` : "—"} />
                <Row label="Gender" value={profile.gender ?? "—"} />
                <Row
                  label="Weight"
                  value={profile.weight ? `${toFixedOrDash(profile.weight, 1)} kg` : "—"}
                />
                <Row
                  label="Height"
                  value={profile.height ? `${toFixedOrDash(profile.height, 1)} cm` : "—"}
                />
                <Row label="Activity Level" value={profile.activityFactorDisplay ?? "—"} />
                <Row label="Goal" value={profile.goalDisplay ?? "—"} />
              </>
            )}
          </Card>

          <div className="space-y-6">
            <Card title="Health Metrics">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <MetricCard label="BMI" value={profile.bmi ?? "—"} />
                <MetricCard label="BMR" value={profile.bmr ?? "—"} />
              </div>
            </Card>

            <Card title="Dietary Preferences">
              <div className="flex flex-wrap gap-2 justify-center mt-8">
                <span className="inline-flex items-center rounded-full border border-black/10 bg-white px-3 py-1 text-xs font-semibold text-black/80">
                  {profile.isVegan ? "Vegan" : "Not vegan"}
                </span>
                <span className="inline-flex items-center rounded-full border border-black/10 bg-white px-3 py-1 text-xs font-semibold text-black/80">
                  {profile.isVegetarian ? "Vegetarian" : "Not vegetarian"}
                </span>
                <span className="inline-flex items-center rounded-full border border-black/10 bg-white px-3 py-1 text-xs font-semibold text-black/80">
                  {profile.dairyIntolerance ? "Dairy intolerance" : "No dairy intolerance"}
                </span>
              </div>
            </Card>
          </div>
        </div>

        <div className="mt-6">
          <Card title="Daily Nutritional Targets">
            <div className="space-y-5">
              <Bar label="Calories" value={targets.kcal} unit="kcal" />
              <Bar label="Carbohydrates" value={targets.carbs} unit="g" />
              <Bar label="Protein" value={targets.protein} unit="g" />
              <Bar label="Fat" value={targets.fat} unit="g" />

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-2">
                <div className="rounded-2xl border border-black/10 bg-white p-4 text-center">
                  <div className="text-xs font-semibold text-black/80">Saturated fat</div>
                  <div className="mt-1 text-lg font-extrabold text-black/80">
                    {targets.satFat} g
                  </div>
                </div>

                <div className="rounded-2xl border border-black/10 bg-white p-4 text-center">
                  <div className="text-xs font-semibold text-black/80">Sugar</div>
                  <div className="mt-1 text-lg font-extrabold text-black/80">
                    {targets.sugar} g
                  </div>
                </div>

                <div className="rounded-2xl border border-black/10 bg-white p-4 text-center">
                  <div className="text-xs font-semibold text-black/80">Salt</div>
                  <div className="mt-1 text-lg font-extrabold text-black/80">
                    {targets.salt} g
                  </div>
                </div>
              </div>

              <div className="pt-2 flex justify-center">
                <button
                  type="button"
                  className="rounded-xl bg-brandGreen px-5 py-2.5 text-sm font-bold text-white hover:opacity-90 transition disabled:opacity-50 disabled:cursor-not-allowed"
                  onClick={onResetNutrition}
                  disabled={actionLoading}
                >
                  {actionLoading ? "Working..." : "Reset to Default Nutrition"}
                </button>
              </div>
            </div>
          </Card>
        </div>

        <div className="mt-6">
          <Card title="Edit Daily Nutrition">
            <form onSubmit={onSaveEditTargets}>
              <div className="divide-y divide-black/5">
                <InputRow
                  label="Calories (kcal)"
                  name="kcal"
                  placeholder="—"
                  value={editTargets.kcal}
                  onValueChange={onTargetChange}
                />
                <InputRow
                  label="Carbohydrates (g)"
                  name="carbs"
                  placeholder="—"
                  value={editTargets.carbs}
                  onValueChange={onTargetChange}
                />
                <InputRow
                  label="Protein (g)"
                  name="protein"
                  placeholder="—"
                  value={editTargets.protein}
                  onValueChange={onTargetChange}
                />
                <InputRow
                  label="Fat (g)"
                  name="fat"
                  placeholder="—"
                  value={editTargets.fat}
                  onValueChange={onTargetChange}
                />
                <InputRow
                  label="Saturated Fat (g)"
                  name="satFat"
                  placeholder="—"
                  value={editTargets.satFat}
                  onValueChange={onTargetChange}
                />
                <InputRow
                  label="Sugar (g)"
                  name="sugar"
                  placeholder="—"
                  value={editTargets.sugar}
                  onValueChange={onTargetChange}
                />
                <InputRow
                  label="Salt (g)"
                  name="salt"
                  placeholder="—"
                  value={editTargets.salt}
                  onValueChange={onTargetChange}
                />
              </div>

              <div className="pt-5">
                <button
                  type="submit"
                  className="rounded-xl bg-brandGreen px-6 py-2.5 text-sm font-bold text-white hover:opacity-90 transition disabled:opacity-50 disabled:cursor-not-allowed"
                  disabled={actionLoading}
                >
                  {actionLoading ? "Saving..." : "Save Changes"}
                </button>
              </div>
            </form>
          </Card>
        </div>
      </div>
    </div>
  );
}
