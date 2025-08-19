from flask import Flask, render_template, request, redirect, url_for
from math import radians, sin, cos, sqrt, atan2
import os

app = Flask(__name__)

# Dummy login credentials including access token
DUMMY_USERNAME = "user"
DUMMY_PASSWORD = "pass123"
DUMMY_ACCESS_TOKEN = "token123"
homeLat = 30.3529 
homeLng = 76.3637

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['email']
    password = request.form['password']
    access_token = request.form['access_token']
    if (username == DUMMY_USERNAME and 
        password == DUMMY_PASSWORD and 
        access_token == DUMMY_ACCESS_TOKEN):
        return redirect(url_for('user_dashboard'))
    return render_template('index.html', error="Invalid credentials or access token")



@app.route('/user_dashboard')
def user_dashboard():
    return render_template('user_dashboard.html')

@app.route('/tracking', methods=['GET', 'POST'])
def tracking():
    if request.method == 'POST':
        vaccine_type = request.form.get('vaccine')  
        latitude = request.form.get('lat')         
        longitude = request.form.get('lng')          
        print(f"Vaccine Type: {vaccine_type}, Latitude: {latitude}, Longitude: {longitude}")
        # Convert latitude and longitude from string to float
        lat1 = float(homeLat)
        lon1 = float(homeLng)
        lat2 = float(latitude)
        lon2 = float(longitude)

        # Haversine formula
        R = 6371  # Earth radius in kilometers
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c

        data = {
            "vaccine_type": vaccine_type,
            "latitude": latitude,
            "longitude": longitude,
            "distance": f"{distance:.2f} km"
        }
        print(f"Distance: {data['distance']}")  
        if(distance>15):
            print("here")
            return render_template("user_dashboard.html", error="Drone is too far from the home location.")
        elif (distance<0.5):
            print("there")
            return render_template("user_dashboard.html", error="Drone is too close to the home location.")
        else:
            return render_template("tracking.html",data=data)
    return render_template('tracking.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
