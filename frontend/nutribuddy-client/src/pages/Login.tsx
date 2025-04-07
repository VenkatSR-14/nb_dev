import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate, Link } from "react-router-dom";
import {
  Container,
  TextField,
  Button,
  Typography,
  Paper,
  Box,
  CircularProgress,
} from "@mui/material";
import { isAuthenticated } from "../utils/auth";

const Login = () => {
  const [userName, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const API_BASE_URL = process.env.REACT_APP_API_URL || "http://backend:8000";

  // Check authentication status in useEffect instead of during render
  useEffect(() => {
    if (isAuthenticated()) {
      console.log("Already authenticated, redirecting to /dashboard");
      navigate("/dashboard");
    }
  }, [navigate]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const response = await axios.post(`${API_BASE_URL}/api/v1/users/login`, {
        username: userName,
        password,
      });

      localStorage.setItem("token", response.data.access_token);
      localStorage.setItem("username", userName);

      if (response.data.user_id) {
        const userId = response.data.user_id;
        localStorage.setItem("user_id", userId);

        // Fetch user profile data
        try {
          const profileResponse = await axios.get(
            `${API_BASE_URL}/api/v1/users/profile/${userId}`,
            {
              headers: {
                Authorization: `Bearer ${response.data.access_token}`,
              },
            }
          );

          // Store height, weight, and diet preference in localStorage
          if (profileResponse.data.height) {
            localStorage.setItem("userHeight", profileResponse.data.height.toString());
          }
          if (profileResponse.data.weight) {
            localStorage.setItem("userWeight", profileResponse.data.weight.toString());
          }
          if (profileResponse.data.diet_preference) {
            localStorage.setItem("userDietPreference", profileResponse.data.diet_preference);
          }

          console.log("User profile data cached successfully");
        } catch (profileError) {
          console.error("Failed to fetch user profile data:", profileError);
        }

        // Refresh recommendations
        try {
          const refreshResponse = await axios.post(
            `${API_BASE_URL}/api/v1/recommender/refresh-recommendations/${userId}`
          );
          console.log("Refresh response:", refreshResponse.data);
        } catch (refreshError) {
          console.error("Failed to refresh recommendations:", refreshError);
        }
      } else {
        console.error("User ID missing from response");
      }

      setLoading(false);
      console.log("Navigating to /dashboard");
      
      // Use window.location for a hard redirect if navigate isn't working
      window.location.href = "/dashboard";
      // As a fallback, still try the navigate function
      navigate("/dashboard");
      
    } catch (err: any) {
      console.error("Login failed", err);
      setError("Login failed. Please check your credentials.");
      setLoading(false);
    }
  };

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
