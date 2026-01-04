import { Bar } from "react-chartjs-2";

export default function AverageMacrosBar({ stats }) {
  if (!stats) return null;

  const data = {
    labels: ["Protein (g)", "Fat (g)", "Carbs (g)", "Sugar (g)"],
    datasets: [
      {
        label: "Average intake",
        data: [
          stats.averageProtein,
          stats.averageFat,
          stats.averageCarbs,
          stats.averageSugar,
        ],
        backgroundColor: ["#14b8a6", "#fb7185", "#6366f1", "#f59e0b"],
        borderRadius: 6,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { display: false },
    },
    scales: {
      y: {
        beginAtZero: true,
        title: { display: true, text: "Grams" },
      },
    },
  };

  return (
    <div className="rounded-2xl bg-white border border-slate-200 p-6 shadow-sm">
      <h3 className="mb-4 font-semibold text-lg">
        Average macronutrients
      </h3>
      <Bar data={data} options={options} />
    </div>
  );
}
