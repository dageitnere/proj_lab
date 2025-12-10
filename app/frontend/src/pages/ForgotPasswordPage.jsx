import { useState } from "react";
import { Link } from "react-router-dom";
import NavbarLogo from "../components/NavbarLogo.jsx";
import Footer from "../components/Footer.jsx";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [msg, setMsg] = useState("");
  const [success, setSuccess] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMsg("");
    setSuccess(null);

    try {
      const res = await fetch("http://localhost:8000/auth/forgot-password/start", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email: email.trim() }),
      });

      if (res.ok) {
        setSuccess(true);
        setMsg("If this email exists, a reset link has been sent.");
      } else {
        setSuccess(false);
        setMsg("Failed to send reset link.");
      }

    } catch {
      setSuccess(false);
      setMsg("Failed to send reset link.");
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
          <h2 className="text-2xl font-bold mb-2 text-brandGreen">
            Forgot your password?
          </h2>

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

          {msg && (
            <p
              className={`text-sm ${
                success ? "text-green-600" : "text-red-500"
              }`}
            >
              {msg}
            </p>
          )}

          <button
            type="submit"
            className="w-full py-2 bg-brandGreen text-white rounded
                       hover:bg-green-700 transition"
          >
            Send reset link
          </button>

          <p className="mt-2 text-sm text-brandGreen text-center">
            <Link to="/auth/login" className="hover:underline font-semibold">
              Back to login
            </Link>
          </p>
        </form>
      </div>

      <Footer />
    </>
  );
}
