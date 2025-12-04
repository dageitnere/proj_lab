import NavbarLogo from "../components/NavbarLogo.jsx";
import Footer from "../components/Footer.jsx";
import SidebarMenu from "../components/SidebarMenu.jsx";

export default function NewPage() {
  return (
    <div className="min-h-screen bg-noise-light text-slate-900">
    <SidebarMenu />
      <main className="px-8 py-6">
        <NavbarLogo />
        <Footer />
      </main>
    </div>
  );
}
