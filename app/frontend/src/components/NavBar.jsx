import { useState } from "react";
import Modal from "./Modal";
import LoginForm from "./LoginForm";

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <nav
        className="fixed top-0 left-0 w-full px-40 py-10 flex items-center justify-between"
        style={{ backgroundColor: "#2F6235" }}
      >
        <h1 className="text-white text-3xl font-bold">NutriMax</h1>

        <button
          className="inline-flex items-center justify-center rounded-full px-8 py-3
                     bg-white text-[#2F6235] font-semibold shadow
                     hover:bg-white/90 focus:outline-none focus-visible:ring
                     focus-visible:ring-white/60 transition"
          onClick={() => setIsOpen(true)}
        >
          Login
        </button>
      </nav>


      <Modal isOpen={isOpen} onClose={() => setIsOpen(false)}>
        <LoginForm onSuccess={() => setIsOpen(false)} />
      </Modal>
    </>
  );
}
