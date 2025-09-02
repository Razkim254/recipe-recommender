AI-Powered Recipe Recommender

A full-stack web app that recommends recipes based on ingredients you provide. Powered by OpenAI, backed by SQL scripts, and built with Flask and vanilla JS. Designed for clean deployment, modularity, and intuitive UX.

📁 Project Structure
Code
RECIPES/
├── backend/
│   ├── app.py
│   ├── openai_helpers.py
│   ├── .env
│   ├── requirements.txt
│   └── __pycache__/
├── database/
│   ├── create_db.sql
│   ├── insert_sample.sql
│   └── test_queries.sql
├── frontend/
│   └── index.html
└── .gitignore
🚀 Features
🧠 AI-generated recipe suggestions via OpenAI

🗃️ SQL scripts for database setup and testing

🔐 Secure API key handling via .env

🎨 Responsive, minimal frontend

🌍 Live deployment via Render & GitHub Pages

🧱 Modular structure for easy maintenance

🛠️ Getting Started
1. Clone the Repo
bash
git clone https://github.com/your-username/recipe-recommender.git
cd recipe-recommender
2. Backend Setup
bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
Create a .env file:

env
OPENAI_API_KEY=your_openai_key_here
Run the server:

bash
python app.py
3. Frontend Setup
Open frontend/index.html in your browser. Update fetch URLs to match your backend (local or Render).

🧪 Database Setup
Navigate to the database/ folder and run:

sql
-- create_db.sql
CREATE TABLE ingredients (...);
CREATE TABLE recipes (...);

-- insert_sample.sql
INSERT INTO ingredients VALUES (...);
INSERT INTO recipes VALUES (...);

-- test_queries.sql
SELECT * FROM recipes WHERE ...;
Use a local SQLite or MySQL instance depending on your backend config.

🌐 Deployment
Backend (Render)
Push to GitHub

Create a new web service on Render

Set environment variable OPENAI_API_KEY

Use app.py as entry point

Frontend (GitHub Pages)
Push frontend/ to a gh-pages branch

Enable GitHub Pages in repo settings

Update fetch URLs in index.html to point to your Render backend

📦 API Reference
POST /recommend
Request:

json
{
  "ingredients": ["egg", "tomato", "cheese"]
}
Response:

json
{
  "recipe": "Try making a tomato and cheese omelette..."
}
📌 Roadmap
[ ] Add dietary filters (vegan, gluten-free, etc.)

[ ] Improve error handling and loading states

[ ] Connect database to backend for persistent storage

[ ] Add user authentication for saved preferences

🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

To contribute:
Fork the repo

Create your feature branch (git checkout -b feature/awesome-feature)

Commit your changes (git commit -m 'Add awesome feature')

Push to the branch (git push origin feature/awesome-feature)

Open a pull request

📄 License
This project is licensed under the MIT License. See the LICENSE file for details.

🙌 Acknowledgments
Built by raz with curiosity, clean code, and a love for good food.
