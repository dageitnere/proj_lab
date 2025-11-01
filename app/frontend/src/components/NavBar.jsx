import { useState } from "react";
import Modal from "./Modal";

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <nav
        className="fixed top-0 left-0 w-full px-40 py-10 flex items-center justify-between"
        style={{ backgroundColor: '#2F6235' }}
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
        <h2 className="text-2xl font-bold mb-4 text-black brandGreen">Login</h2>
        <input
          type="text"
          placeholder="Username"
          className="w-full p-2 border mb-4 rounded text-black"
        />
        <input
          type="password"
          placeholder="Password"
          className="w-full p-2 border mb-4 rounded text-black"
        />
        <button className="w-full py-2 bg-brandGreen text-white rounded hover:bg-green-700 transition">
          Submit
        </button>
      </Modal>
    </>
  );
}