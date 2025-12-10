import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const menuItems = [
  { id: "planner", label: "Planner", path: "/planner" },
  { id: "my-menus", label: "My menus", path: "/mymenus" },
  { id: "discover", label: "Discover", path: "/discover" },
  { id: "generate-menu", label: "Generate menu", path: "/generatemenu" },
  { id: "all-products", label: "All products", path: "/products" },
  { id: "my-products", label: "My products", path: "/my-products" },
  { id: "consumed-products", label: "Consumed products", path: "/consumed" },
  { id: "statistics", label: "Statistics", path: "/statistics" },
];

export default function SidebarMenu() {
  const [opened, setOpened] = useState(false);
  const [username, setUsername] = useState("");
  const userInitial = username ? username.charAt(0).toUpperCase() : "";
  const navigate = useNavigate();

  const visibleWhenClosed = ["planner", "my-menus", "discover"];

  useEffect(() => {
    const stored = localStorage.getItem("username");
    if (stored) setUsername(stored);
  }, []);

  const handleLogout = async () => {
    try {
      await fetch("http://localhost:8000/auth/logout", {
        method: "POST",
        credentials: "include",
      });
    } catch (e) {
      console.error("Logout error:", e);
    }

    localStorage.removeItem("username");
    navigate("/");
  };

  const handleNavigate = (path) => {
    navigate(path);
  };

  return (
    <div
      className={`
        fixed inset-y-0 right-0 z-40
        flex
        overflow-hidden
        bg-white
        border-l-2 border-gray-300
        transition-[width] duration-300
        ${opened ? "w-72" : "w-40"}
      `}
    >
      <div className="flex-1 h-full">
        {opened && (
          <div className="h-full flex flex-col pt-28 px-6 text-slate-900"></div>
        )}
      </div>

      <div
        className={`
          h-full flex flex-col pt-28 items-start
          ${opened ? "w-40 pr-6" : "w-24 pr-2"}
        `}
      >
        <button
          type="button"
          onClick={() => setOpened((prev) => !prev)}
          className={`
            self-center
            ${opened ? "" : "-ml-12"}
            tham tham-e-squeeze tham-w-7
            ${opened ? "tham-active" : ""}
          `}
        >
          <div className="tham-box">
            <div className="tham-inner bg-black" />
          </div>
        </button>

        {opened && username && (
          <div className="mt-6 flex items-center gap-2 pl-2">
            <div
              className="
                w-8 h-8 rounded-full
                bg-brandGreen text-white
                flex items-center justify-center
                text-base font-semibold
              "
            >
              {userInitial}
            </div>
            <p className="text-lg font-semibold text-slate-800 text-left">
              {username}
            </p>
          </div>
        )}

        <div className={`mt-10 w-full ${opened ? "space-y-3" : "space-y-12"}`}>

          {menuItems.map((item) => {
            if (!opened && !visibleWhenClosed.includes(item.id)) {
              return null;
            }

            const baseClasses = `
              ${opened ? "text-base" : "text-xl -ml-10"}
              text-center text-slate-900 whitespace-nowrap
              cursor-pointer hover:text-green-700
              transition-colors
            `;

            return (
              <p
                key={item.id}
                onClick={() => handleNavigate(item.path)}
                className={baseClasses}
              >
                {item.label}
              </p>
            );
          })}

          {opened && (
            <button
              type="button"
              onClick={handleLogout}
              className="
                pt-2
                text-base
                text-black-600
                hover:text-green-700 hover:underline
                block mx-auto
              "
            >
              Log out
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
