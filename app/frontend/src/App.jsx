import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import RegisterPage from "./pages/RegisterPage";
import ForgotPasswordPage from "./pages/ForgotPasswordPage";
import VerificationPage from "./pages/VerificationPage.jsx";
import CompleteProfilePage from "./pages/CompleteProfilePage.jsx";
import ResetPasswordPage from "./pages/ResetPasswordPage.jsx";
import NewPage from "./pages/NewPage.jsx";
import AllProductsPage from "./pages/AllProductsPage.jsx";
import MyProductsPage from "./pages/MyProductsPage.jsx";

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
          <Route path="/complete" element={<CompleteProfilePage />} />
          <Route path="/reset-password" element={<ResetPasswordPage />} />
          <Route path="/products" element={<AllProductsPage />} />
          <Route path="/my-products" element={<MyProductsPage />} />
        </Routes>

      </div>
    </Router>
  );
}
