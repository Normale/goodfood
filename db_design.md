For now, the database is designed to handle small number of users and their foods.


There are 3 tables:
- ingredients - this works as a "cache" for commonly used ingredients, e.g. "carrot", "salt"
- user_foods - this is the user's copy / version of a certain food. Can be user-created, edited from the external database or just copied. This table will be used in recommendation to look-up the dishes known to user.
- food_log - this table is just a log of foods eaten by the user at given time. Will be used to analyze by summing over the dishes in certain time period.


Table specifics:
CREATE TABLE ingredients (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    description TEXT,

    -- Nutrients as explicit columns
    calories NUMERIC,
    protein NUMERIC,
    fat NUMERIC,
    -- others (total of 60 right now)


    updated_at TIMESTAMP DEFAULT NOW()
);


CREATE TABLE user_foods (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    source TEXT  -- nullable reference to source
    source_key TEXT -- nullable reference to a key in source 

    name TEXT,
    description TEXT,

    -- Nutrients as explicit columns
    calories NUMERIC,
    protein NUMERIC,
    fat NUMERIC,
    -- others (total of 60 right now)

    -- AI vectors
    vector_nutrition VECTOR(60), -- normalized vector used for finding foods similar to needs
    vector_description VECTOR(384), -- embedding vector used for matching foods based on description

    updated_at TIMESTAMP DEFAULT NOW()
);


CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE,
    created_at TIMESTAMP DEFAULT NOW()
);


CREATE TABLE food_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    user_food_id UUID REFERENCES user_foods(id), -- any food logged HAS TO be in user_foods. If the food is not present in user_foods table, it should be added there before adding to the
    eaten_at TIMESTAMP DEFAULT NOW(),
    amount_grams NUMERIC,
    meal_type TEXT,  -- breakfast, lunch, etc.
    extra JSONB -- extra info about the food logged
);



# The python integration
The database in use should be postgres with pgvector extension. The application concisely integrates with the asynchronous fastapi and pydantic models using tortoise. Vectors should be automatically created by the postgres on insert, by taking nutritional values and normalizing them by calories. 
The vectors will be searched by 
 - nutritional vector - exact nearest neighbours
 - HNSW indexes for embeddings - approx. to speed things up.