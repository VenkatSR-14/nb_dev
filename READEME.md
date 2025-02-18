### **🚀 README.md for NutriBuddy Project**
This README provides **setup instructions, project architecture, and usage** for the NutriBuddy application, including **FastAPI, PostgreSQL (Docker), and LLM-powered disease parsing and diet recommendations**.

---

## **📌 NutriBuddy**
**NutriBuddy** is a **health and nutrition recommendation system** that:
- ✅ **Allows users to sign up and update health details.**
- ✅ **Uses PostgreSQL for structured storage.**
- ✅ **Integrates with LLM (GPT-3.5) to extract diseases from medical history.**
- ✅ **Recommends suitable diets based on preprocessed meal data.**
- ✅ **Runs on Docker for easy deployment.**

---

## **📂 Project Structure**
```
nutribuddy/
│── backend/                     # Backend Service (FastAPI)
│   ├── app/
│   │   ├── api/                  # API Endpoints
│   │   │   ├── v1/
│   │   │   │   ├── endpoints/     # API Handlers (Users, LLM, Activities)
│   │   ├── core/                  # Core Services (DB, Security, Config)
│   │   ├── models/                # SQLAlchemy Models
│   │   ├── services/              # Business Logic Services
│   │   ├── main.py                # FastAPI Application Entry Point
│── frontend/                     # React Frontend
│── data/                         # Preprocessed Data (CSV Files)
│── db-scripts/                   # SQL Scripts (Schema & Data)
│── docker-compose.yml            # Docker Config
│── README.md                     # Project Documentation
```

---

## **🚀 Prerequisites**
Before running the project, ensure you have:
- **Python 3.9+**
- **Docker & Docker Compose**
- **Node.js (For Frontend)**
- **PostgreSQL (Dockerized)**

---

## **🛠️ Setup & Installation**
### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/VenkatSR-14/nutribuddy.git
cd nutribuddy
```

### **2️⃣ Set Up Environment Variables**
Create a `.env` file in `backend/app/config/`:
```
DATABASE_URL=postgresql://postgres:Venk@t1998@postgres_db:5432/nutribuddy
OPENAI_API_KEY=your_openai_api_key_here
```

---

## **🐳 Running the Application (Dockerized)**
### **1️⃣ Start PostgreSQL and Backend**
```sh
docker-compose up -d --build
```

### **2️⃣ Apply Database Migrations**
```sh
docker exec -it postgres_db psql -U postgres -d nutribuddy -c "SELECT * FROM users;"
```

### **3️⃣ Run FastAPI Backend**
```sh
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### **4️⃣ Start the Frontend**
```sh
cd frontend
npm install
npm start
```

---

## **🔗 API Endpoints**
| Method | Endpoint | Description |
|--------|---------|-------------|
| **POST** | `/api/v1/users/signup` | User Signup |
| **PUT** | `/api/v1/users/update-user/{user_id}` | Update User Profile |
| **POST** | `/api/v1/llm/parse-disease-history` | Extract Diseases & Recommend Diet |
| **POST** | `/api/v1/activity/update-dashboard/{user_id}` | Log Recent Activity |

---

## **🛠 Tech Stack**
- **Backend:** FastAPI, SQLAlchemy, PostgreSQL, OpenAI GPT-3.5
- **Frontend:** React (Material UI)
- **Database:** PostgreSQL (Dockerized)
- **Infrastructure:** Docker, Docker Compose
- **Deployment:** GitHub, Uvicorn

---

## **🔍 Testing API with cURL**
#### **1️⃣ User Signup**
```sh
curl -X POST "http://127.0.0.1:8000/api/v1/users/signup" \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "password": "securepass", "email": "test@example.com", "veg_non": true, "height": 170, "weight": 70, "disease": "hypertension"}'
```
#### **2️⃣ Disease Parsing & Diet Recommendation**
```sh
curl -X POST "http://127.0.0.1:8000/api/v1/llm/parse-disease-history" \
     -H "Content-Type: application/json" \
     -d '{"history": "The patient has diabetes, hypertension, and kidney disease."}'
```

---

## **✅ Features Implemented**
- **✅ User Signup & Profile Management**
- **✅ LLM Integration (GPT-3.5) for Disease Extraction**
- **✅ Diet Recommendation Based on Preprocessed Data**
- **✅ Dockerized PostgreSQL & FastAPI Backend**
- **✅ React Frontend for User Interaction**
- **✅ Logging Recent Activity on Dashboard Update**

---

## **📝 Next Steps**
- [ ] **Enhance LLM to use embeddings for more accurate disease-diet matching**
- [ ] **Implement JWT Authentication for Secure Login**
- [ ] **Deploy on AWS/GCP using Docker Compose & Nginx**

---

## **💡 Contributors**
- **Aadarsh Gaikwad** 
- **Deepak Udayakumar:**
- **Venkat Srinivasa Raghavan.**

📧 **Contact:** `venkatsr14@example.com`

---

## **🎯 Conclusion**
🚀 **NutriBuddy is now fully functional with FastAPI, PostgreSQL, LLM disease extraction, and personalized diet recommendations!** Let me know if you need **further refinements**! 🔥