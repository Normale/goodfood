-- GoodFood Database Schema
-- PostgreSQL with pgvector extension
-- Migration: 001_initial_schema

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";

-- ============================================================================
-- TABLE: users
-- ============================================================================
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE,
    created_at TIMESTAMPTZ DEFAULT (NOW() AT TIME ZONE 'UTC')
);

-- ============================================================================
-- TABLE: ingredients
-- ============================================================================
CREATE TABLE ingredients (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    description TEXT,
    reasoning TEXT,

    -- Macronutrients
    calories NUMERIC(10, 2),
    carbohydrates NUMERIC(10, 2),
    protein NUMERIC(10, 2),
    total_fats NUMERIC(10, 2),
    alpha_linolenic_acid NUMERIC(10, 2),
    linoleic_acid NUMERIC(10, 2),
    epa_dha NUMERIC(10, 2),
    soluble_fiber NUMERIC(10, 2),
    insoluble_fiber NUMERIC(10, 2),
    water NUMERIC(10, 2),

    -- Vitamins
    vitamin_c NUMERIC(10, 2),
    vitamin_b1_thiamine NUMERIC(10, 2),
    vitamin_b2_riboflavin NUMERIC(10, 2),
    vitamin_b3_niacin NUMERIC(10, 2),
    vitamin_b5_pantothenic_acid NUMERIC(10, 2),
    vitamin_b6_pyridoxine NUMERIC(10, 2),
    vitamin_b7_biotin NUMERIC(10, 2),
    vitamin_b9_folate NUMERIC(10, 2),
    vitamin_b12 NUMERIC(10, 2),
    vitamin_a NUMERIC(10, 2),
    vitamin_d NUMERIC(10, 2),
    vitamin_e NUMERIC(10, 2),
    vitamin_k NUMERIC(10, 2),

    -- Minerals
    calcium NUMERIC(10, 2),
    phosphorus NUMERIC(10, 2),
    magnesium NUMERIC(10, 2),
    potassium NUMERIC(10, 2),
    sodium NUMERIC(10, 2),
    chloride NUMERIC(10, 2),
    iron NUMERIC(10, 2),
    zinc NUMERIC(10, 2),
    copper NUMERIC(10, 2),
    selenium NUMERIC(10, 2),
    manganese NUMERIC(10, 2),
    iodine NUMERIC(10, 2),
    chromium NUMERIC(10, 2),
    molybdenum NUMERIC(10, 2),

    -- Amino Acids
    leucine NUMERIC(10, 2),
    lysine NUMERIC(10, 2),
    valine NUMERIC(10, 2),
    isoleucine NUMERIC(10, 2),
    threonine NUMERIC(10, 2),
    methionine NUMERIC(10, 2),
    phenylalanine NUMERIC(10, 2),
    histidine NUMERIC(10, 2),
    tryptophan NUMERIC(10, 2),

    -- Beneficial Compounds
    choline NUMERIC(10, 2),
    taurine NUMERIC(10, 2),
    coq10 NUMERIC(10, 2),
    alpha_lipoic_acid NUMERIC(10, 2),
    beta_glucan NUMERIC(10, 2),
    resistant_starch NUMERIC(10, 2),

    -- Phytonutrients
    beta_carotene NUMERIC(10, 2),
    lycopene NUMERIC(10, 2),
    lutein NUMERIC(10, 2),
    zeaxanthin NUMERIC(10, 2),
    total_polyphenols NUMERIC(10, 2),
    quercetin NUMERIC(10, 2),
    sulforaphane NUMERIC(10, 2),
    allicin NUMERIC(10, 2),
    curcumin NUMERIC(10, 2),

    updated_at TIMESTAMPTZ DEFAULT (NOW() AT TIME ZONE 'UTC')
);

-- ============================================================================
-- TABLE: user_foods
-- ============================================================================
CREATE TABLE user_foods (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    source TEXT,
    source_key TEXT,

    name TEXT NOT NULL,
    description TEXT,

    -- Macronutrients
    calories NUMERIC(10, 2),
    carbohydrates NUMERIC(10, 2),
    protein NUMERIC(10, 2),
    total_fats NUMERIC(10, 2),
    alpha_linolenic_acid NUMERIC(10, 2),
    linoleic_acid NUMERIC(10, 2),
    epa_dha NUMERIC(10, 2),
    soluble_fiber NUMERIC(10, 2),
    insoluble_fiber NUMERIC(10, 2),
    water NUMERIC(10, 2),

    -- Vitamins
    vitamin_c NUMERIC(10, 2),
    vitamin_b1_thiamine NUMERIC(10, 2),
    vitamin_b2_riboflavin NUMERIC(10, 2),
    vitamin_b3_niacin NUMERIC(10, 2),
    vitamin_b5_pantothenic_acid NUMERIC(10, 2),
    vitamin_b6_pyridoxine NUMERIC(10, 2),
    vitamin_b7_biotin NUMERIC(10, 2),
    vitamin_b9_folate NUMERIC(10, 2),
    vitamin_b12 NUMERIC(10, 2),
    vitamin_a NUMERIC(10, 2),
    vitamin_d NUMERIC(10, 2),
    vitamin_e NUMERIC(10, 2),
    vitamin_k NUMERIC(10, 2),

    -- Minerals
    calcium NUMERIC(10, 2),
    phosphorus NUMERIC(10, 2),
    magnesium NUMERIC(10, 2),
    potassium NUMERIC(10, 2),
    sodium NUMERIC(10, 2),
    chloride NUMERIC(10, 2),
    iron NUMERIC(10, 2),
    zinc NUMERIC(10, 2),
    copper NUMERIC(10, 2),
    selenium NUMERIC(10, 2),
    manganese NUMERIC(10, 2),
    iodine NUMERIC(10, 2),
    chromium NUMERIC(10, 2),
    molybdenum NUMERIC(10, 2),

    -- Amino Acids
    leucine NUMERIC(10, 2),
    lysine NUMERIC(10, 2),
    valine NUMERIC(10, 2),
    isoleucine NUMERIC(10, 2),
    threonine NUMERIC(10, 2),
    methionine NUMERIC(10, 2),
    phenylalanine NUMERIC(10, 2),
    histidine NUMERIC(10, 2),
    tryptophan NUMERIC(10, 2),

    -- Beneficial Compounds
    choline NUMERIC(10, 2),
    taurine NUMERIC(10, 2),
    coq10 NUMERIC(10, 2),
    alpha_lipoic_acid NUMERIC(10, 2),
    beta_glucan NUMERIC(10, 2),
    resistant_starch NUMERIC(10, 2),

    -- Phytonutrients
    beta_carotene NUMERIC(10, 2),
    lycopene NUMERIC(10, 2),
    lutein NUMERIC(10, 2),
    zeaxanthin NUMERIC(10, 2),
    total_polyphenols NUMERIC(10, 2),
    quercetin NUMERIC(10, 2),
    sulforaphane NUMERIC(10, 2),
    allicin NUMERIC(10, 2),
    curcumin NUMERIC(10, 2),

    -- AI vectors
    vector_nutrition VECTOR(60),  -- Normalized nutrition vector for similarity search
    vector_description VECTOR(384),  -- Description embedding (placeholder for future)

    updated_at TIMESTAMPTZ DEFAULT (NOW() AT TIME ZONE 'UTC')
);

-- ============================================================================
-- TABLE: food_logs
-- ============================================================================
CREATE TABLE food_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    user_food_id UUID REFERENCES user_foods(id),
    eaten_at TIMESTAMPTZ DEFAULT (NOW() AT TIME ZONE 'UTC'),
    amount_grams NUMERIC(10, 2),
    meal_type TEXT,
    extra JSONB
);

-- ============================================================================
-- TRIGGER: Auto-generate nutrition vector on insert/update
-- ============================================================================
CREATE OR REPLACE FUNCTION update_nutrition_vector()
RETURNS TRIGGER AS $$
DECLARE
    nutrient_values NUMERIC[];
    norm_factor NUMERIC;
BEGIN
    -- Collect all 60 nutrient values into an array
    nutrient_values := ARRAY[
        COALESCE(NEW.carbohydrates, 0),
        COALESCE(NEW.protein, 0),
        COALESCE(NEW.total_fats, 0),
        COALESCE(NEW.alpha_linolenic_acid, 0),
        COALESCE(NEW.linoleic_acid, 0),
        COALESCE(NEW.epa_dha, 0),
        COALESCE(NEW.soluble_fiber, 0),
        COALESCE(NEW.insoluble_fiber, 0),
        COALESCE(NEW.water, 0),
        COALESCE(NEW.vitamin_c, 0),
        COALESCE(NEW.vitamin_b1_thiamine, 0),
        COALESCE(NEW.vitamin_b2_riboflavin, 0),
        COALESCE(NEW.vitamin_b3_niacin, 0),
        COALESCE(NEW.vitamin_b5_pantothenic_acid, 0),
        COALESCE(NEW.vitamin_b6_pyridoxine, 0),
        COALESCE(NEW.vitamin_b7_biotin, 0),
        COALESCE(NEW.vitamin_b9_folate, 0),
        COALESCE(NEW.vitamin_b12, 0),
        COALESCE(NEW.vitamin_a, 0),
        COALESCE(NEW.vitamin_d, 0),
        COALESCE(NEW.vitamin_e, 0),
        COALESCE(NEW.vitamin_k, 0),
        COALESCE(NEW.calcium, 0),
        COALESCE(NEW.phosphorus, 0),
        COALESCE(NEW.magnesium, 0),
        COALESCE(NEW.potassium, 0),
        COALESCE(NEW.sodium, 0),
        COALESCE(NEW.chloride, 0),
        COALESCE(NEW.iron, 0),
        COALESCE(NEW.zinc, 0),
        COALESCE(NEW.copper, 0),
        COALESCE(NEW.selenium, 0),
        COALESCE(NEW.manganese, 0),
        COALESCE(NEW.iodine, 0),
        COALESCE(NEW.chromium, 0),
        COALESCE(NEW.molybdenum, 0),
        COALESCE(NEW.leucine, 0),
        COALESCE(NEW.lysine, 0),
        COALESCE(NEW.valine, 0),
        COALESCE(NEW.isoleucine, 0),
        COALESCE(NEW.threonine, 0),
        COALESCE(NEW.methionine, 0),
        COALESCE(NEW.phenylalanine, 0),
        COALESCE(NEW.histidine, 0),
        COALESCE(NEW.tryptophan, 0),
        COALESCE(NEW.choline, 0),
        COALESCE(NEW.taurine, 0),
        COALESCE(NEW.coq10, 0),
        COALESCE(NEW.alpha_lipoic_acid, 0),
        COALESCE(NEW.beta_glucan, 0),
        COALESCE(NEW.resistant_starch, 0),
        COALESCE(NEW.beta_carotene, 0),
        COALESCE(NEW.lycopene, 0),
        COALESCE(NEW.lutein, 0),
        COALESCE(NEW.zeaxanthin, 0),
        COALESCE(NEW.total_polyphenols, 0),
        COALESCE(NEW.quercetin, 0),
        COALESCE(NEW.sulforaphane, 0),
        COALESCE(NEW.allicin, 0),
        COALESCE(NEW.curcumin, 0)
    ];

    -- Normalize by calories (avoid division by zero)
    IF NEW.calories IS NOT NULL AND NEW.calories > 0 THEN
        norm_factor := NEW.calories;
    ELSE
        norm_factor := 1.0;
    END IF;

    -- Create normalized vector (divide each element by calories)
    -- Format: [val1,val2,val3,...] for pgvector
    NEW.vector_nutrition := (
        SELECT '[' || array_to_string(
            ARRAY(
                SELECT (val / norm_factor)::TEXT
                FROM unnest(nutrient_values) AS val
            ),
            ','
        ) || ']'
    )::VECTOR(60);

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Attach trigger to user_foods table
CREATE TRIGGER user_foods_nutrition_vector_trigger
BEFORE INSERT OR UPDATE ON user_foods
FOR EACH ROW
EXECUTE FUNCTION update_nutrition_vector();

-- ============================================================================
-- INDEXES
-- ============================================================================

-- Standard B-tree indexes for lookups
CREATE INDEX idx_ingredients_name ON ingredients(name);
CREATE INDEX idx_user_foods_user_id ON user_foods(user_id);
CREATE INDEX idx_user_foods_source ON user_foods(source, source_key);
CREATE INDEX idx_food_logs_user_id ON food_logs(user_id);
CREATE INDEX idx_food_logs_user_food_id ON food_logs(user_food_id);
CREATE INDEX idx_food_logs_eaten_at ON food_logs(eaten_at);
CREATE INDEX idx_food_logs_meal_type ON food_logs(meal_type);

-- HNSW indexes for vector similarity search
-- Nutrition vector: exact nearest neighbors (using L2 distance)
CREATE INDEX idx_user_foods_nutrition_vector ON user_foods
USING hnsw (vector_nutrition vector_l2_ops)
WITH (m = 16, ef_construction = 64);

-- Description vector: approximate nearest neighbors (using cosine distance)
-- Note: This index is created for future use when embeddings are implemented
CREATE INDEX idx_user_foods_description_vector ON user_foods
USING hnsw (vector_description vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- ============================================================================
-- INITIAL DATA: Default user
-- ============================================================================
INSERT INTO users (id, username, email, created_at)
VALUES (
    '00000000-0000-0000-0000-000000000000',
    'default_user',
    'default@goodfood.local',
    NOW() AT TIME ZONE 'UTC'
)
ON CONFLICT (username) DO NOTHING;
