import Pear from "../assets/pear.png";

const noop = () => {};

export default function StartScreenNewPage({
  onGenerate = noop,
  onCopyPrevious = noop,
  onPlanManually = noop,
}) {
  return (
    <div className="flex flex-col items-center text-center px-4
    space-y-4
        scale-150 md:scale-110">
      <img
        src={Pear}
        alt="Cute peach painting a meal"
        className="w-52 h-52 object-contain mb-4"
      />

      <h2 className="text-2xl font-semibold mb-2">
        What are we eating today?
      </h2>

      <div className="mt-4 flex flex-wrap gap-3 justify-center">
        <button
          type="button"
          onClick={onGenerate}
          className="
            px-6 py-2 rounded-full
            bg-green-500 text-black font-medium
            shadow-md hover:bg-green-600
            flex items-center gap-2
          "
        >
          ⟳ Generate
        </button>
        <button
          type="button"
          onClick={onPlanManually}
          className="
            px-6 py-2 rounded-full
            bg-white border border-slate-300
            text-slate-800 font-medium
            hover:bg-slate-50
          "
        >
          Plan Manually
        </button>
      </div>
    </div>
  );
}