from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dummy login credentials including access token
DUMMY_USERNAME = "user"
DUMMY_PASSWORD = "pass123"
DUMMY_ACCESS_TOKEN = "token123"

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
        return redirect(url_for('dashboard'))
    return render_template('index.html', error="Invalid credentials or access token")

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

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
        return redirect(url_for('user_dashboard'))
    return render_template('tracking.html')


if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
