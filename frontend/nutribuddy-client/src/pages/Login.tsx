import axios from "axios";
import { useNavigate, Link } from "react-router-dom";
import { useState } from "react";
import { Container, TextField, Button, Typography, Paper, Box, CircularProgress } from "@mui/material";
import { isAuthenticated } from "../utils/auth";  // ✅ Import authentication check

const Login = () => {
  const [userName, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const API_BASE_URL = process.env.REACT_APP_API_URL || "http://backend:8000";

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${API_BASE_URL}/api/v1/users/login`, {
        username: userName,  // ✅ Ensure correct field name
        password,
      });
  
      // ✅ Store token in localStorage
      localStorage.setItem("token", response.data.access_token);
      localStorage.setItem("username", userName);
  
      // ✅ Store user ID to fetch recommendations later (Fix applied)
      if (response.data.user_id) {
        localStorage.setItem("user_id", response.data.user_id);
        
        // Add the recommendation refresh code here
        console.log("Refreshing recommendations for user:", response.data.user_id);
        try {
          const refreshResponse = await axios.post(
            `${API_BASE_URL}/api/v1/recommender/refresh-recommendations/${response.data.user_id}`
          );
          console.log("Refresh response:", refreshResponse.data);
        } catch (error) {
          console.error("Failed to refresh recommendations:", error);
        }
        
      } else {
        console.error("User ID missing from response");
      }
  
      // ✅ Redirect to Dashboard after login
      navigate("/dashboard");
    } catch (error) {
      console.error("Login failed", error);
    }
  };

  // If already authenticated, redirect to Dashboard
  if (isAuthenticated()) {
    navigate("/dashboard");
    return null;
  }

  return (
    <Container component="main" maxWidth="xs">
      <Paper elevation={3} style={{ padding: "20px", marginTop: "50px" }}>
        <Typography variant="h5" align="center">
          Login
        </Typography>
        {error && (
          <Typography color="error" align="center" style={{ marginTop: "10px" }}>
            {error}
          </Typography>
        )}
        <form onSubmit={handleSubmit}>
          <TextField
            fullWidth
            label="Username"
            margin="normal"
            onChange={(e) => setUsername(e.target.value)}
            disabled={loading}
            required
          />
          <TextField
            fullWidth
            label="Password"
            type="password"
            margin="normal"
            onChange={(e) => setPassword(e.target.value)}
            disabled={loading}
            required
          />
          <Button
            fullWidth
            type="submit"
            variant="contained"
            color="primary"
            style={{ marginTop: "10px" }}
            disabled={loading}
          >
            {loading ? <CircularProgress size={24} color="inherit" /> : "Login"}
          </Button>
        </form>

        {/* Signup Link */}
        <Box mt={2} textAlign="center">
          <Typography variant="body2">
            No account?{" "}
            <Link to="/signup" style={{ color: "#1976d2", textDecoration: "none" }}>
              Sign Up
            </Link>
          </Typography>
        </Box>
      </Paper>
    </Container>
  );
};

export default Login;
