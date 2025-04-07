import { useState } from "react";
import axios from "axios";
import { Container, TextField, Button, Typography, Paper, CircularProgress } from "@mui/material";

const API_BASE_URL = process.env.REACT_APP_API_URL || "http://backend:8000";

const UpdateSettings = () => {
    const [history, setHistory] = useState("");
    const [height, setHeight] = useState("");
    const [weight, setWeight] = useState("");
    const [loading, setLoading] = useState(false);

    const handleUpdate = async(e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        const token = localStorage.getItem("token");
        const userId = localStorage.getItem("user_id");
        
        try {
            // First, update user profile
            await axios.put(`${API_BASE_URL}/api/v1/users/update-user/${userId}`, {
                disease: history,
                height: Number(height),
                weight: Number(weight),
            }, {
                headers: {Authorization: `Bearer ${token}`}
            });
            
            // Store updated height and weight in localStorage for use in other components
            localStorage.setItem("userHeight", height);
            localStorage.setItem("userWeight", weight);
            
            // Refresh recommendations after profile update
            await axios.post(`${API_BASE_URL}/api/v1/recommender/refresh-recommendations/${userId}`);
            
            alert("Profile updated successfully and recommendations refreshed!");
        } catch(error){
            console.error("Update failed", error);
            alert("Failed to update profile. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <Container component="main" maxWidth="xs">
            <Paper elevation={3} style={{ padding: "20px", marginTop: "50px" }}>
                <Typography variant="h5" align="center">
                    Update Profile
                </Typography>
                <form onSubmit={handleUpdate}>
                    <TextField 
                        fullWidth 
                        label="Medical History" 
                        multiline 
                        rows={4} 
                        margin="normal" 
                        value={history}
                        onChange={(e) => setHistory(e.target.value)} 
                        required 
                        helperText="Enter your medical conditions, allergies, or dietary restrictions"
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
                        color="secondary" 
                        style={{ marginTop: "10px" }}
                        disabled={loading}
                    >
                        {loading ? <CircularProgress size={24} color="inherit" /> : "Update Profile"}
                    </Button>
                </form>
            </Paper>
        </Container>
    );
}

export default UpdateSettings;
