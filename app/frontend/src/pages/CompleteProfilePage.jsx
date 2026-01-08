import { useState } from "react";
import { useNavigate } from "react-router-dom";
import NavbarLogo from "../components/NavbarLogo.jsx";
import Footer from "../components/Footer.jsx";

export default function CompleteProfilePage() {
  const navigate = useNavigate();

  const [msg, setMsg] = useState("");
  const [msgType, setMsgType] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMsg("");

    const form = new FormData(e.target);

    const body = {
      age: Number(form.get("age")),
      gender: form.get("gender"),
      weight: Number(form.get("weight")),
      height: Number(form.get("height")),
      isVegan: form.get("isVegan") === "true",
      isVegetarian: form.get("isVegetarian") === "true",
      isDairyInt: form.get("isDairyInt") === "true",
      goal: form.get("goal"),
      activityFactor: form.get("activityFactor"),
    };

    try {
      const res = await fetch("/profile/completeInfo", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify(body),
    });


      const text = await res.text();
      console.log(res.status, text);
      if (res.ok) {
        setMsgType("ok");
        setMsg("Saved. Redirecting...");
        setTimeout(() => navigate("/"), 800);
      } else {
        setMsgType("err");
        setMsg(`Error ${res.status}: ${text}`);
      }
    } catch (err) {
      setMsgType("err");
      setMsg(err.message || "Failed");
    }
  };

  return (
    <>
      <NavbarLogo />

      <div className="pt-32 pb-32 max-w-xl sm:max-w-xl mx-auto">
        <form
          onSubmit={handleSubmit}
          className="space-y-6 bg-white p-8 rounded-xl shadow-lg"
        >
          <h1 className="text-2xl font-bold text-brandGreen text-center">
            Complete Your Registration
          </h1>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-sm text-black font-medium">Age</label>
              <input
                name="age"
                type="number"
                min="10"
                max="120"
                required
                className="w-full mt-1 p-2 border rounded text-black focus:outline-none focus:ring-2 focus:ring-brandGreen/70"
              />
            </div>

            <div>
              <label className="text-sm text-black font-medium">Gender</label>
              <select
                name="gender"
                required
                className="w-full mt-1 p-2 border rounded text-black bg-white focus:outline-none focus:ring-2 focus:ring-brandGreen/70"
              >
                <option value="MALE">Male</option>
                <option value="FEMALE">Female</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-sm text-black font-medium">Weight (kg)</label>
              <input
                name="weight"
                type="number"
                step="0.1"
                min="1"
                required
                className="w-full mt-1 p-2 border rounded text-black focus:outline-none focus:ring-2 focus:ring-brandGreen/70"
              />
            </div>

            <div>
              <label className="text-sm text-black font-medium">Height (cm)</label>
              <input
                name="height"
                type="number"
                step="0.1"
                min="50"
                required
                className="w-full mt-1 p-2 border rounded text-black focus:outline-none focus:ring-2 focus:ring-brandGreen/70"
              />
            </div>
          </div>

          <div className="grid grid-cols-3 gap-4">
            <div>
              <label className="text-sm text-black font-medium">Vegan?</label>
              <select
                name="isVegan"
                className="w-full mt-1 p-2 border rounded bg-white text-black focus:ring-2 focus:ring-brandGreen/70"
              >
                <option value="false">No</option>
                <option value="true">Yes</option>
              </select>
            </div>

            <div>
              <label className="text-sm text-black font-medium">Vegetarian?</label>
              <select
                name="isVegetarian"
                className="w-full mt-1 p-2 border rounded bg-white text-black focus:ring-2 focus:ring-brandGreen/70"
              >
                <option value="false">No</option>
                <option value="true">Yes</option>
              </select>
            </div>

            <div>
              <label className="text-sm text-black font-medium">Dairy products?</label>
              <select
                name="isDairyInt"
                className="w-full mt-1 p-2 border rounded bg-white text-black focus:ring-2 focus:ring-brandGreen/70"
              >
                <option value="false">Yes</option>
                <option value="true">No (intolerance)</option>
              </select>
            </div>
          </div>

          <div>
            <label className="text-sm text-black font-medium">Goal</label>
            <select
              name="goal"
              required
              className="w-full mt-1 p-2 border rounded bg-white text-black focus:ring-2 focus:ring-brandGreen/70"
            >
              <option value="MAINTAIN">Maintain weight</option>
              <option value="LOSE">Lose weight</option>
              <option value="GAIN">Gain weight</option>
            </select>
          </div>

          <div>
            <label className="text-sm text-black font-medium">Activity Level</label>
            <select
              name="activityFactor"
              required
              className="w-full mt-1 p-2 border rounded bg-white text-black focus:ring-2 focus:ring-brandGreen/70"
            >
              <option value="SEDENTARY">Sedentary (little movement)</option>
              <option value="LIGHT">Light (1–3x per week)</option>
              <option value="MODERATE">Moderate (3–5x per week)</option>
              <option value="ACTIVE">Active (6–7x per week)</option>
              <option value="VERY_ACTIVE">Very active (2x per day)</option>
            </select>
          </div>

          <button
            type="submit"
            className="w-full py-2 bg-brandGreen text-white rounded hover:bg-green-700 transition"
          >
            Save
          </button>

          {msg && (
            <p
              className={`text-sm text-center ${
                msgType === "ok" ? "text-green-600" : "text-red-500"
              }`}
            >
              {msg}
            </p>
          )}
        </form>
      </div>

      <Footer />
    </>
  );
}
