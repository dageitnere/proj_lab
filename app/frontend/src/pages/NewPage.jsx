import NavbarLogo from "../components/NavbarLogo.jsx";
import Footer from "../components/Footer.jsx";
import SidebarMenu from "../components/SidebarMenu.jsx";
// import StartScreenNewPage from "../components/StartScreenNewPage.jsx";  <section className="flex-1 flex items-center justify-center pr-40 mt-44">
//           <StartScreenNewPage />
//             </section>

import PlannerHeader from "../components/PlannerHeader.jsx";

export default function NewPage() {
  return (
    <div className="min-h-screen bg-noise-light text-slate-900">
    <SidebarMenu />
      <main className="px-8 py-6">
          <div className="mt-10 mb-4">  <PlannerHeader /> </div>
        <Footer />
      </main>
    </div>
  );
}
