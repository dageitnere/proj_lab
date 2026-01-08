import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import NavbarLogo from "../components/NavbarLogo.jsx";
import Footer from "../components/Footer.jsx";

export default function ResetPasswordPage() {
  const navigate = useNavigate();

  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [isOk, setIsOk] = useState(false);

  const getToken = () => {
    return new URL(window.location.href).searchParams.get("token") || "";
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");

    try {
      const res = await fetch("/auth/reset-password/confirm", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({
          token: getToken(),
          new_password: password,
        }),
      });

      const data = await res.json().catch(() => ({}));

      if (!res.ok) {
        setIsOk(false);
        setMessage(data.detail || "Failed to reset password.");
        return;
      }

      setIsOk(true);
      setMessage("Password successfully changed. Redirecting...");

      setTimeout(() => navigate("/?login=open"), 900);
    } catch (err) {
      setIsOk(false);
      setMessage("Failed to change password.");
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
            Change Password
          </h2>

          <div>
            <input
              type="password"
              placeholder="New Password"
              value={password}
              minLength={8}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full p-2 border mb-1 rounded text-black
                         focus:outline-none focus:ring-2 focus:ring-brandGreen/70"
              required
            />
            <p className="text-sm text-gray-600">
              At least 8 characters, 1 uppercase letter, 1 number, 1 special symbol.
            </p>
          </div>

          {message && (
            <p
              className={`text-sm mb-1 text-center ${
                isOk ? "text-green-600" : "text-red-500"
              }`}
            >
              {message}
            </p>
          )}

          <button
            type="submit"
            className="w-full py-2 bg-brandGreen text-white rounded
                       hover:bg-green-700 transition"
          >
            Change
          </button>

          <p className="mt-2 text-sm text-brandGreen text-center">
            <Link to="/?login=open" className="hover:underline font-semibold">
              Back to Login
            </Link>
          </p>
        </form>
      </div>

      <Footer />
    </>
  );
}
