import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  FiBookOpen,
  FiUser,
  FiZap,
  FiGrid,
  FiBox,
  FiCheckCircle,
  FiBarChart2,
} from "react-icons/fi";

const menuItems = [
  { id: "my-menus", label: "My menus", path: "/mymenus", icon: FiBookOpen },
  { id: "profile", label: "Profile", path: "/profile", icon: FiUser },
  { id: "generate-menu", label: "Generate menu", path: "/generatemenu", icon: FiZap },
  { id: "all-products", label: "All products", path: "/products", icon: FiGrid },
  { id: "my-products", label: "My products", path: "/my-products", icon: FiBox },
  { id: "consumed-products", label: "Consumed products", path: "/consumed", icon: FiCheckCircle },
  { id: "statistics", label: "Statistics", path: "/statistics", icon: FiBarChart2 },
];

export default function SidebarMenu({ opened, setOpened }) {
  const [username, setUsername] = useState("");
  const userInitial = username ? username.charAt(0).toUpperCase() : "";
  const navigate = useNavigate();

  const visibleWhenClosed = ["my-menus", "profile"];

  useEffect(() => {
    const stored = localStorage.getItem("username");
    if (stored) setUsername(stored);
  }, []);

  const handleLogout = async () => {
    try {
      await fetch("/auth/logout", {
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
        fixed inset-y-0 left-0 z-40
        bg-white
        border-r-2 border-gray-300
        transition-all duration-300
        ${opened ? "w-72" : "w-40"}
      `}
    >
      <div
        className={`
          h-full flex flex-col pt-20
          ${opened ? "items-start pl-6 pr-6" : "items-center pr-2"}
        `}
      >
        <button
          type="button"
          onClick={() => setOpened((prev) => !prev)}
          className={`
            tham tham-e-squeeze tham-w-7
            ${opened ? "self-start ml-4" : "self-center"}
          `}
          aria-label="Toggle sidebar"
        >
          <div className="tham-box">
            <div className="tham-inner bg-black" />
          </div>
        </button>

        {opened && username && (
          <button
            type="button"
            onClick={() => navigate("/profile")}
            className="
              mt-6 flex items-center gap-2 pl-4
              w-full
              rounded-xl
              hover:bg-slate-50
              transition
              text-left
              py-2
            "
            aria-label="Open profile"
          >
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

            <span className="text-lg font-semibold text-slate-800">
              {username}
            </span>
          </button>
        )}

        <div
          className={`
            w-full
            ${opened ? "mt-4 space-y-2" : "mt-12 space-y-10"}
          `}
        >
          {menuItems.map((item) => {
            if (!opened && !visibleWhenClosed.includes(item.id)) return null;

            const Icon = item.icon;

            if (opened) {
              return (
                <button
                  key={item.id}
                  type="button"
                  onClick={() => handleNavigate(item.path)}
                  className="
                    w-full
                    flex items-center gap-3
                    text-left
                    pl-4 py-2
                    rounded-xl
                    text-slate-900
                    hover:bg-slate-50 hover:text-green-700
                    transition
                  "
                >
                  {Icon ? (
                    <Icon className="text-xl text-slate-700 group-hover:text-green-700" />
                  ) : null}
                  <span className="text-lg whitespace-nowrap">{item.label}</span>
                </button>
              );
            }

            return (
              <button
                key={item.id}
                type="button"
                onClick={() => handleNavigate(item.path)}
                className="
                  w-full
                  flex flex-col items-center
                  gap-2
                  cursor-pointer
                  group
                "
              >
                {Icon ? (
                  <Icon className="text-3xl text-slate-800 group-hover:text-green-700 transition" />
                ) : null}

                <span className="text-base font-medium text-slate-900 group-hover:text-green-700 transition">
                  {item.label}
                </span>
              </button>
            );
          })}

          {opened && (
            <button
              type="button"
              onClick={handleLogout}
              className="
                pt-4
                w-full
                text-base
                text-left
                pl-4
                text-black
                hover:text-green-700 hover:underline
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
