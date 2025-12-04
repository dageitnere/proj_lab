import { useState } from "react";

const menuItems = [
  { id: "planner", label: "Planner" },
  { id: "my menus", label: "My menus" },
  { id: "discover", label: "Discover" },
];

export default function SidebarMenu() {
  const [opened, setOpened] = useState(false);

  return (
    <div
      className={`
        fixed inset-y-0 right-0 z-40
        flex
        overflow-hidden
        bg-white shadow-2xl
        transition-[width] duration-300
        ${opened ? "w-72" : "w-40"}
      `}
    >

      <div className="flex-1 h-full">
        {opened && (
          <div className="h-full flex flex-col pt-28 px-6 text-slate-900">

          </div>
        )}
      </div>

      <div className="w-24 h-full flex flex-col items-center pt-28 pr-16">
        <button
          type="button"
          onClick={() => setOpened((prev) => !prev)}
          className={`
            tham tham-e-squeeze tham-w-7
            ${opened ? "tham-active" : ""}
          `}
        >
          <div className="tham-box">
            <div className="tham-inner bg-black" />
          </div>
        </button>

 <div className="mt-8 space-y-5 w-full">
          {menuItems.map((item) => (
            <p
              key={item.id}
              className={`
                ${opened ? "text-sm" : "text-lg"} 
                text-slate-900 text-center whitespace-nowrap
              `}
            >
              {item.label}
            </p>
          ))}
        </div>
      </div>
    </div>
  );
}