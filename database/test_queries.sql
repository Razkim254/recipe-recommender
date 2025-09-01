-- Join users and recipes to show who added what
SELECT users.name AS added_by, recipes.title
FROM recipes
JOIN users ON recipes.user_id = users.id;
