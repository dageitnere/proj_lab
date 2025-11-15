import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import RegisterPage from "./pages/RegisterPage";
import ForgotPasswordPage from "./pages/ForgotPasswordPage";
import NewPage from "./pages/NewPage.jsx";
import Footer from "./components/Footer.jsx";

export default function App() {
  return (
    <Router>
      <div className="min-h-screen bg-[#2F6235] text-white">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/new-page" element={<NewPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/forgot-password" element={<ForgotPasswordPage />} />
        </Routes>
          <Footer />
      </div>
    </Router>
  );
}
