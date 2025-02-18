-- Drop Tables in Correct Order to Avoid Dependency Issues
DROP TABLE IF EXISTS recommendations CASCADE;
DROP TABLE IF EXISTS user_activity CASCADE;
DROP TABLE IF EXISTS exercises CASCADE;
DROP TABLE IF EXISTS meals CASCADE;
DROP TABLE IF EXISTS exercise_user_profiles CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Recreate Users Table (Handles authentication & user profile)
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE,
    password_hash TEXT,
    email VARCHAR(255) UNIQUE,
    veg_non BOOLEAN,
    height FLOAT,
    weight FLOAT,
    bmi FLOAT GENERATED ALWAYS AS (weight / ((height / 100) * (height / 100))) STORED,
    nutrient VARCHAR(100),
    disease TEXT,
    diet TEXT
);

-- Recreate Meals Table
CREATE TABLE IF NOT EXISTS meals (
    meal_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(50),
    description TEXT,
    veg_non BOOLEAN,
    nutrient VARCHAR(100),
    disease TEXT,
    diet TEXT,
    price DECIMAL(10,2)
);

-- Recreate Exercises Table
CREATE TABLE IF NOT EXISTS exercises (
    exercise_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    calories_burned FLOAT NOT NULL,
    target_weight FLOAT,
    actual_weight FLOAT,
    age INT,
    gender VARCHAR(10) CHECK (gender IN ('male', 'female')),
    duration INT NOT NULL,
    heart_rate INT,
    bmi FLOAT,
    weather_conditions VARCHAR(50),
    intensity INT CHECK (intensity BETWEEN 1 AND 10)
);

-- Recreate User Activity Table
CREATE TABLE IF NOT EXISTS user_activity (
    activity_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    meal_id INT REFERENCES meals(meal_id) ON DELETE CASCADE,
    exercise_id INT REFERENCES exercises(exercise_id) ON DELETE CASCADE,
    rated BOOLEAN,
    liked BOOLEAN,
    searched BOOLEAN,
    purchased BOOLEAN,
    performed BOOLEAN,
    duration INT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Recreate Recommendations Table
CREATE TABLE IF NOT EXISTS recommendations (
    recommendation_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    meal_id INT REFERENCES meals(meal_id) ON DELETE CASCADE,
    exercise_id INT REFERENCES exercises(exercise_id) ON DELETE CASCADE,
    recommendation_reason TEXT,
    interacted BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Recreate Exercise User Profiles Table
CREATE TABLE IF NOT EXISTS exercise_user_profiles (
    user_id SERIAL PRIMARY KEY REFERENCES users(user_id) ON DELETE CASCADE,
    age INT NOT NULL,
    gender VARCHAR(10) CHECK (gender IN ('Male', 'Female')),
    preferred_intensity INT CHECK (preferred_intensity BETWEEN 1 AND 10),
    fitness_goal VARCHAR(50) NOT NULL,
    preferred_duration INT CHECK (preferred_duration > 0)
);
