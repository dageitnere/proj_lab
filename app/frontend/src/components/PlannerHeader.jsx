import { useState } from "react";
import { FiCalendar } from "react-icons/fi";
import CalendarPopup from "./CalendarPopup.jsx";

function formatDate(date) {
  const d = date.getDate().toString().padStart(2, "0");
  const m = (date.getMonth() + 1).toString().padStart(2, "0");
  const y = date.getFullYear();
  return `${d}/${m}/${y}`;
}

export default function PlannerHeader() {
  const [view, setView] = useState("day");
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [isCalendarOpen, setIsCalendarOpen] = useState(false);

  const handlePrevDay = () => {
    setSelectedDate((prev) =>
      new Date(prev.getFullYear(), prev.getMonth(), prev.getDate() - 1)
    );
  };

  const handleNextDay = () => {
    setSelectedDate((prev) =>
      new Date(prev.getFullYear(), prev.getMonth(), prev.getDate() + 1)
    );
  };

  const handleDateChange = (newDate) => {
    setSelectedDate(newDate);
  };

  return (
    <div className="relative inline-flex flex-col">
      <div className="flex items-center gap-4">

        <div className="inline-flex items-center h-11 rounded-xl border border-slate-300 bg-white overflow-hidden shadow-sm">
          <button
            type="button"
            onClick={() => setView("day")}
            className={`
              h-full px-6 text-base font-medium
              ${
                view === "day"
                  ? "bg-green-500 text-black"
                  : "text-slate-800 hover:bg-slate-100"
              }
            `}
          >
            Day
          </button>
          <button
            type="button"
            onClick={() => setView("week")}
            className={`
              h-full px-6 text-base font-medium
              ${
                view === "week"
                  ? "bg-green-500 text-black"
                  : "text-slate-800 hover:bg-slate-100"
              }
            `}
          >
            Week
          </button>
        </div>

        <div className="flex items-center gap-1 text-slate-700 -mt-[1px]">
          <button
            type="button"
            onClick={handlePrevDay}
            className="
              h-11 w-10
              flex items-center justify-center
              text-5xl leading-none
              hover:text-slate-900
            "
          >
            ‹
          </button>

          <button
            type="button"
            onClick={() => setIsCalendarOpen((prev) => !prev)}
            className="
              h-11 w-10
              flex items-center justify-center
              hover:text-slate-900
            "
          >
            <FiCalendar className="w-7 h-7" />
          </button>

          <button
            type="button"
            onClick={handleNextDay}
            className="
              h-11 w-10
              flex items-center justify-center
              text-5xl leading-none
              hover:text-slate-900
            "
          >
            ›
          </button>

          <span className="ml-1 text-2xl font-semibold text-slate-900">
            Today
          </span>

        </div>
      </div>


      {isCalendarOpen && (
        <div className="absolute left-40 mt-4 z-50">
          <CalendarPopup
            initialDate={selectedDate}
            onApply={(newDate) => {
              handleDateChange(newDate);
              setIsCalendarOpen(false);
            }}
            onCancel={() => setIsCalendarOpen(false)}
          />
        </div>
      )}
    </div>
  );
}
