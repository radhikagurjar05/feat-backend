from flask import Blueprint, request, jsonify
import sqlite3
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
 
print("Auth FILE LOADED")
auth = Blueprint("auth", __name__)
bcrypt = Bcrypt()

def get_db():
    return sqlite3.connect("database.db")

@auth.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    db = get_db()
    cursor = db.cursor()

    # ✅ DEBUG
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    print("ALL USERS:", users)

    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    user = cursor.fetchone()
    print("FOUND USER:", user)

    if user:
        stored_password = user[3]  # ✅ correct index
        print("STORED HASH:", stored_password)

        if bcrypt.check_password_hash(stored_password, password):
            print("PASSWORD MATCH ✅")
            return jsonify({"message": "Login successful"})
        else:
            print("PASSWORD WRONG ❌")
            return jsonify({"message": "Invalid credentials"})
    else:
        print("USER NOT FOUND ❌")
        return jsonify({"message": "User not found"})