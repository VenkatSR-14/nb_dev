import { useState } from "react";
import axios, { AxiosError } from "axios";
import { useNavigate } from "react-router-dom";
import {
  Container,
  TextField,
  Button,
  Typography,
  Paper,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
} from "@mui/material";

const API_BASE_URL = process.env.REACT_APP_API_URL || "http://backend:8000";

const Signup = () => {
  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const [disease, setDisease] = useState<string>("");
  const [height, setHeight] = useState<string>("");
  const [weight, setWeight] = useState<string>("");
  const [vegNon, setVegNon] = useState<string>(""); // Boolean (true for veg, false for non-veg)
  const [gender, setGender] = useState<string>("");
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    try {
      const response = await axios.post(`${API_BASE_URL}/api/v1/users/signup`, {
        username,
        password,
        email,
        disease,
        height: Number(height),
        weight: Number(weight),
        veg_non: vegNon === "1",  // ✅ Converts "1" to true, "0" to false
        gender: gender === "1",   // ✅ Converts "1" to true, "0" to false
      });

      // ✅ Automatically log in after successful signup
      const loginResponse = await axios.post(`${API_BASE_URL}/api/v1/users/login`, {
        username,
        password,
      });

      // ✅ Store token & user ID in localStorage
      localStorage.setItem("token", loginResponse.data.access_token);
      localStorage.setItem("user_id", loginResponse.data.user_id);

      // ✅ Redirect to Dashboard
      navigate("/dashboard");
    } catch (error) {
      const axiosError = error as AxiosError;
      console.error("Signup failed", axiosError);
      alert(
        axiosError.response?.data
          ? JSON.stringify(axiosError.response.data)
          : "Signup failed. Please try again."
      );
    }
  };

  return (
    <Container component="main" maxWidth="xs">
      <Paper elevation={3} style={{ padding: "20px", marginTop: "50px" }}>
        <Typography variant="h5" align="center">
          Sign Up
        </Typography>
        <form onSubmit={handleSubmit}>
          <TextField
            fullWidth
            label="Username"
            margin="normal"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <TextField
            fullWidth
            label="Password"
            type="password"
            margin="normal"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <TextField
            fullWidth
            label="Email"
            type="email"
            margin="normal"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <FormControl fullWidth margin="normal">
            <InputLabel>Gender</InputLabel>
            <Select
              value={gender}
              onChange={(e) => setGender(e.target.value as string)}
              required
            >
              <MenuItem value="" disabled>Select Gender</MenuItem> {/* ✅ Default placeholder */}
              <MenuItem value="0">Male</MenuItem>
              <MenuItem value="1">Female</MenuItem>
            </Select>
          </FormControl>

          <FormControl fullWidth margin="normal">
            <InputLabel>Diet Preference</InputLabel>
            <Select
              value={vegNon}
              onChange={(e) => setVegNon(e.target.value as string)}
              required
            >
              <MenuItem value="" disabled>Select Diet Preference</MenuItem> {/* ✅ Default placeholder */}
              <MenuItem value="0">Vegetarian</MenuItem>
              <MenuItem value="1">Non-Vegetarian</MenuItem>
            </Select>
          </FormControl>

          <TextField
            fullWidth
            label="Disease History"
            multiline
            rows={4}
            margin="normal"
            value={disease}
            onChange={(e) => setDisease(e.target.value)}
            required
          />
          <TextField
            fullWidth
            label="Height (cm)"
            type="number"
            margin="normal"
            value={height}
            onChange={(e) => setHeight(e.target.value)}
            required
          />
          <TextField
            fullWidth
            label="Weight (kg)"
            type="number"
            margin="normal"
            value={weight}
            onChange={(e) => setWeight(e.target.value)}
            required
          />

          <Button
            fullWidth
            type="submit"
            variant="contained"
            color="primary"
            style={{ marginTop: "10px" }}
          >
            Sign Up
          </Button>
        </form>
      </Paper>
    </Container>
  );
};

export default Signup;
