from flask import Flask, render_template, request, redirect, url_for, session,flash
import random
import requests


app = Flask(__name__)
API_KEY="9584b2e7bfa79e3ba2d6ab7fc3f21fad"
app.secret_key = "secret"

# Dashboard
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

# Calculator
@app.route('/calculator', methods=["GET", "POST"])
def calculator():
    result = ""
    num1 = ""
    num2 = ""
    operator = ""

    if request.method == "POST":
        num1 = request.form.get("num1")
        num2 = request.form.get("num2")
        operator = request.form.get("operator")

        try:
            num1 = float(num1)
            num2 = float(num2)

            if operator == "add":
                result = num1 + num2
            elif operator == "subtract":
                result = num1 - num2
            elif operator == "multiply":
                result = num1 * num2
            elif operator == "divide":
                result = "Cannot divide by zero" if num2 == 0 else num1 / num2
            else:
                result = "Invalid operator"
        except ValueError:
            result = "Please enter valid numbers."

    return render_template("calculator.html", result=result, num1=num1, num2=num2, operator=operator)

# Currency Converter
@app.route('/converter', methods=['GET', 'POST'])
def converter():
    converted = None
    if request.method == 'POST':
        amount = float(request.form['amount'])
        rate = float(request.form['rate'])
        converted = round(amount * rate, 2)
    return render_template('converter.html', converted=converted)

# Rock Paper Scissors
@app.route('/rps', methods=['GET', 'POST'])
def rps():
    result = ""
    if request.method == 'POST':
        user = request.form['choice']
        comp = random.choice(['rock', 'paper', 'scissors'])
        if user == comp:
            result = "Draw!"
        elif (user == "rock" and comp == "scissors") or \
             (user == "scissors" and comp == "paper") or \
             (user == "paper" and comp == "rock"):
            result = "You Win!"
        else:
            result = "Computer Wins!"
    return render_template('rps.html', result=result)

# Guessing Game
@app.route('/guess', methods=['GET', 'POST'])
def guess():
    msg = ""
    if 'number' not in session:
        session['number'] = random.randint(1, 100)  # Match the range shown in HTML

    if request.method == 'POST':
        try:
            user_input = request.form.get('guess', '')
            if not user_input.isdigit():
                msg = "Please enter a valid number."
            else:
                guess = int(user_input)
                target = session['number']
                if guess == target:
                    msg = "🎉 Correct! You've guessed it!"
                    session.pop('number', None)  # Reset for a new game
                elif guess < target:
                    msg = "Too Low! Try again."
                else:
                    msg = "Too High! Try again."
        except Exception as e:
            msg = f"Error: {str(e)}"

    return render_template('guess.html', message=msg)


# Register/Login
users = {}

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ""
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        users[uname] = pwd
        msg = "Registered successfully!"
    return render_template('register.html', message=msg)

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ""
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        if users.get(uname) == pwd:
            msg = "Login successful"
        else:
            msg = "Login failed"
    return render_template('login.html', message=msg)

API_KEY = "9584b2e7bfa79e3ba2d6ab7fc3f21fad"  # Replace this with your actual API key

@app.route("/weather", methods=["GET", "POST"])
def weather():
    weather_data = None
    if request.method == "POST":
        city = request.form.get("city")
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather_data = {
                "city": city,
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "icon": data["weather"][0]["icon"]
            }
        else:
            weather_data = {"error": "City not found"}
    return render_template("weather.html", weather=weather_data)

@app.route('/feedback', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form.get('name')
        comments = request.form.get('comments')
        flash("Thank you for your feedback!")
        return redirect(url_for('home'))  # Reload same page
    
    return render_template('feedback.html')
if __name__== '__main__':
    app.run(debug=True)