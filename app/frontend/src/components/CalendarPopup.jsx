// src/components/CalendarPopup.jsx
import { useState } from "react";

function formatDate(date) {
  const d = date.getDate().toString().padStart(2, "0");
  const m = (date.getMonth() + 1).toString().padStart(2, "0");
  const y = date.getFullYear();
  return `${d}/${m}/${y}`;
}

export default function CalendarPopup({ initialDate, onApply, onCancel }) {
  const [currentMonth, setCurrentMonth] = useState(
    new Date(initialDate.getFullYear(), initialDate.getMonth(), 1)
  );
  const [tempDate, setTempDate] = useState(initialDate);

  const year = currentMonth.getFullYear();
  const month = currentMonth.getMonth();

  const firstDay = new Date(year, month, 1).getDay();
  const daysInMonth = new Date(year, month + 1, 0).getDate();

  const cells = [];
  for (let i = 0; i < firstDay; i++) cells.push(null);
  for (let d = 1; d <= daysInMonth; d++) cells.push(d);

  const weeks = [];
  for (let i = 0; i < cells.length; i += 7) {
    weeks.push(cells.slice(i, i + 7));
  }

  const monthNames = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];

  const handlePrevMonth = () => {
    setCurrentMonth(new Date(year, month - 1, 1));
  };

  const handleNextMonth = () => {
    setCurrentMonth(new Date(year, month + 1, 1));
  };

  const handleSelectDay = (day) => {
    if (!day) return;
    setTempDate(new Date(year, month, day));
  };

  const isSelected = (day) => {
    if (!day) return false;
    return (
      tempDate.getFullYear() === year &&
      tempDate.getMonth() === month &&
      tempDate.getDate() === day
    );
  };

  return (
    <div
      className="
        w-[260px] md:w-[280px]
        bg-white rounded-xl shadow-lg
        border border-slate-200
        p-3
      "
    >
      <div className="mb-3">
        <input
          type="text"
          readOnly
          value={formatDate(tempDate)}
          className="
            w-full border border-slate-300 rounded-lg
            px-2 py-1.5
            text-slate-800 text-xs
          "
        />
      </div>

      <div className="flex items-center justify-between mb-2">
        <button
          type="button"
          onClick={handlePrevMonth}
          className="text-lg px-1 hover:text-slate-900"
        >
          ‹
        </button>

        <div className="text-sm font-semibold">
          {monthNames[month]} {year}
        </div>

        <button
          type="button"
          onClick={handleNextMonth}
          className="text-lg px-1 hover:text-slate-900"
        >
          ›
        </button>
      </div>

      <div className="grid grid-cols-7 text-center text-[10px] font-semibold text-slate-500 mb-1">
        <div>S</div>
        <div>M</div>
        <div>T</div>
        <div>W</div>
        <div>T</div>
        <div>F</div>
        <div>S</div>
      </div>

      <div className="grid grid-cols-7 text-center text-xs mb-3 gap-y-1">
        {weeks.map((week, wi) =>
          week.map((day, di) => {
            const key = `${wi}-${di}`;
            if (!day) {
              return <div key={key} />;
            }

            const selected = isSelected(day);

            return (
              <button
                key={key}
                type="button"
                onClick={() => handleSelectDay(day)}
                className={`
                  mx-auto w-7 h-7 rounded-md
                  flex items-center justify-center
                  ${
                    selected
                      ? "bg-brandGreen text-white"
                      : "hover:bg-slate-100 text-slate-800"
                  }
                `}
              >
                {day}
              </button>
            );
          })
        )}
      </div>

      <div className="flex items-center justify-between mt-1">
        <button
          type="button"
          onClick={onCancel}
          className="text-[11px] text-brandGreen hover:underline"
        >
          Cancel
        </button>

        <button
          type="button"
          onClick={() => onApply(tempDate)}
          className="
            px-4 py-1.5 rounded-full bg-brandGreen
            text-white font-semibold text-xs
            hover:bg-green
          "
        >
          OK
        </button>
      </div>
    </div>
  );
}
