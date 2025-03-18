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
} from "@mui/material";
import Navbar from "../components/Navbar";
import { isAuthenticated } from "../utils/auth";

const Dashboard = () => {
  const navigate = useNavigate();
  const [recommendations, setRecommendations] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [ratings, setRatings] = useState<{ [key: number]: number }>({});
  const [userName, setUsername] = useState<string>("");
  const [userPreference, setUserPreference] = useState<string>("non-vegetarian");
  const API_BASE_URL = process.env.REACT_APP_API_URL || "http://backend:8000";

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
    
    if (storedUserName) {
      setUsername(storedUserName);
    }
    
    if (storedDietPreference) {
      setUserPreference(storedDietPreference);
    }
  }, []);

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

  const handleInteraction = async (mealId: number, action: string, rating: number | null = null) => {
    const userId = localStorage.getItem("user_id");

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

  const fetchNewRecommendation = async (currentRecommendations: any[]) => {
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
      {/* Main Content */}
      <Container>
        <Paper elevation={3} style={{ padding: "20px", marginTop: "50px", textAlign: "center" }}>
          <Typography variant="h5" color="textPrimary">
            Welcome to your Dashboard {userName}!
          </Typography>
          <Typography variant="body1" color="textSecondary" style={{ marginTop: "10px" }}>
            Here you can interact with meals to improve recommendations.
          </Typography>

          {/* Recommendations Section */}
          <div style={{ marginTop: "30px", textAlign: "left" }}>
            <Typography variant="h6">Your Recommended Meals:</Typography>
            {loading ? (
              <CircularProgress style={{ marginTop: "10px" }} />
            ) : recommendations.length > 0 ? (
              <ul style={{ listStyle: "none", padding: 0 }}>
                {recommendations.map((rec, index) => {
                  // Determine if meal is vegetarian based on diet field
                  const isMealVegetarian = rec.VegNon === 0 || rec.veg_non === false;

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
                          {/* Like Button */}
                          <Button
                            variant="contained"
                            color="primary"
                            size="small"
                            onClick={() => handleInteraction(rec.meal_id, "like")}
                          >
                            👍 Like
                          </Button>

                          {/* Dislike Button */}
                          <Button
                            variant="contained"
                            color="secondary"
                            size="small"
                            style={{ marginLeft: "5px" }}
                            onClick={() => handleInteraction(rec.meal_id, "dislike")}
                          >
                            👎 Dislike
                          </Button>

                          {/* Buy Button */}
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

                      {/* Rating Slider */}
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
        </Paper>
      </Container>
    </div>
  );
};

export default Dashboard;
