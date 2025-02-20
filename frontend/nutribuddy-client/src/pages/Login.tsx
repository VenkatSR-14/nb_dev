import axios from "axios";
import { useNavigate, Link } from "react-router-dom";
import { useState } from "react";
import { Container, TextField, Button, Typography, Paper, Box } from "@mui/material";
import { isAuthenticated } from "../utils/auth";  // ✅ Import authentication check

const Login = () => {
  const [userName, setUsername] = useState("");
  const [password, setPassword] = useState("");
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

      // ✅ Store user ID to fetch recommendations later (Fix applied)
      if (response.data.user_id) {
        localStorage.setItem("user_id", response.data.user_id);
      } else {
        console.error("User ID missing from response");
      }

      // ✅ Redirect to Dashboard after login
      navigate("/dashboard");
    } catch (error) {
      console.error("Login failed", error);
    }
  };

  // ✅ If already authenticated, redirect to Dashboard
  if (isAuthenticated()) {
    navigate("/dashboard");
  }

  return (
    <Container component="main" maxWidth="xs">
      <Paper elevation={3} style={{ padding: "20px", marginTop: "50px" }}>
        <Typography variant="h5" align="center">
          Login
        </Typography>
        <form onSubmit={handleSubmit}>
          <TextField
            fullWidth
            label="Username"
            margin="normal"
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <TextField
            fullWidth
            label="Password"
            type="password"
            margin="normal"
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <Button
            fullWidth
            type="submit"
            variant="contained"
            color="primary"
            style={{ marginTop: "10px" }}
          >
            Login
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
