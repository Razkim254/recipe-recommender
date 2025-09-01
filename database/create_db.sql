-- Create database
CREATE DATABASE IF NOT EXISTS recipe_app;
USE recipe_app;

-- Users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Recipes table
CREATE TABLE recipes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    ingredients TEXT,
    instructions TEXT,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
