import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { Container, TextField, Button, Typography, Paper } from "@mui/material";

const Signup = () => {
  const [userName, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [history, setHistory] = useState("");
  const [height, setHeight] = useState("");
  const [weight, setWeight] = useState("");
  const navigate = useNavigate();

  const calculateBMI = (height: number, weight: number) => {
    return (weight / ((height / 100) * (height / 100))).toFixed(2);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const bmi = calculateBMI(Number(height), Number(weight));

    try {
      await axios.post("http://localhost:8000/auth/signup", {
        userName,
        password,
        history,
        height: Number(height),
        weight: Number(weight),
        bmi: Number(bmi),
      });
      navigate("/");
    } catch (error) {
      console.error("Signup failed", error);
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
          <TextField
            fullWidth
            label="Disease History"
            multiline
            rows={6}  // Increased height
            sx={{ minHeight: "120px" }}  // Added extra height
            margin="normal"
            onChange={(e) => setHistory(e.target.value)}
            required
          />
          <TextField
            fullWidth
            label="Height (cm)"
            type="number"
            margin="normal"
            onChange={(e) => setHeight(e.target.value)}
            required
          />
          <TextField
            fullWidth
            label="Weight (kg)"
            type="number"
            margin="normal"
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
