import Footer from "../components/Footer.jsx";
import SidebarMenu from "../components/SidebarMenu.jsx";
import StartScreenNewPage from "../components/StartScreenNewPage.jsx";

export default function NewPage() {
  return (
    <div className="min-h-screen bg-noise-light text-slate-900">
      <SidebarMenu />
        <StartScreenNewPage />
        <Footer />
    </div>
  );
}

