USE recipe_app;

-- Insert some users
INSERT INTO users (name) VALUES ('Alice'), ('Bob');

-- Insert sample recipes
INSERT INTO recipes (title, ingredients, instructions, user_id) VALUES
('Tomato Chicken Curry', 'chicken, tomato, onion, garlic', 'Cook chicken with tomatoes...', 1),
('Veggie Rice', 'rice, carrots, peas', 'Boil rice and add vegetables...', 2);
