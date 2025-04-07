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
  const [showNoDiseaseMessage, setShowNoDiseaseMessage] = useState(false);
  const [userNameError, setUserNameError] = useState<string | null>(null);
  const [passwordError, setPasswordError] = useState<string | null>(null);
  const [emailError, setEmailError] = useState<string | null>(null);
  const [heightError, setHeightError] = useState<string | null>(null);
  const [weightError, setWeightError] = useState<string | null>(null);
  const [diseaseError, setDiseaseError] = useState<string | null>(null);
  const navigate = useNavigate();

  const validatePassword = (password: string) => {
    if (password.length < 8){
      return "Password must be atleast 8 characters long";
    }
    return true;
  };

  const validateHeight = (height: string) => {
    const heightValue = Number(height);
    if (isNaN(heightValue) || heightValue < 50 || heightValue > 250){
      return "Height value is abnormal, please check again";
    }
    return true;
  }

  const validateWeight = (weight: string) => {
    const weightValue = Number(weight);
    if (isNaN(weightValue) || weightValue < 20 || weightValue > 250){
      return "Weight value is abnormal, please check again";
    }
    return true;
  }

  const validateEmail = (email: string) => {
    const emailRegex = /\S+@\S+\.\S+/;
    if (!emailRegex.test(email)) {
      return "Invalid email format.";
    }
    return true;
  };

  const validateForm = () => {
    let isValid = true;

    const passwordValidation = validatePassword(password);
    if (passwordValidation !== true) {
      setPasswordError(passwordValidation);
      isValid = false;
    } else {
      setPasswordError(null);
    }

    const heightValidation = validateHeight(height);
    if (heightValidation !== true){
      setHeightError(heightValidation);
      isValid = false;
      
    }
    else{
      setHeightError(null);
    }

    const weightValidation = validateWeight(weight);
    if (weightValidation !== true){
      setWeightError(weightValidation);
      isValid = false;
    }
    else{
      setWeightError(null);
    }
    
    const emailValidation = validateEmail(email);
    if (emailValidation !== true){
      setEmailError(emailValidation);
      isValid = false;
    }
    else{
      setEmailError(null);
    }
    
    if (disease === "No diseases detected.") {
      setShowNoDiseaseMessage(true);
    } else {
      setShowNoDiseaseMessage(false);
    }

    return isValid;
  }

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!validateForm()){
      return

    }
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
      // Store token & user ID in localStorage
      localStorage.setItem("token", loginResponse.data.access_token);
      localStorage.setItem("user_id", loginResponse.data.user_id);
      localStorage.setItem("username", username);
      localStorage.setItem("userHeight", height);
      localStorage.setItem("userWeight", weight);
      localStorage.setItem("userDietPreference", vegNon === "0" ? "vegetarian" : "non-vegetarian");

      // ✅ Redirect to Dashboard
      window.location.href = "/dashboard";
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
            error = {!!passwordError}
            helperText = {passwordError || ""}
            required
          />
          <TextField
            fullWidth
            label="Email"
            type="email"
            margin="normal"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            error = {!!emailError}
            helperText = {emailError || ""}
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

          {showNoDiseaseMessage && (
            <Typography variant="body2" color="textSecondary" align="center" style={{ marginBottom: "10px" }}>
              No disease detected using this dataset.
            </Typography>
          )}
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
            error = {!!heightError}
            helperText = {heightError || ""}
            required
          />
          <TextField
            fullWidth
            label="Weight (kg)"
            type="number"
            margin="normal"
            value={weight}
            onChange={(e) => setWeight(e.target.value)}
            error = {!!weightError}
            helperText = {weightError || ""}
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
