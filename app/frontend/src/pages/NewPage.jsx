import { useState } from "react";
import Footer from "../components/Footer.jsx";
import SidebarMenu from "../components/SidebarMenu.jsx";
import StartScreenNewPage from "../components/StartScreenNewPage.jsx";

export default function NewPage() {
  const [sidebarOpened, setSidebarOpened] = useState(false);

  return (
    <div className="bg-slate-50">
      <SidebarMenu
        opened={sidebarOpened}
        setOpened={setSidebarOpened}
      />

      <main
        className={`
          transition-all duration-300
          ${sidebarOpened ? "ml-32" : "ml-0"}
        `}
      >
        <StartScreenNewPage />
        <Footer />
      </main>
    </div>
  );
}
