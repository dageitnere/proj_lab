import { Bar } from "react-chartjs-2";

export default function FatCompositionBar({ stats }) {
  if (!stats) return null;

  const data = {
    labels: ["Total fat (g)", "Saturated fat (g)"],
    datasets: [
      {
        data: [stats.averageFat, stats.averageSatFat],
        backgroundColor: ["#fb7185", "#e11d48"],
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
        Fat composition
      </h3>
      <Bar data={data} options={options} />
    </div>
  );
}
