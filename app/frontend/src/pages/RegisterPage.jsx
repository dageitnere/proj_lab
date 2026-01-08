import NavbarLogo from "../components/NavbarLogo.jsx";
import Footer from "../components/Footer.jsx";
import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";

export default function RegisterPage() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const res = await fetch("/auth/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({ username, email, password }),
      });

      const data = await res.json().catch(() => ({}));

      if (!res.ok) {
        if (typeof data.detail === "string") throw new Error(data.detail);

        if (Array.isArray(data.detail)) {
          const msg = data.detail
            .map((e) => e.msg || e.detail)
            .filter(Boolean)
            .join(", ");
          throw new Error(msg);
        }

        throw new Error("Registration failed");
      }

      navigate(`/verification?email=${encodeURIComponent(email)}`);
    } catch (err) {
      setError(err.message || "Registration failed");
    }
  };

  return (
    <>
      <NavbarLogo />

      <div className="pt-32 flex justify-center">
        <form
          onSubmit={handleSubmit}
          className="space-y-4 bg-white p-10 rounded-lg w-96 shadow-lg"
        >
          <h2 className="text-2xl font-bold mb-2 text-brandGreen">Register</h2>

          <div>
            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full p-2 border mb-2 rounded text-black
                         focus:outline-none focus:ring-2 focus:ring-brandGreen/70"
              required
            />
          </div>

          <div>
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full p-2 border mb-2 rounded text-black
                         focus:outline-none focus:ring-2 focus:ring-brandGreen/70"
              required
            />
          </div>

          <div>
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full p-2 border mb-2 rounded text-black
                         focus:outline-none focus:ring-2 focus:ring-brandGreen/70"
              required
            />
          </div>

          <p className="text-sm text-gray-600">
            At least 8 characters, 1 uppercase letter, 1 number, and 1 special symbol.
          </p>

          {error && <p className="text-red-500 text-sm mb-1">{error}</p>}

          <button
            type="submit"
            className="w-full py-2 bg-brandGreen text-white rounded
                       hover:bg-green-700 transition"
          >
            Register
          </button>

          <p className="mt-2 text-sm text-brandGreen text-center">
            Already have an account?{" "}
            <Link to="/?login=open" className="hover:underline font-semibold">
              Log in
            </Link>
          </p>
        </form>
      </div>

      <Footer />
    </>
  );
}
