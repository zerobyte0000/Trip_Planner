from flask import Flask, render_template, request, redirect, url_for, session
import json
import os
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a strong, random key

USER_DATA_FILE = 'data/users.json'

def load_users():
    if not os.path.exists(USER_DATA_FILE):
        return {}
    with open(USER_DATA_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    os.makedirs(os.path.dirname(USER_DATA_FILE), exist_ok=True)
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f)

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users:
            return render_template('signin.html', error='Username already exists. Please choose another.')
        users[username] = {'password': password}
        save_users(users)
        return redirect(url_for('login'))
    return render_template('signin.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('budget'))
        else:
            return render_template('login.html', error='Invalid username or password.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/budget', methods=['GET', 'POST'])
def budget():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        session['budget'] = float(request.form['total_budget'])
        session['num_days'] = int(request.form['num_days'])
        session['start_date'] = request.form['start_date']
        session['end_date'] = request.form['end_date']
        return redirect(url_for('plan'))
    return render_template('budget.html')

@app.route('/plan', methods=['GET', 'POST'])
def plan():
    if 'username' not in session:
        return redirect(url_for('login'))
    if 'budget' not in session or 'num_days' not in session:
        return redirect(url_for('budget'))

    budget = session['budget']
    num_days = session['num_days']

    if request.method == 'POST':
        num_people = int(request.form['num_people'])
        session['num_people'] = num_people
        daily_food = float(request.form.get('food_per_day', 0)) * num_people
        daily_stay = float(request.form.get('stay_per_day', 0)) * num_people
        daily_emergency = float(request.form.get('emergency_per_day', 0)) * num_people

        session['daily_plan'] = {
            'food': daily_food,
            'stay': daily_stay,
            'emergency': daily_emergency
        }

        session['visiting_places'] = []
        for i in range(1, num_days + 1):
            place = request.form.get(f'day_{i}_place', '')
            session['visiting_places'].append(place)

        estimated_cost = (daily_food + daily_stay + daily_emergency) * num_days
        session['estimated_cost'] = estimated_cost
        session['remaining_budget'] = budget - estimated_cost

        # Basic suggestion (needs more sophisticated logic)
        session['transport_suggestion'] = "Consider local transport options."
        if session['remaining_budget'] > 5000: # Example threshold
            session['transport_suggestion'] = "Budget allows for train or short flight. Check options on the next page."

        return redirect(url_for('home'))

    return render_template('plan.html', num_days=num_days)

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/flight_train', methods=['GET', 'POST'])
def flight_train():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        start_place = request.form['start_place']
        destination = request.form['destination']
        travel_date = request.form['travel_date']
        adults = int(request.form['adults'])
        seniors = int(request.form['seniors'])
        children = int(request.form['children'])

        # In a real app, you'd integrate with an API to fetch prices and routes
        # For now, let's just store the information
        session['flight_train_details'] = {
            'start_place': start_place,
            'destination': destination,
            'travel_date': travel_date,
            'adults': adults,
            'seniors': seniors,
            'children': children
        }
        return redirect(url_for('my_trip'))
    return render_template('flight_train.html')

@app.route('/hotel', methods=['GET', 'POST'])
def hotel():
    if 'username' not in session:
        return redirect(url_for('login'))
    destination = session.get('flight_train_details', {}).get('destination', '') # Get destination if available
    if request.method == 'POST':
        num_rooms = int(request.form['num_rooms'])
        room_type = request.form['room_type']
        num_guests = int(request.form['num_guests']) # You'd need to handle max occupancy
        session['hotel_details'] = {
            'num_rooms': num_rooms,
            'room_type': room_type,
            'num_guests': num_guests
        }
        return redirect(url_for('my_trip')) # Redirect to final plan after booking
    # In a real app, you'd fetch hotel data based on the destination
    hotels = [
        {'name': 'Luxury Inn', 'stars': 5},
        {'name': 'Comfort Suites', 'stars': 3},
        {'name': 'Budget Stay', 'stars': 2}
    ]
    return render_template('hotel.html', destination=destination, hotels=hotels)

@app.route('/my_trip')
def my_trip():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('my_trip.html', session=session)

if __name__ == '__main__':
    app.run(debug=True)