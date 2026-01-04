import { Doughnut } from "react-chartjs-2";

export default function ProteinDonutChart({ stats }) {
  if (!stats) return null;

  const data = {
    labels: ["Animal protein", "Plant protein", "Dairy protein"],
    datasets: [
      {
        data: [
          stats.averageAnimalProtein,
          stats.averagePlantProtein,
          stats.averageDairyProtein,
        ],
        backgroundColor: ["#fb7185", "#14b8a6", "#6366f1"],
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { position: "bottom" },
    },
    cutout: "60%",
  };

  return (
    <div className="rounded-2xl bg-white border border-slate-200 p-6 shadow-sm">
      <h3 className="mb-4 font-semibold text-lg">
        Protein sources
      </h3>
      <Doughnut data={data} options={options} />
    </div>
  );
}
