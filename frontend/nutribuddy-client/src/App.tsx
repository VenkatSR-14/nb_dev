import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import Signup from "./pages/Signup";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import UpdateSettings from "./pages/UpdateSettings";
import { isAuthenticated } from "./utils/auth";
import Navbar from "./components/Navbar";

function App() {
  return (
    <Router>
      <Navbar />  {/* Navbar is now available on all pages */}
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/dashboard" element={isAuthenticated() ? <Dashboard /> : <Navigate to="/" />} />
        <Route path="/update-settings" element={isAuthenticated() ? <UpdateSettings /> : <Navigate to="/" />} />
      </Routes>
    </Router>
  );
}

export default App;
