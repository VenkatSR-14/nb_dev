### 📦 NutriBuddy - Setup & Installation Guide

This repository contains the **NutriBuddy** application, a full-stack personalized diet and exercise recommendation system using FastAPI, PostgreSQL, and React.

---

## 📈 Project Description & Purpose

**NutriBuddy** is a **health and nutrition recommendation system** that:

- ✅ **Allows users to sign up and update health details.**
- ✅ **Uses PostgreSQL for structured storage.**
- ✅ **Integrates with LLM (GPT-3.5) to extract diseases from medical history.**
- ✅ **Recommends suitable diets based on preprocessed meal data.**
- ✅ **Runs on Docker for easy deployment.**
- ✅ **Includes a React-based frontend for user interaction.**

---

## 📊 Dataset Details & Link

We use a preprocessed **Fitness Recommender Dataset** that includes nutritional data, exercise details, and disease-related dietary requirements.

You can access the dataset here: [Fitness Recommender Dataset](https://www.kaggle.com/datasets/venkyy123/fitness-recommender-dataset/data)

---

## 📂 Project Structure

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
│   ├── src/
│   │   ├── components/            # UI Components
│   │   ├── pages/                 # Page Components
│   │   ├── api/                   # API Calls
│   ├── public/
│   ├── package.json               # Frontend Dependencies
│── data/                         # Preprocessed Data (CSV Files)
│── db-scripts/                   # SQL Scripts (Schema & Data)
│── docker-compose.yml            # Docker Config
│── README.md                     # Project Documentation
```

---

## 🚀 Installation

### 1️⃣ Clone the Repository

```sh
git clone https://github.com/VenkatSR-14/nutribuddy.git
cd nutribuddy
```

### 2️⃣ Create and Activate Virtual Environment

```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

### 3️⃣ Install Dependencies

```sh
pip install -r requirements.txt
```

For frontend dependencies:

```sh
cd frontend
npm install
```

### 4️⃣ Set Up Environment Variables

Create a `.env` file in `backend/app/config/`:

```sh
touch .env
```

Add the following environment variables (update values accordingly):

```ini
DATABASE_URL=postgresql://postgres:Venk@t1998@postgres_db:5432/nutribuddy
OPENAI_API_KEY=your_openai_api_key_here
```

---

## 🛠️ Running the Application (Dockerized)

### 1️⃣ Start PostgreSQL, Backend, and Frontend

```sh
docker-compose up -d --build
```

### 2️⃣ Apply Database Migrations

```sh
docker exec -it postgres_db psql -U postgres -d nutribuddy -c "SELECT * FROM users;"
```

### 3️⃣ Run FastAPI Backend

```sh
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4️⃣ Start the Frontend

```sh
cd frontend
npm start
```

---

## 📞 API Endpoints

| Method   | Endpoint                                     | Description                       |
| -------- | -------------------------------------------- | --------------------------------- |
| **POST** | /api/v1/users/signup                         | User Signup                       |
| **PUT**  | /api/v1/users/update-user/{user\_id}         | Update User Profile               |
| **POST** | /api/v1/llm/parse-disease-history            | Extract Diseases & Recommend Diet |
| **POST** | /api/v1/activity/update-dashboard/{user\_id} | Log Recent Activity               |

For more details, check the API documentation at:

```sh
http://localhost:8000/docs
```

---

## 🛠️ Tech Stack

- **Backend:** FastAPI, SQLAlchemy, PostgreSQL, OpenAI GPT-3.5
- **Frontend:** React (Material UI)
- **Database:** PostgreSQL (Dockerized)
- **Infrastructure:** Docker, Docker Compose
- **Deployment:** GitHub, Uvicorn

---

## 📊 Testing API with cURL

#### 1️⃣ User Signup

```sh
curl -X POST "http://127.0.0.1:8000/api/v1/users/signup" \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "password": "securepass", "email": "test@example.com", "veg_non": true, "height": 170, "weight": 70, "disease": "hypertension"}'
```

#### 2️⃣ Disease Parsing & Diet Recommendation

```sh
curl -X POST "http://127.0.0.1:8000/api/v1/llm/parse-disease-history" \
     -H "Content-Type: application/json" \
     -d '{"history": "The patient has diabetes, hypertension, and kidney disease."}'
```

---

## ✅ Features Implemented

- **✅ User Signup & Profile Management**
- **✅ LLM Integration (GPT-3.5) for Disease Extraction**
- **✅ Diet Recommendation Based on Preprocessed Data**
- **✅ Dockerized PostgreSQL & FastAPI Backend**
- **✅ React Frontend for User Interaction**
- **✅ Logging Recent Activity on Dashboard Update**

---

## 📝 Next Steps

- [ ] **Enhance LLM to use embeddings for more accurate disease-diet matching**
- [ ] **Implement JWT Authentication for Secure Login**
- [ ] **Deploy on AWS/GCP using Docker Compose & Nginx**

---

## 💡 Contributors

- **Aadarsh Gaikwad**
- **Deepak Udayakumar**
- **Venkat Srinivasa Raghavan**

💎 **Contact:** [venkatsr14@example.com](mailto:venkatsr14@example.com)

---

## 🎯 Conclusion

🚀 **NutriBuddy is now fully functional with FastAPI, PostgreSQL, LLM disease extraction, and personalized diet recommendations!** Let me know if you need **further refinements**! 🔥

