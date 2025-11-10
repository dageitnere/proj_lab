import { useState } from "react";

export default function LoginForm({ onSuccess }) {
  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const res = await fetch("http://localhost:8000/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({ login, password }),
      });

      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error(data.detail || "Error");
      }

      const data = await res.json();
      console.log("Logged in as:", data.username);

      if (onSuccess) onSuccess();
    } catch (err) {
      setError(err.message || "Login failed");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <h2 className="text-2xl font-bold mb-2 text-black brandGreen">
        Login
      </h2>

      <div>
        <input
          type="text"
          placeholder="Username"
          value={login}
          onChange={(e) => setLogin(e.target.value)}
          className="w-full p-2 border mb-2 rounded text-black focus:outline-none focus:ring-2 focus:ring-brandGreen/70"
          required
        />
      </div>

      <div>
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full p-2 border mb-2 rounded text-black focus:outline-none focus:ring-2 focus:ring-brandGreen/70"
          required
        />
      </div>

      {error && (
        <p className="text-red-500 text-sm mb-1">
          {error}
        </p>
      )}

      <button
        type="submit"
        className="w-full py-2 bg-brandGreen text-white rounded hover:bg-green-700 transition"
      >
        Login
      </button>

      <div className="flex justify-between mt-2 text-sm text-brandGreen">
        <a href="/register" className="hover:underline">
          Register
        </a>
        <a href="/forgot-password" className="hover:underline">
          Forgot password?
        </a>
      </div>
    </form>
  );
}
