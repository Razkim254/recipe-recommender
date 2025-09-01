

# # app.py
# from flask import Flask, request, jsonify
# from flask_mysqldb import MySQL
# from flask_cors import CORS
# from openai import OpenAI
# import os
# import json
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# # Initialize Flask app
# app = Flask(__name__)
# CORS(app)  # Allow CORS for all domains

# # MySQL Configuration
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')  # from .env
# app.config['MYSQL_DB'] = 'recipe_app'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# # Initialize MySQL
# mysql = MySQL(app)

# # Initialize OpenAI client
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# @app.route('/')
# def home():
#     return "✅ Recipe Recommender API is running!"

# @app.route('/recommend', methods=['POST'])
# def recommend():
#     data = request.get_json(silent=True)
#     if not data or 'ingredients' not in data:
#         return jsonify({'error': 'Please provide ingredients as a list or comma-separated string'}), 400

#     raw_ingredients = data['ingredients']
#     if isinstance(raw_ingredients, str):
#         ingredients = [i.strip() for i in raw_ingredients.split(',') if i.strip()]
#     else:
#         ingredients = [str(i).strip() for i in raw_ingredients if str(i).strip()]

#     if not ingredients:
#         return jsonify({'error': 'No valid ingredients provided'}), 400

#     # System prompt to force JSON output
#     system_prompt = (
#         "You are a helpful recipe assistant. Respond ONLY with valid JSON matching exactly:\n"
#         "{ \"recipes\": [ { \"title\": string, \"ingredients\": [string], \"steps\": [string] } ] }\n"
#         "Return exactly 3 recipes. Keep steps concise."
#     )

#     try:
#         ai_response = client.chat.completions.create(
#             model="gpt-4o-mini",  # Updated to a current model
#             messages=[
#                 {"role": "system", "content": system_prompt},
#                 {"role": "user", "content": f"Create 3 simple recipes using: {', '.join(ingredients)}"}
#             ],
#             max_tokens=600,
#             temperature=0.7
#         )

#         content = ai_response.choices[0].message.content.strip()

#         try:
#             payload = json.loads(content)
#         except json.JSONDecodeError:
#             return jsonify({'error': 'Model returned invalid JSON', 'raw': content}), 502

#         if not isinstance(payload, dict) or 'recipes' not in payload or not isinstance(payload['recipes'], list):
#             return jsonify({'error': 'Unexpected JSON shape', 'raw': content}), 502

#         # Save recipes to MySQL
#         try:
#             cur = mysql.connection.cursor()
#             for r in payload['recipes']:
#                 title = r.get('title', '').strip()
#                 ingr = r.get('ingredients', [])
#                 steps = r.get('steps', [])
#                 if not title or not isinstance(ingr, list) or not isinstance(steps, list):
#                     continue
#                 cur.execute(
#                     "INSERT INTO recommendations (title, ingredients, steps) VALUES (%s, %s, %s)",
#                     (title, json.dumps(ingr), json.dumps(steps))
#                 )
#             mysql.connection.commit()
#             cur.close()
#         except Exception as db_err:
#             return jsonify({'error': 'DB save failed', 'details': str(db_err)}), 500

#         return jsonify(payload)

#     except Exception as e:
#         return jsonify({'error': 'OpenAI API call failed', 'details': str(e)}), 500

# @app.route('/recipes', methods=['GET'])
# def list_recipes():
#     try:
#         cur = mysql.connection.cursor()
#         cur.execute("SELECT id, title, ingredients, steps, created_at FROM recommendations ORDER BY created_at DESC LIMIT 10")
#         rows = cur.fetchall()
#         cur.close()

#         formatted = []
#         for row in rows:
#             formatted.append({
#                 'id': row['id'],
#                 'title': row['title'],
#                 'ingredients': json.loads(row['ingredients']) if row['ingredients'] else [],
#                 'steps': json.loads(row['steps']) if row['steps'] else [],
#                 'created_at': row['created_at'].isoformat() if row['created_at'] else None
#             })

#         return jsonify({'recipes': formatted})
#     except Exception as e:
#         return jsonify({'error': 'DB fetch failed', 'details': str(e)}), 500

# if __name__ == '__main__':
#     print("OPENAI_API_KEY set:", bool(os.getenv("OPENAI_API_KEY")))
#     print("MYSQL_PASSWORD set:", bool(os.getenv("MYSQL_PASSWORD")))
#     app.run(debug=True)

from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS
from openai import OpenAI
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file (local dev)
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# --- CORS ---
# In development, allow all origins; in production, restrict to your GitHub Pages URL
frontend_origin = os.getenv("FRONTEND_ORIGIN", "*")  # e.g. "https://yourusername.github.io"
CORS(app, resources={r"/*": {"origins": frontend_origin}})

# --- MySQL Configuration ---
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'recipe_app')
app.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT', 3306))
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Initialize MySQL
mysql = MySQL(app)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/')
def home():
    return "✅ Recipe Recommender API is running!"

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json(silent=True)
    if not data or 'ingredients' not in data:
        return jsonify({'error': 'Please provide ingredients as a list or comma-separated string'}), 400

    raw_ingredients = data['ingredients']
    if isinstance(raw_ingredients, str):
        ingredients = [i.strip() for i in raw_ingredients.split(',') if i.strip()]
    else:
        ingredients = [str(i).strip() for i in raw_ingredients if str(i).strip()]

    if not ingredients:
        return jsonify({'error': 'No valid ingredients provided'}), 400

    # System prompt to force JSON output
    system_prompt = (
        "You are a helpful recipe assistant. Respond ONLY with valid JSON matching exactly:\n"
        "{ \"recipes\": [ { \"title\": string, \"ingredients\": [string], \"steps\": [string] } ] }\n"
        "Return exactly 3 recipes. Keep steps concise."
    )

    try:
        ai_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Create 3 simple recipes using: {', '.join(ingredients)}"}
            ],
            max_tokens=600,
            temperature=0.7
        )

        content = ai_response.choices[0].message.content.strip()

        try:
            payload = json.loads(content)
        except json.JSONDecodeError:
            return jsonify({'error': 'Model returned invalid JSON', 'raw': content}), 502

        if not isinstance(payload, dict) or 'recipes' not in payload or not isinstance(payload['recipes'], list):
            return jsonify({'error': 'Unexpected JSON shape', 'raw': content}), 502

        # Save recipes to MySQL
        try:
            cur = mysql.connection.cursor()
            for r in payload['recipes']:
                title = r.get('title', '').strip()
                ingr = r.get('ingredients', [])
                steps = r.get('steps', [])
                if not title or not isinstance(ingr, list) or not isinstance(steps, list):
                    continue
                cur.execute(
                    "INSERT INTO recommendations (title, ingredients, steps) VALUES (%s, %s, %s)",
                    (title, json.dumps(ingr), json.dumps(steps))
                )
            mysql.connection.commit()
            cur.close()
        except Exception as db_err:
            return jsonify({'error': 'DB save failed', 'details': str(db_err)}), 500

        return jsonify(payload)

    except Exception as e:
        return jsonify({'error': 'OpenAI API call failed', 'details': str(e)}), 500

@app.route('/recipes', methods=['GET'])
def list_recipes():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, title, ingredients, steps, created_at FROM recommendations ORDER BY created_at DESC LIMIT 10")
        rows = cur.fetchall()
        cur.close()

        formatted = []
        for row in rows:
            formatted.append({
                'id': row['id'],
                'title': row['title'],
                'ingredients': json.loads(row['ingredients']) if row['ingredients'] else [],
                'steps': json.loads(row['steps']) if row['steps'] else [],
                'created_at': row['created_at'].isoformat() if row['created_at'] else None
            })

        return jsonify({'recipes': formatted})
    except Exception as e:
        return jsonify({'error': 'DB fetch failed', 'details': str(e)}), 500

if __name__ == '__main__':
    print("OPENAI_API_KEY set:", bool(os.getenv("OPENAI_API_KEY")))
    print("MYSQL_PASSWORD set:", bool(os.getenv("MYSQL_PASSWORD")))
    app.run(debug=True)
