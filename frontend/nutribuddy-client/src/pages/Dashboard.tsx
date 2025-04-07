import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import {
  Container,
  Paper,
  Typography,
  CircularProgress,
  Button,
  Box,
  Slider,
  Card,
  Chip,
  Switch,
  FormControlLabel,
  MenuItem,
  Select,
  TextField,
} from "@mui/material";
import Navbar from "../components/Navbar";
import { isAuthenticated } from "../utils/auth";

// Define the types for your data
interface MealRecommendation {
  meal_id: number;
  name: string;
  nutrient: string;
  diet: string;
  disease: string;
  is_vegetarian: boolean;
  reason: string;
}

interface ExerciseRecommendation {
  name: string;
  exerciseintensity: number;
  calories_burned: number;
  duration: number;
  weatherconditions: string;
  gender: string;
  age: string;
  bmi_range: string;
}

const Dashboard = () => {
  const navigate = useNavigate();
  const [recommendations, setRecommendations] = useState<MealRecommendation[]>([]);
  const [loading, setLoading] = useState(true);
  const [ratings, setRatings] = useState<{ [key: number]: number }>({});
  const [userName, setUsername] = useState<string>("");
  const [userPreference, setUserPreference] = useState<string>("non-vegetarian");
  const [showExercise, setShowExercise] = useState<boolean>(false);
  const [exerciseRecommendations, setExerciseRecommendations] = useState<ExerciseRecommendation[]>([]);
  const [exerciseLoading, setExerciseLoading] = useState(true);
  const [userWeight, setUserWeight] = useState<number>(0);
  const [userHeight, setUserHeight] = useState<number>(0);
  const [showChangePassword, setShowChangePassword] = useState(false);
  const [oldPassword, setOldPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [refreshingRecommendations, setRefreshingRecommendations] = useState(false);
  
  const API_BASE_URL = process.env.REACT_APP_API_URL || "http://backend:8000";

  const exercise_options: { [key: string]: Array<{ "Exercise Name": string; "Exercise Type": string }> } = {
    "exercise 1": [
      { "Exercise Name": "Jumping Jacks", "Exercise Type": "Cardio" },
      { "Exercise Name": "High Knees", "Exercise Type": "Cardio" },
      { "Exercise Name": "Butt Kicks", "Exercise Type": "Cardio" },
      { "Exercise Name": "Jumping Rope", "Exercise Type": "Cardio" },
      { "Exercise Name": "Lateral Jumps", "Exercise Type": "Cardio" }
    ],
    "exercise 2": [
      { "Exercise Name": "Push-ups", "Exercise Type": "Strength" },
      { "Exercise Name": "Diamond Push-ups", "Exercise Type": "Strength" },
      { "Exercise Name": "Wide Push-ups", "Exercise Type": "Strength" },
      { "Exercise Name": "Decline Push-ups", "Exercise Type": "Strength" },
      { "Exercise Name": "Incline Push-ups", "Exercise Type": "Strength" }
    ],
    "exercise 3": [
      { "Exercise Name": "Burpees", "Exercise Type": "Cardio & Strength" },
      { "Exercise Name": "Mountain Climbers", "Exercise Type": "Cardio & Strength" },
      { "Exercise Name": "Squat Jumps", "Exercise Type": "Cardio & Strength" },
      { "Exercise Name": "Plank Jacks", "Exercise Type": "Cardio & Strength" },
      { "Exercise Name": "Jump Lunges", "Exercise Type": "Cardio & Strength" }
    ],
    "exercise 4": [
      { "Exercise Name": "Plank", "Exercise Type": "Core" },
      { "Exercise Name": "Side Plank", "Exercise Type": "Core" },
      { "Exercise Name": "Hollow Hold", "Exercise Type": "Core" },
      { "Exercise Name": "Superman Hold", "Exercise Type": "Core" },
      { "Exercise Name": "Bird Dog", "Exercise Type": "Core" }
    ],
    "exercise 5": [
      { "Exercise Name": "Squats", "Exercise Type": "Strength" },
      { "Exercise Name": "Sumo Squats", "Exercise Type": "Strength" },
      { "Exercise Name": "Goblet Squats", "Exercise Type": "Strength" },
      { "Exercise Name": "Bulgarian Split Squats", "Exercise Type": "Strength" },
      { "Exercise Name": "Pistol Squats", "Exercise Type": "Strength" }
    ],
    "exercise 6": [
      { "Exercise Name": "Mountain Climbers", "Exercise Type": "Cardio & Strength" },
      { "Exercise Name": "Burpees", "Exercise Type": "Cardio & Strength" },
      { "Exercise Name": "Bear Crawls", "Exercise Type": "Cardio & Strength" },
      { "Exercise Name": "Kettlebell Swings", "Exercise Type": "Cardio & Strength" },
      { "Exercise Name": "Battle Ropes", "Exercise Type": "Cardio & Strength" }
    ],
    "exercise 7": [
      { "Exercise Name": "Pull-ups", "Exercise Type": "Strength" },
      { "Exercise Name": "Chin-ups", "Exercise Type": "Strength" },
      { "Exercise Name": "Lat Pulldowns", "Exercise Type": "Strength" },
      { "Exercise Name": "Inverted Rows", "Exercise Type": "Strength" },
      { "Exercise Name": "Australian Pull-ups", "Exercise Type": "Strength" }
    ],
    "exercise 8": [
      { "Exercise Name": "Lunges", "Exercise Type": "Strength" },
      { "Exercise Name": "Reverse Lunges", "Exercise Type": "Strength" },
      { "Exercise Name": "Walking Lunges", "Exercise Type": "Strength" },
      { "Exercise Name": "Side Lunges", "Exercise Type": "Strength" },
      { "Exercise Name": "Curtsy Lunges", "Exercise Type": "Strength" }
    ],
    "exercise 9": [
      { "Exercise Name": "High Knees", "Exercise Type": "Cardio" },
      { "Exercise Name": "Jumping Jacks", "Exercise Type": "Cardio" },
      { "Exercise Name": "Skipping", "Exercise Type": "Cardio" },
      { "Exercise Name": "Box Jumps", "Exercise Type": "Cardio" },
      { "Exercise Name": "Burpees", "Exercise Type": "Cardio" }
    ],
    "exercise 10": [
      { "Exercise Name": "Sit-ups", "Exercise Type": "Core" },
      { "Exercise Name": "Crunches", "Exercise Type": "Core" },
      { "Exercise Name": "Russian Twists", "Exercise Type": "Core" },
      { "Exercise Name": "Bicycle Crunches", "Exercise Type": "Core" },
      { "Exercise Name": "Leg Raises", "Exercise Type": "Core" }
    ],
  };
  
  // Function to get a random exercise from the options
  const getRandomExercise = (exerciseName: string) => {
    const options = exercise_options[exerciseName] || [];
    if (options.length === 0) {
      return { "Exercise Name": exerciseName, "Exercise Type": "General" };
    }
    return options[Math.floor(Math.random() * options.length)];
  };
  // Redirect to login if not authenticated
  useEffect(() => {
    if (!isAuthenticated()) {
      navigate("/");
    }
  }, [navigate]);

  useEffect(() => {
    fetchRecommendations();

    // Get username and diet preference from localStorage
    const storedUserName = localStorage.getItem("username");
    const storedDietPreference = localStorage.getItem("userDietPreference");
    const storedWeight = localStorage.getItem("userWeight");
    const storedHeight = localStorage.getItem("userHeight");
    if (storedUserName) {
      setUsername(storedUserName);
    }

    if (storedDietPreference) {
      setUserPreference(storedDietPreference);
    }
    if (storedHeight) setUserHeight(parseFloat(storedHeight));
    if (storedWeight) setUserWeight(parseFloat(storedWeight));
  }, []);

  useEffect(() => {
    if (showExercise && userHeight && userWeight) {
      fetchExerciseRecommendations();
    }
  }, [showExercise, userHeight, userWeight]);

  const fetchRecommendations = async () => {
    const userId = localStorage.getItem("user_id");

    if (!userId || userId === "undefined") {
      console.error("No user ID found in localStorage");
      return;
    }

    try {
      const response = await axios.get(`${API_BASE_URL}/api/v1/recommender/recommend/${userId}`);
      setRecommendations(response.data.recommendations);
    } catch (error) {
      console.error("Error fetching recommendations", error);
    } finally {
      setLoading(false);
    }
  };

  const fetchExerciseRecommendations = async () => {
    const userId = localStorage.getItem("user_id");
    if (!userId || userId === "undefined") {
      console.error("No user ID found in localStorage");
      return;
    }
    setExerciseLoading(true);
    try {
      const response = await axios.post(`${API_BASE_URL}/api/v1/recommender/exercise/${userId}`, {
        height: userHeight,
        weight: userWeight,
      });
      setExerciseRecommendations(response.data.recommendations);
    } catch (error) {
      console.error("Error in fetching the exercise recommendations", error);
    } finally {
      setExerciseLoading(false);
    }
  };

  const handleInteraction = async (mealId: number, action: string, rating: number | null = null) => {
    const userId = localStorage.getItem("user_id");
    if (!userId) return;

    try {
      await axios.post(`${API_BASE_URL}/api/v1/recommender/interact`, {
        user_id: parseInt(userId as string),
        meal_id: mealId,
        action: action,
        rating: rating,
      });

      setRecommendations((prevRecs) => {
        let updatedRecs = [...prevRecs];

        if (action === "dislike") {
          updatedRecs = prevRecs.filter((rec) => rec.meal_id !== mealId);
          fetchNewRecommendation(updatedRecs);
        } else if (action === "like" || action === "buy" || (action === "rate" && rating && rating >= 4)) {
          const mealIndex = updatedRecs.findIndex((rec) => rec.meal_id === mealId);
          if (mealIndex !== -1) {
            const [favoriteMeal] = updatedRecs.splice(mealIndex, 1);
            updatedRecs.unshift(favoriteMeal); // Move top
          }
        }

        return updatedRecs;
      });
    } catch (error) {
      console.error(`Error when trying to ${action} meal`, error);
    }
  };

  const handleToggleExercise = () => {
    setShowExercise((prev) => !prev);
  };

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    const token = localStorage.getItem("token");
    const userId = localStorage.getItem("user_id");

    try {
      await axios.put(
        `${API_BASE_URL}/api/v1/users/change-password/${userId}`,
        {
          old_password: oldPassword,
          new_password: newPassword,
        },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      alert("Password changed successfully!");
      setShowChangePassword(false);
      setOldPassword("");
      setNewPassword("");
    } catch (error) {
      console.error("Failed to change password", error);
      alert("Failed to change password. Please try again.");
    }
  };

  const handleRerunRecommendations = async () => {
    const userId = localStorage.getItem("user_id");
    if (!userId) return;
    
    setRefreshingRecommendations(true);
    try {
      // First refresh meal recommendations
      await axios.post(`${API_BASE_URL}/api/v1/recommender/refresh-recommendations/${userId}`);
      
      // Then fetch the updated recommendations
      await fetchRecommendations();
      
      // If exercise tab is showing, refresh exercise recommendations too
      if (showExercise && userHeight && userWeight) {
        await fetchExerciseRecommendations();
      }
      
      alert("Recommendations refreshed successfully!");
    } catch (error) {
      console.error("Failed to refresh recommendations", error);
      alert("Failed to refresh recommendations.");
    } finally {
      setRefreshingRecommendations(false);
    }
  };

  const getIntensityLabel = (intensity: number): string => {
    if (intensity <= 3) return "Low";
    if (intensity <= 7) return "Medium";
    return "High";
  };

  const fetchNewRecommendation = async (currentRecommendations: MealRecommendation[]) => {
    const userId = localStorage.getItem("user_id");

    if (!userId || userId === "undefined") {
      console.error("No user ID found in localStorage");
      return;
    }

    try {
      const response = await axios.get(`${API_BASE_URL}/api/v1/recommender/recommend/${userId}`);
      const newRecommendations = response.data.recommendations.filter(
        (rec: any) => !currentRecommendations.some((existing) => existing.meal_id === rec.meal_id)
      );

      // Ensure at least 10 meals remain in the list
      while (currentRecommendations.length < 10 && newRecommendations.length > 0) {
        currentRecommendations.push(newRecommendations.shift());
      }

      setRecommendations([...currentRecommendations]);
    } catch (error) {
      console.error("Error fetching additional recommendations", error);
    }
  };

  const handleRatingChange = (mealId: number, newValue: number) => {
    setRatings((prevRatings) => ({ ...prevRatings, [mealId]: newValue }));
  };

  // Determine tag color based on user preference and meal type
  const getTagColor = (isMealVegetarian: Boolean) => {
    const isUserVegetarian = userPreference === "vegetarian";

    if (isUserVegetarian) {
      // For vegetarian users: green for veg, red for non-veg
      return isMealVegetarian ? "success" : "error";
    } else {
      // For non-vegetarian users: green for both
      return isMealVegetarian ? "success" : "error";
    }
  };

  return (
    <div style={{ backgroundColor: "#f5f5f5", minHeight: "100vh" }}>
      <Container>
        <Paper elevation={3} style={{ padding: "20px", marginTop: "50px", textAlign: "center" }}>
          <Typography variant="h5" color="textPrimary">
            Welcome to your Dashboard {userName}!
          </Typography>
          <Typography variant="body1" color="textSecondary" style={{ marginTop: "10px" }}>
            Here you can interact with meals to improve recommendations.
          </Typography>

          <Box sx={{ mt: 3, display: 'flex', justifyContent: 'space-between' }}>
            <Select
              value={showChangePassword ? "change-password" : ""}
              onChange={(e) => setShowChangePassword(e.target.value === "change-password")}
              displayEmpty
              style={{ width: "200px" }}
            >
              <MenuItem value="" disabled>
                Account Options
              </MenuItem>
              <MenuItem value="change-password">Change Password</MenuItem>
            </Select>

            <Button 
              variant="contained" 
              color="primary"
              onClick={handleRerunRecommendations}
              disabled={refreshingRecommendations}
            >
              {refreshingRecommendations ? "Refreshing..." : "Refresh Recommendations"}
            </Button>
          </Box>

          {showChangePassword && (
            <form onSubmit={handleChangePassword} style={{ marginTop: "20px" }}>
              <TextField
                label="Old Password"
                type="password"
                fullWidth
                margin="normal"
                value={oldPassword}
                onChange={(e) => setOldPassword(e.target.value)}
                required
              />
              <TextField
                label="New Password"
                type="password"
                fullWidth
                margin="normal"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                required
              />
              <Button
                type="submit"
                variant="contained"
                color="primary"
                fullWidth
                style={{ marginTop: "10px" }}
              >
                Change Password
              </Button>
            </form>
          )}

          <FormControlLabel
            control={<Switch checked={showExercise} onChange={handleToggleExercise} />}
            label={showExercise ? "Show Diet Recommendations" : "Show Exercise Recommendations"}
            style={{ margin: "20px 0" }}
          />

          {!showExercise ? (
            <div style={{ marginTop: "30px", textAlign: "left" }}>
              <Typography variant="h6">Your Recommended Meals:</Typography>
              {loading ? (
                <CircularProgress style={{ marginTop: "10px" }} />
              ) : recommendations.length > 0 ? (
                <ul style={{ listStyle: "none", padding: 0 }}>
                  {recommendations.map((rec, index) => {
                    console.log(rec.is_vegetarian);
                    const isMealVegetarian = rec.is_vegetarian;
                    return (
                      <Card key={index} sx={{ mb: 2, p: 2 }}>
                        <Box display="flex" justifyContent="space-between" alignItems="center">
                          <Typography variant="h6">{rec.name}</Typography>
                          <Chip
                            label={isMealVegetarian ? "Vegetarian" : "Non-Vegetarian"}
                            color={getTagColor(isMealVegetarian)}
                            size="small"
                          />
                        </Box>

                        <Typography variant="body2">Nutrients: {rec.nutrient}</Typography>
                        <Typography variant="body2">Diet: {rec.diet}</Typography>
                        <Typography variant="body2">Good for: {rec.disease}</Typography>

                        <Box display="flex" justifyContent="space-between" alignItems="center" mt={2}>
                          <div>
                            <Button
                              variant="contained"
                              color="primary"
                              size="small"
                              onClick={() => handleInteraction(rec.meal_id, "like")}
                            >
                              👍 Like
                            </Button>

                            <Button
                              variant="contained"
                              color="secondary"
                              size="small"
                              style={{ marginLeft: "5px" }}
                              onClick={() => handleInteraction(rec.meal_id, "dislike")}
                            >
                              👎 Dislike
                            </Button>

                            <Button
                              variant="contained"
                              color="success"
                              size="small"
                              style={{ marginLeft: "5px" }}
                              onClick={() => handleInteraction(rec.meal_id, "buy")}
                            >
                              🛒 Buy
                            </Button>
                          </div>
                        </Box>

                        <Box display="flex" alignItems="center" mt={1}>
                          <Typography variant="body2" style={{ marginRight: "10px" }}>
                            Rate:
                          </Typography>
                          <Slider
                            value={ratings[rec.meal_id] || 3}
                            onChange={(event, newValue) => handleRatingChange(rec.meal_id, newValue as number)}
                            step={1}
                            marks
                            min={1}
                            max={5}
                            style={{ width: "150px" }}
                          />
                          <Button
                            variant="outlined"
                            color="primary"
                            size="small"
                            style={{ marginLeft: "10px" }}
                            onClick={() => handleInteraction(rec.meal_id, "rate", ratings[rec.meal_id])}
                          >
                            Submit Rating
                          </Button>
                        </Box>
                      </Card>
                    );
                  })}
                </ul>
              ) : (
                <Typography variant="body2" color="textSecondary">
                  No recommendations available.
                </Typography>
              )}
            </div>
          ) : (
            <div style={{ marginTop: "30px", textAlign: "left" }}>
              <Typography variant="h6">Your Exercise Recommendations:</Typography>
              {!userHeight || !userWeight ? (
                <Card sx={{ p: 3, mt: 2, textAlign: "center" }}>
                  <Typography variant="body1" color="error">
                    Height or weight information not available. Please update your profile.
                  </Typography>
                </Card>
              ) : exerciseLoading ? (
                <Box sx={{ display: "flex", justifyContent: "center", mt: 4 }}>
                  <CircularProgress />
                </Box>
              ) : exerciseRecommendations.length > 0 ? (
                <ul style={{ listStyle: "none", padding: 0 }}>
                  {exerciseRecommendations.map((exercise, index) => {
  // Get a random exercise from the options for this exercise name
  const randomExercise = getRandomExercise(exercise.name);
  
  return(
    <Card key={index} sx={{ mb: 2, p: 2 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center">
        <Typography variant="h6">{randomExercise["Exercise Name"]}</Typography>
        <Chip
          label={getIntensityLabel(exercise.exerciseintensity)}
          color={
            exercise.exerciseintensity > 7 ? "error" : exercise.exerciseintensity > 3 ? "warning" : "success"
          }
          size="small"
        />
      </Box>

      <Typography variant="body2">Calories Burn: {Math.round(exercise.calories_burned)} kcal</Typography>
      <Typography variant="body2">Duration: {5} minutes</Typography>
      <Typography variant="body2">Type: {randomExercise["Exercise Type"]}</Typography>

      <Box mt={1}>
        <Typography variant="body2">Target BMI: {exercise.bmi_range}</Typography>
      </Box>
    </Card>
  );
})}
                </ul>
              ) : (
                <Typography variant="body2" color="textSecondary">
                  No exercise recommendations available.
                </Typography>
              )}
            </div>
          )}
        </Paper>
      </Container>
    </div>
  );
};

export default Dashboard;
