from flask import Flask, render_template, request, redirect, session
import sqlite3
import pickle

app = Flask(__name__)
app.secret_key = "secret123"

# Load ML model
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# ---------------- DATABASE ----------------
def create_table():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

create_table()

# ---------------- ROUTES ----------------

@app.route('/')
def login():
    return render_template("login.html")

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/register', methods=['POST'])
def register():
    user = request.form['username']
    pwd = request.form['password']

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users(username,password) VALUES(?,?)", (user,pwd))
    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/login_check', methods=['POST'])
def login_check():
    user = request.form['username']
    pwd = request.form['password']

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (user,pwd))
    data = cursor.fetchone()
    conn.close()

    if data:
        session['user'] = user
        return redirect('/dashboard')
    else:
        return "Invalid Login"

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template("dashboard.html")
    return redirect('/')

@app.route('/predict', methods=['POST'])
def predict():
    text = request.form['text']
    vector = vectorizer.transform([text])
    result = model.predict(vector)[0]

    # Suggestions
    suggestion = ""
    if result == "Depression":
        suggestion = "Talk to someone you trust ❤️"
    elif result == "Stress":
        suggestion = "Take rest and relax 🧘"
    else:
        suggestion = "Keep enjoying life 😊"

    return render_template("result.html", text=text, result=result, suggestion=suggestion)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)