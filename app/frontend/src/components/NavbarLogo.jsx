import { Link } from "react-router-dom";

export default function NavbarLogo({ children }) {
  const isLoggedIn = document.cookie.split("; ").some(cookie => cookie.startsWith("access_token="));

  return (
    <nav className="fixed top-0 left-0 w-full px-40 py-10 flex items-center justify-between bg-transparent">
      <Link to={isLoggedIn ? "/new-page" : "/"}>
        <h1 className="text-black text-3xl font-bold">NutriMax</h1>
      </Link>
      <div className="flex gap-4">
        {children}
      </div>
    </nav>
  );
}
