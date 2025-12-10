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

  const handleGoToMyMenus = () => {
  navigate("/mymenus");
    };

  return (
    <div
      className={`
        fixed inset-y-0 left-0 z-40
        bg-white 
        border-r-2 border-gray-300
        ${opened ? "w-72" : "w-40"}
      `}
    >

      <div
        className={`
          h-full flex flex-col pt-28
          ${opened ? "items-start pl-10 pr-6" : "items-center pr-2"}
        `}
      >
        <button
          type="button"
          onClick={() => setOpened((prev) => !prev)}
          className={`
            tham tham-e-squeeze tham-w-7
            ${opened ? "self-start ml-4" : "self-center"}
          `}
        >
          <div className="tham-box">
            <div className="tham-inner bg-black" />
          </div>
        </button>

        {opened && username && (
          <div className="mt-6 flex items-center gap-2 pl-4">
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

        <div
          className={`
            mt-6 w-full
            ${opened ? "space-y-3" : " mt-24 space-y-16"}
          `}
        >
          {menuItems.map((item) => {
            if (!opened && !visibleWhenClosed.includes(item.id)) {
              return null;
            }

            const baseClasses = `
              w-full
              ${
                opened
                  ? "text-lg text-left pl-4"
                  : "text-xl text-center"
              }
              text-slate-900 whitespace-nowrap
            `;

            if (item.id === "generate-menu") {
              return (
                <p
                  key={item.id}
                  onClick={handleGoToGenerateMenu}
                  className={
                    baseClasses + " cursor-pointer hover:text-green-700"
                  }
                >
                  {item.label}
                </p>
              );
            }

            if (item.id === "my-menus") {
            return (
              <p
                key={item.id}
                onClick={handleGoToMyMenus}
                className={baseClasses + " cursor-pointer hover:text-green-700"}
              >
                {item.label}
              </p>
            );
          }

            return (
              <p key={item.id} className={baseClasses}>
                {item.label}
              </p>
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
