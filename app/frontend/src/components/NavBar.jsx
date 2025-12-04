import { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import Modal from "./Modal";
import LoginForm from "./LoginForm";
import NavbarLogo from "./NavbarLogo";

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    if (params.get("login") === "open") {
      setIsOpen(true);
    }
  }, [location]);

  return (
    <NavbarLogo>
      <button
        className="inline-flex items-center justify-center rounded-full px-8 py-3
                  bg-white text-brandGreen font-semibold shadow
                  hover:bg-white/90 focus:outline-none focus-visible:ring
                  focus-visible:ring-white/60 transition"
        onClick={() => setIsOpen(true)}
      >
        Login
      </button>
      <a
        href="/register"
        className="inline-flex items-center justify-center rounded-full px-8 py-3
                  bg-white text-brandGreen font-semibold shadow
                  hover:bg-white/90 focus:outline-none focus-visible:ring
                  focus-visible:ring-white/60 transition"
      >
        Register
      </a>

      <Modal isOpen={isOpen} onClose={() => setIsOpen(false)}>
        <LoginForm onSuccess={() => setIsOpen(false)} />
      </Modal>
    </NavbarLogo>
  );
}
