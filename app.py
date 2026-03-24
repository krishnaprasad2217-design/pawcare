from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json, os, hashlib, webbrowser, threading
from datetime import datetime, date
from pet_data import get_pet_info
from drpet import DrPetChatbot

app = Flask(__name__, template_folder=".")
app.secret_key = "petcare_secret_2024"

DB_FILE = "data/users.json"

# ------------------ DATABASE ------------------

def load_users():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE) as f:
        try:
            return json.load(f)
        except:
            return {}

def save_users(users):
    with open(DB_FILE, "w") as f:
        json.dump(users, f, indent=2)

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

# ------------------ ROUTES ------------------

@app.route("/")
def index():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return render_template("index.html")

# ------------------ SIGNUP ------------------

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        data = request.form
        users = load_users()

        email = data["email"].lower().strip()

        if email in users:
            return render_template("signup.html", error="Email already registered.")

        users[email] = {
            "name": data["parent_name"],
            "email": email,
            "password": hash_pw(data["password"]),
            "pet_name": data["pet_name"],
            "breed": data["breed"],
            "color": data["color"],
            "pet_type": data["pet_type"],
            "pet_dob": data["pet_dob"],
            "location": data.get("location", ""),
            "joined": str(date.today()),
            "profile_photo": "",
            "vaccination_status": {},
            "diet_notes": {},
            "pets": []
        }

        save_users(users)
        session["user"] = email
        return redirect(url_for("dashboard"))

    return render_template("signup.html")

# ------------------ LOGIN ------------------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].lower().strip()
        password = request.form["password"]

        users = load_users()
        user = users.get(email)

        if user and user["password"] == hash_pw(password):
            session["user"] = email
            return redirect(url_for("dashboard"))

        return render_template("login.html", error="Invalid email or password.")

    return render_template("login.html")

# ------------------ LOGOUT ------------------

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

# ------------------ DASHBOARD (FIXED) ------------------

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    users = load_users()
    email = session["user"]

    # ✅ FIX: prevent KeyError
    if email not in users:
        session.clear()
        return redirect(url_for("login"))

    user = users[email]
    pet_info = get_pet_info(user["breed"], user["pet_type"], user["pet_dob"])

    return render_template("dashboard.html", user=user, pet=pet_info)

# ------------------ API ROUTES ------------------

@app.route("/api/pet-info")
def api_pet_info():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    users = load_users()
    email = session["user"]

    if email not in users:
        session.clear()
        return jsonify({"error": "Session expired"}), 401

    user = users[email]
    pet_info = get_pet_info(user["breed"], user["pet_type"], user["pet_dob"])

    return jsonify(pet_info)

@app.route("/api/pets", methods=["GET"])
def get_pets():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    users = load_users()
    email = session["user"]

    if email not in users:
        session.clear()
        return jsonify({"error": "Session expired"}), 401

    pets = users[email].get("pets", [])
    return jsonify({"pets": pets})

@app.route("/api/pets/add", methods=["POST"])
def add_pet():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    users = load_users()
    email = session["user"]

    if email not in users:
        session.clear()
        return jsonify({"error": "Session expired"}), 401

    data = request.get_json()

    pet_name = data.get("pet_name", "").strip()
    breed = data.get("breed", "").strip()
    pet_type = data.get("pet_type", "dog").strip()
    pet_dob = data.get("pet_dob", "").strip()
    photo = data.get("photo", "")

    if not pet_name or not breed:
        return jsonify({"error": "Pet name and breed required"}), 400

    new_pet = {
        "id": str(int(datetime.now().timestamp() * 1000)),
        "pet_name": pet_name,
        "breed": breed,
        "pet_type": pet_type,
        "pet_dob": pet_dob,
        "photo": photo,
        "added": str(date.today())
    }

    users[email].setdefault("pets", []).append(new_pet)
    save_users(users)

    return jsonify({"success": True, "pet": new_pet})

@app.route("/api/pets/delete/<pet_id>", methods=["DELETE"])
def delete_pet(pet_id):
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    users = load_users()
    email = session["user"]

    if email not in users:
        session.clear()
        return jsonify({"error": "Session expired"}), 401

    users[email]["pets"] = [
        p for p in users[email].get("pets", [])
        if p["id"] != pet_id
    ]

    save_users(users)
    return jsonify({"success": True})

@app.route("/api/account/delete", methods=["DELETE"])
def delete_account():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    users = load_users()
    email = session["user"]

    if email in users:
        del users[email]
        save_users(users)

    session.clear()
    return jsonify({"success": True})

# ------------------ VACCINATION STATUS ------------------

@app.route("/api/vaccination-status", methods=["GET"])
def get_vaccination_status():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    users = load_users()
    email = session["user"]
    if email not in users:
        return jsonify({"error": "Session expired"}), 401
    status = users[email].get("vaccination_status", {})
    return jsonify({"status": status})

@app.route("/api/vaccination-status", methods=["POST"])
def save_vaccination_status():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    users = load_users()
    email = session["user"]
    if email not in users:
        return jsonify({"error": "Session expired"}), 401
    data = request.get_json()
    users[email]["vaccination_status"] = data.get("status", {})
    save_users(users)
    return jsonify({"success": True})

# ------------------ DIET NOTES (meals, water, nutrition, health records) ------------------

@app.route("/api/diet-notes", methods=["GET"])
def get_diet_notes():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    users = load_users()
    email = session["user"]
    if email not in users:
        return jsonify({"error": "Session expired"}), 401
    notes = users[email].get("diet_notes", {})
    return jsonify({"notes": notes})

@app.route("/api/diet-notes", methods=["POST"])
def save_diet_notes():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    users = load_users()
    email = session["user"]
    if email not in users:
        return jsonify({"error": "Session expired"}), 401
    data = request.get_json()
    users[email]["diet_notes"] = data.get("notes", {})
    save_users(users)
    return jsonify({"success": True})

# ------------------ PROFILE PHOTO ------------------

@app.route("/api/profile-photo", methods=["POST"])
def save_profile_photo():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    users = load_users()
    email = session["user"]
    if email not in users:
        return jsonify({"error": "Session expired"}), 401
    data = request.get_json()
    photo = data.get("photo", "")
    # Limit photo size to avoid bloating users.json (max ~2MB base64)
    if len(photo) > 2 * 1024 * 1024:
        return jsonify({"error": "Photo too large. Please use a smaller image."}), 400
    users[email]["profile_photo"] = photo
    save_users(users)
    return jsonify({"success": True})

# ------------------ FORGOT PASSWORD ------------------

@app.route("/forgot-password")
def forgot_password():
    return render_template("forgot_password.html")

@app.route("/api/reset/check-email", methods=["POST"])
def reset_check_email():
    data = request.get_json()
    email = data.get("email", "").lower().strip()
    users = load_users()
    return jsonify({"exists": email in users})

@app.route("/api/reset/verify", methods=["POST"])
def reset_verify():
    data = request.get_json()
    email = data.get("email", "").lower().strip()
    pet_name = data.get("pet_name", "").strip().lower()
    pet_dob = data.get("pet_dob", "").strip()
    users = load_users()
    user = users.get(email)
    if not user:
        return jsonify({"verified": False})
    name_match = user.get("pet_name", "").lower() == pet_name
    dob_match = user.get("pet_dob", "") == pet_dob
    return jsonify({"verified": name_match and dob_match})

@app.route("/api/reset/save", methods=["POST"])
def reset_save():
    data = request.get_json()
    email = data.get("email", "").lower().strip()
    password = data.get("password", "")
    if len(password) < 6:
        return jsonify({"success": False, "error": "Password too short"}), 400
    users = load_users()
    if email not in users:
        return jsonify({"success": False, "error": "Account not found"}), 404
    users[email]["password"] = hash_pw(password)
    save_users(users)
    return jsonify({"success": True})

# ------------------ PET GALLERY ------------------

@app.route("/api/gallery", methods=["GET"])
def get_gallery():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    users = load_users()
    email = session["user"]
    if email not in users:
        return jsonify({"error": "Session expired"}), 401
    gallery = users[email].get("gallery", [])
    return jsonify({"gallery": gallery})

@app.route("/api/gallery/add", methods=["POST"])
def add_gallery_photo():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    users = load_users()
    email = session["user"]
    if email not in users:
        return jsonify({"error": "Session expired"}), 401
    data = request.get_json()
    photo = data.get("photo", "")
    caption = data.get("caption", "").strip()[:120]
    tag = data.get("tag", "").strip()
    if not photo:
        return jsonify({"error": "No photo provided"}), 400
    if len(photo) > 2 * 1024 * 1024:
        return jsonify({"error": "Photo too large. Please use an image under 2MB."}), 400
    entry = {
        "id": str(int(datetime.now().timestamp() * 1000)),
        "photo": photo,
        "caption": caption,
        "tag": tag,
        "date": str(date.today())
    }
    users[email].setdefault("gallery", []).insert(0, entry)
    save_users(users)
    return jsonify({"success": True, "entry": entry})

@app.route("/api/gallery/delete/<photo_id>", methods=["DELETE"])
def delete_gallery_photo(photo_id):
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    users = load_users()
    email = session["user"]
    if email not in users:
        return jsonify({"error": "Session expired"}), 401
    users[email]["gallery"] = [
        p for p in users[email].get("gallery", [])
        if p["id"] != photo_id
    ]
    save_users(users)
    return jsonify({"success": True})

@app.route("/api/gallery/update/<photo_id>", methods=["POST"])
def update_gallery_caption(photo_id):
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    users = load_users()
    email = session["user"]
    if email not in users:
        return jsonify({"error": "Session expired"}), 401
    data = request.get_json()
    for p in users[email].get("gallery", []):
        if p["id"] == photo_id:
            p["caption"] = data.get("caption", p.get("caption", "")).strip()[:120]
            p["tag"] = data.get("tag", p.get("tag", "")).strip()
            break
    save_users(users)
    return jsonify({"success": True})

# ------------------ DR. PET CHATBOT ------------------

@app.route("/api/drpet/chat", methods=["POST"])
def drpet_chat():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    users = load_users()
    email = session["user"]

    if email not in users:
        session.clear()
        return jsonify({"error": "Session expired"}), 401

    user = users[email]
    data = request.get_json()
    user_message = data.get("message", "").strip()
    image_data = data.get("image_data")        # base64 string (no prefix)
    image_media_type = data.get("media_type", "image/jpeg")

    if not user_message and not image_data:
        return jsonify({"error": "Empty message"}), 400

    # Restore or initialise conversation history
    if "drpet_history" not in session:
        session["drpet_history"] = []

    bot = DrPetChatbot(
        pet_name=user.get("pet_name", "your pet"),
        pet_type=user.get("pet_type", "pet"),
        breed=user.get("breed", "unknown breed"),
        pet_dob=user.get("pet_dob", ""),
        owner_name=user.get("name", "there")
    )

    bot.conversation_history = session["drpet_history"]
    response = bot.chat(user_message, image_data=image_data, image_media_type=image_media_type)
    session["drpet_history"] = bot.conversation_history

    return jsonify({"response": response})


@app.route("/api/drpet/reset", methods=["POST"])
def drpet_reset():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    session.pop("drpet_history", None)
    return jsonify({"success": True})


def open_browser():
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)

    # create empty file if missing
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({}, f)

    threading.Timer(1.2, open_browser).start()

    app.run(debug=False, port=5000)