import { Bar } from "react-chartjs-2";

export default function SugarSaltBar({ stats }) {
  if (!stats) return null;

  const data = {
    labels: ["Sugar (g)", "Salt (g)"],
    datasets: [
      {
        data: [stats.averageSugar, stats.averageSalt],
        backgroundColor: ["#f59e0b", "#64748b"],
        borderRadius: 6,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: { legend: { display: false } },
    scales: {
      y: { beginAtZero: true, title: { display: true, text: "Grams" } },
    },
  };

  return (
    <div className="rounded-2xl bg-white border border-slate-200 p-6 shadow-sm">
      <h3 className="mb-4 font-semibold text-lg">
        Sugar & salt
      </h3>
      <Bar data={data} options={options} />
    </div>
  );
}
