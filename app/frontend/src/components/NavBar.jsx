// src/components/NavBar.jsx
export default function Navbar() {
  return (
    <nav
      className="fixed top-0 left-0 w-full flex items-center justify-between px-6 py-4 z-50"
      style={{ backgroundColor: '#2F6235' }}
    >
      <h1 className="text-white text-2xl font-bold">Nutrimax</h1>
      <button className="px-4 py-2 border border-white text-white rounded hover:bg-white hover:text-blue-500 transition">
        Login
      </button>
    </nav>
  );
}
