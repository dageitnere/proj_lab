import { Link } from "react-router-dom";

export default function NavbarLogo({ children }) {
  return (
    <nav
      className="fixed top-0 left-0 w-full px-40 py-10 flex items-center justify-between bg-brandGreen"
    >
      <Link to="/">
        <h1 className="text-white text-3xl font-bold">NutriMax</h1>
      </Link>
      <div className="flex gap-4">
        {children}
      </div>
    </nav>
  );
}
