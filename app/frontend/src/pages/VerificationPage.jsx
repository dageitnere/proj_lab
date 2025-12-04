import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import NavbarLogo from "../components/NavbarLogo.jsx";
import Footer from "../components/Footer.jsx";

export default function VerificationPage() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [code, setCode] = useState("");
  const [messageSend, setMessageSend] = useState("");
  const [messageConfirm, setMessageConfirm] = useState("");

  useEffect(() => {
    const qp = new URL(window.location.href).searchParams.get("email");
    if (qp) {
      sessionStorage.setItem("verify_email", qp);
      setEmail(qp);
    } else {
      const stored = sessionStorage.getItem("verify_email");
      if (stored) setEmail(stored);
    }
  }, []);

  const handleResend = async () => {
    setMessageSend("");
    if (!email) return setMessageSend("Email not found.");

    try {
      const res = await fetch("http://localhost:8000/auth/verification/start", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });

      if (res.ok) {
        setMessageSend("Verification code sent again.");
      } else {
        setMessageSend("Failed to send code.");
      }
    } catch (err) {
      setMessageSend("Failed to send code.");
    }
  };

  const handleConfirmCode = async (e) => {
    e.preventDefault();
    setMessageConfirm("");

    const storedEmail = sessionStorage.getItem("verify_email") || email;
    if (!storedEmail) return setMessageConfirm("Email missing.");

    try {
      const res = await fetch("http://localhost:8000/auth/verification/confirm", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ email: storedEmail, code }),
      });

      if (res.ok) {
        setMessageConfirm("Email verified! Redirecting...");
        setTimeout(() => navigate("/new-page"), 800);
      } else {
        const data = await res.json().catch(() => ({ detail: "Invalid or expired code." }));
        setMessageConfirm(data.detail || "Invalid or expired code.");
      }
    } catch (err) {
      setMessageConfirm("Invalid or expired code.");
    }
  };

  return (
    <>
      <NavbarLogo />

      <div className="pt-32 max-w-md mx-auto">
        <form onSubmit={handleConfirmCode} className="space-y-5 bg-white p-8 rounded-lg shadow-lg">
          <h2 className="text-2xl font-bold text-brandGreen text-center">Email Verification</h2>

          <p className="text-sm text-gray-600 text-center">
            Enter the 6-digit code we sent to:<br />
            <span className="font-semibold text-black">{email || "your email"}</span>
          </p>

          <input
            type="text"
            placeholder="Verification Code"
            value={code}
            onChange={(e) => setCode(e.target.value)}
            pattern="\d{6}"
            maxLength={6}
            className="w-full p-2 border rounded text-black focus:outline-none focus:ring-2 focus:ring-brandGreen/70"
            required
          />

          <button
            type="submit"
            className="w-full py-2 bg-brandGreen text-white rounded hover:bg-green-700 transition"
          >
            Confirm
          </button>

          {messageConfirm && (
            <p className={`text-sm text-center ${messageConfirm.includes("verified") ? "text-green-600" : "text-red-500"}`}>
              {messageConfirm}
            </p>
          )}

          <div className="text-center mt-3">
            <p className="text-sm text-gray-600">Didn’t receive the code?</p>
            <button
              type="button"
              onClick={handleResend}
              className="mt-1 text-brandGreen font-semibold hover:underline"
            >
              Send again
            </button>

            {messageSend && (
              <p className={`text-sm mt-1 ${messageSend.includes("sent") ? "text-green-600" : "text-red-500"}`}>
                {messageSend}
              </p>
            )}
          </div>
        </form>

        <p className="text-center text-sm text-brandGreen mt-4">
          <a href="/" className="hover:underline font-semibold">Back to Login</a>
        </p>
      </div>

      <Footer />
    </>
  );
}