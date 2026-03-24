# 🐾 PawCare

A Flask web app for tracking your pet's vaccinations, feeding schedule, health info, and chatting with Dr. Paws (AI vet assistant).

---

## ✅ Changes in This Version
- **Vaccine section**: Proper up-to-date status (Done / Due Soon / Overdue / Upcoming)
- **Vaccine Reminders**: New reminder card shows which vaccines need attention
- **Delete Pet Profile**: Button in Profile section to permanently delete your account
- **Chatbot**: Replaced OpenAI with **Groq** (free, fast, no credit card needed)

---

## 🚀 How to Run

### Step 1 — Install Python
Make sure Python 3.8+ is installed:
```
python --version
```

### Step 2 — Install dependencies
Open a terminal in the `pet_app` folder and run:
```
pip install -r requirements.txt
```

### Step 3 — Get a FREE Groq API Key (for chatbot)
1. Go to https://console.groq.com
2. Sign up for a free account (no credit card needed)
3. Click **API Keys** → **Create API Key**
4. Copy the key

### Step 4 — Set the Groq API Key

**On Windows (Command Prompt):**
```
set GROQ_API_KEY=your_key_here
```

**On Mac/Linux:**
```
export GROQ_API_KEY=your_key_here
```

### Step 5 — Run the app
```
python app.py
```

### Step 6 — Open in browser
Go to: **http://localhost:5000**

---

## 📁 File Structure
```
pet_app/
├── app.py          ← Flask backend (routes, API)
├── pet_data.py     ← Pet breeds, vaccine schedules, feeding data
├── requirements.txt
├── templates/       ← (Flask looks here, rename if needed — see note)
│   └── dashboard.html, login.html, signup.html, index.html
└── data/
    └── users.json  ← Auto-created on first signup
```

> ⚠️ **Note:** Flask looks for templates in a `templates/` folder.
> If your HTML files are in the root `pet_app/` folder, create a `templates/` subfolder and move the HTML files there, OR the app is already configured to find them (check `app.py`).

---

## 🤖 Chatbot — Groq vs OpenAI
| Feature | Groq (new) | OpenAI (old) |
|---|---|---|
| Cost | **Free** | Paid |
| Speed | Very fast | Moderate |
| Model | Llama 3 8B | GPT-3.5 |
| Sign-up | console.groq.com | platform.openai.com |

