import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { Container, Paper, Typography, CircularProgress } from "@mui/material";
import Navbar from "../components/Navbar";
import { isAuthenticated } from "../utils/auth";  // ✅ Import authentication check

const Dashboard = () => {
  const navigate = useNavigate();
  const [recommendations, setRecommendations] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const API_BASE_URL = process.env.REACT_APP_API_URL || "http://backend:8000";

  // ✅ If not authenticated, redirect to login
  useEffect(() => {
    if (!isAuthenticated()) {
      navigate("/");
    }
  }, [navigate]);

  useEffect(() => {
    const fetchRecommendations = async () => {
      const userId = localStorage.getItem("user_id");

      if (!userId || userId === "undefined") {  // ✅ Check for undefined user_id
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

    fetchRecommendations();
  }, []);

  return (
    <div style={{ backgroundColor: "#f5f5f5", minHeight: "100vh" }}>
      <Navbar />  {/* ✅ Use the shared Navbar */}

      {/* Main Content */}
      <Container>
        <Paper elevation={3} style={{ padding: "20px", marginTop: "50px", textAlign: "center" }}>
          <Typography variant="h5" color="textPrimary">
            Welcome to your Dashboard!
          </Typography>
          <Typography variant="body1" color="textSecondary" style={{ marginTop: "10px" }}>
            Here you can update your settings and manage your account.
          </Typography>

          {/* Recommendations Section */}
          <div style={{ marginTop: "30px", textAlign: "left" }}>
            <Typography variant="h6">Your Recommendations:</Typography>
            {loading ? (
              <CircularProgress style={{ marginTop: "10px" }} />
            ) : recommendations.length > 0 ? (
              <ul>
                {recommendations.map((rec, index) => (
                  <li key={index}>{rec.name}</li>
                ))}
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
