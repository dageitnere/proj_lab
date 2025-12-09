import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const menuItems = [
  { id: "planner", label: "Planner" },
  { id: "my-menus", label: "My menus" },
  { id: "discover", label: "Discover" },
  { id: "generate-menu", label: "Generate menu" },
];

export default function SidebarMenu() {
  const [opened, setOpened] = useState(false);
  const [username, setUsername] = useState("");
  const userInitial = username ? username.charAt(0).toUpperCase() : "";
  const navigate = useNavigate();

  useEffect(() => {
    const stored = localStorage.getItem("username");
    if (stored) {
      setUsername(stored);
    }
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
    setUsername("");
    navigate("/");
  };

  const handleGoToGenerateMenu = () => {
    navigate("/generatemenu");
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
                w-8 h-8
                rounded-full
                bg-brandGreen
                text-white
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
            mt-10 w-full
            ${opened ? "space-y-3" : "space-y-12"}
          `}
        >
          {menuItems.map((item) => {
            if (item.id === "generate-menu" && !opened) {
              return null;
            }

            const baseClasses = `
              ${
                opened
                  ? "text-base text-center"
                  : "text-xl text-center -ml-10"
              }
              text-slate-900 whitespace-nowrap
            `;

            if (item.id === "generate-menu") {
              return (
                <p
                  key={item.id}
                  onClick={handleGoToGenerateMenu}
                  className={baseClasses + " cursor-pointer hover:text-green-700"}
                >
                  {item.label}
                </p>
              );
            }

            return (
              <p
                key={item.id}
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
