import axios from "axios";
import { useState } from "react";


const UpdateSettings = () => {
    const [history, setHistory] = useState("");
    const [height, setHeight] = useState("");
    const [weight, setWeight] = useState("");

    const handleUpdate = async(e: React.FormEvent) => {
        e.preventDefault();
        const token = localStorage.getItem("token");

        try{
            await axios.put("http://localhost:8000/auth/update", {
                history,
                height: Number(height),
                weight: Number(weight),
            }, {
                headers: {Authorization:"Bearer ${token}"}
            });
            alert("Profile updated successfully!");
        } catch(error){
            console.error("Update failed", error);
        }
    };

    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-100">
          <form onSubmit={handleUpdate} className="p-6 shadow-lg rounded-lg bg-white w-96">
            <h2 className="text-xl font-bold mb-4">Update Profile</h2>
            <textarea placeholder="Update history" className="p-2 border rounded mb-2 w-full"
              onChange={(e) => setHistory(e.target.value)} required />
            <input type="number" placeholder="Height (cm)" className="p-2 border rounded mb-2 w-full"
              onChange={(e) => setHeight(e.target.value)} required />
            <input type="number" placeholder="Weight (kg)" className="p-2 border rounded mb-2 w-full"
              onChange={(e) => setWeight(e.target.value)} required />
            <button type="submit" className="p-2 bg-yellow-500 text-white rounded w-full">Update</button>
          </form>
        </div>
      );
}

export default UpdateSettings;

