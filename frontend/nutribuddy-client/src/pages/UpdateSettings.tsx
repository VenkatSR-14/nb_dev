import { useState } from "react";
import axios from "axios";
import { Container, TextField, Button, Typography, Paper } from "@mui/material";

const API_BASE_URL = process.env.REACT_APP_API_URL || "http://backend:8000";
const UpdateSettings = () => {
    const [history, setHistory] = useState("");
    const [height, setHeight] = useState("");
    const [weight, setWeight] = useState("");

    const handleUpdate = async(e: React.FormEvent) => {
        e.preventDefault();
        const token = localStorage.getItem("token");

        try {
            await axios.put("http://localhost:8000/api/v1/users/update", {
                history,
                height: Number(height),
                weight: Number(weight),
            }, {
                headers: {Authorization: `Bearer ${token}`}
            });
            alert("Profile updated successfully!");
        } catch(error){
            console.error("Update failed", error);
        }
    };

    return (
        <Container component="main" maxWidth="xs">
            <Paper elevation={3} style={{ padding: "20px", marginTop: "50px" }}>
                <Typography variant="h5" align="center">
                    Update Profile
                </Typography>
                <form onSubmit={handleUpdate}>
                    <TextField fullWidth label="Update History" multiline rows={4} margin="normal" onChange={(e) => setHistory(e.target.value)} required />
                    <TextField fullWidth label="Height (cm)" type="number" margin="normal" onChange={(e) => setHeight(e.target.value)} required />
                    <TextField fullWidth label="Weight (kg)" type="number" margin="normal" onChange={(e) => setWeight(e.target.value)} required />

                    <Button fullWidth type="submit" variant="contained" color="secondary" style={{ marginTop: "10px" }}>
                        Update
                    </Button>
                </form>
            </Paper>
        </Container>
    );
}

export default UpdateSettings;
