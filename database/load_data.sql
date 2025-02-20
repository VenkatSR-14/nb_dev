-- Load User Profiles, setting missing fields to NULL
COPY users(user_id, veg_non, nutrient, disease, diet)
FROM '/docker-entrypoint-initdb.d/data/cleaned/cleaned_user_profiles.csv'
DELIMITER ',' CSV HEADER;

-- Update NULL fields explicitly (excluding BMI)
UPDATE users
SET username = NULL, 
    password_hash = NULL,
    email = NULL,
    height = NULL,
    weight = NULL
WHERE username IS NULL;

-- Load Meals Data (Fixing category name)
COPY meals(meal_id, name, category, description, veg_non, nutrient, disease, diet, price)
FROM '/docker-entrypoint-initdb.d/data/cleaned/cleaned_meals.csv'
DELIMITER ',' CSV HEADER;

-- Load Exercises Data
COPY exercises(exercise_id, name, calories_burned, target_weight, actual_weight, age, gender, duration, heart_rate, bmi, weather_conditions, intensity)
FROM '/docker-entrypoint-initdb.d/data/cleaned/cleaned_exercise.csv'
DELIMITER ',' CSV HEADER;

-- Load User Activity (Meals)
COPY user_activity(user_id, meal_id, rated, liked, searched, purchased, timestamp)
FROM '/docker-entrypoint-initdb.d/data/cleaned/cleaned_recent_activity.csv'
DELIMITER ',' CSV HEADER;

-- Load User Activity (Exercises)
COPY user_activity(user_id, exercise_id, rated, liked, performed, duration, timestamp)
FROM '/docker-entrypoint-initdb.d/data/cleaned/cleaned_exercise_activity.csv'
DELIMITER ',' CSV HEADER;

-- Load Exercise User Profiles
COPY exercise_user_profiles(user_id, age, gender, preferred_intensity, fitness_goal, preferred_duration)
FROM '/docker-entrypoint-initdb.d/data/cleaned/cleaned_exercise_user_profiles.csv'
DELIMITER ',' CSV HEADER;

SELECT setval('users_user_id_seq', COALESCE((SELECT MAX(user_id) + 1 FROM users), 1), FALSE);