import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import RegisterPage from "./pages/RegisterPage";
import ForgotPasswordPage from "./pages/ForgotPasswordPage";
import VerificationPage from "./pages/VerificationPage.jsx";
import NewPage from "./pages/NewPage.jsx";


export default function App() {
  return (
    <Router>
      <div className="min-h-screen bg-noise-light text-white">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/new-page" element={<NewPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/forgot-password" element={<ForgotPasswordPage />} />
          <Route path="/verification" element={<VerificationPage />} />
        </Routes>

      </div>
    </Router>
  );
}
