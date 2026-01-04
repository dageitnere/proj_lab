export default function KpiRow({ stats }) {
  if (!stats) return null;

  const items = [
    {
      label: "Avg calories",
      value: Math.round(stats.averageKcal),
      unit: "kcal",
    },
    {
      label: "Avg cost",
      value: stats.averageCost.toFixed(2),
      unit: "€",
    },
    {
      label: "Products per day",
      value: Math.round(stats.averageProducts),
      unit: "",
    },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
      {items.map((item) => (
        <div
          key={item.label}
          className="rounded-xl border bg-white p-4 shadow-sm"
        >
          <p className="text-sm text-slate-500">{item.label}</p>
          <p className="mt-1 text-2xl font-bold text-slate-900">
            {item.value}{" "}
            <span className="text-base font-medium text-slate-500">
              {item.unit}
            </span>
          </p>
        </div>
      ))}
    </div>
  );
}
