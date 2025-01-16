from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os


app = Flask(__name__)
CORS(app,origins = ["https://adhavan2024.netlify.app"])  # Enable CORS for frontend-backend communication

# MongoDB Connection
MONGO_URL = "mongodb://localhost:27017"
client = MongoClient(MONGO_URL)
db = client['Project']  # Replace with your database name
users_collection = db['validation']  # Replace with your collection name


@app.route("/api/signup", methods=["POST"])  
def signup():
    try:
        # Parse the request body
        data = request.json
        email = data.get('email')
        password = data.get('password')

        # Validation
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400

        # Check if the email already exists
        if users_collection.find_one({'email': email}):
            return jsonify({'error': 'Email already exists'}), 400

        # Hash the password
        # hashed_password = generate_password_hash(password)

        # Save user to MongoDB
        user = {'email': email, 'password': password}
        users_collection.insert_one(user)

        return jsonify({'message': 'User registered successfully'}), 201

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal server error'}), 500


# if __name__ == '__main__':
#     app.run(debug=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use Render's assigned port (default 5000 for local)
    app.run(debug=True, host='0.0.0.0', port=port)


# ----------------------------------------------------------------------------#

#-----------This is for Login purpose ----------------------------------------#


@app.route("/login", methods=["POST"]) # login", methods=["POST"]
def login():
    # Parse request data
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # Find user in MongoDB
    user = users_collection.find_one({"email": email})
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Validate password
    if user["password"] == password:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid password"}), 401
