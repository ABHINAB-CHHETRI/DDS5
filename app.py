from flask import Flask, render_template, request, redirect, url_for, session
from math import radians, sin, cos, sqrt, atan2
import os
import dotenv
import pymysql

# Load environment variables
dotenv.load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "sfansofdbalsnkglasdg")

# Home location coordinates
HOME_LAT = 30.3529
HOME_LNG = 76.3637

# Access token for registration
ACCESS_TOKEN = "token123"

# Database configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "drone-dispatch-system-thapar-a4f3.c.aivencloud.com"),
    "port": int(os.getenv("DB_PORT", 23916)),
    "user": os.getenv("DB_USER", "avnadmin"),
    "password": os.getenv("DB_PASSWORD", "AVNS_jjQPJ7jxq9aVaNDMFBE"),
    "db": os.getenv("DB_NAME", "defaultdb"),
    "charset": os.getenv("DB_CHARSET", "utf8mb4"),
    "connect_timeout": int(os.getenv("DB_CONNECT_TIMEOUT", 10)),
    "read_timeout": int(os.getenv("DB_READ_TIMEOUT", 10)),
    "write_timeout": int(os.getenv("DB_WRITE_TIMEOUT", 10)),
    "cursorclass": getattr(pymysql.cursors, os.getenv("DB_CURSORCLASS", "DictCursor")),
}

def get_db_connection():
    try:
        return pymysql.connect(**DB_CONFIG)
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')
    email_error = password_error = error = None

    if not email:
        email_error = "Email is required."
    elif "@" not in email or "." not in email:
        email_error = "Invalid email address."
    if not password:
        password_error = "Password is required."

    if email_error or password_error:
        return render_template('index.html', email_error=email_error, password_error=password_error, email=email, signup_error=False)

    conn = get_db_connection()
    if not conn:
        error = "Database connection error."
        return render_template('index.html', error=error, email=email, signup_error=False)

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
            user = cursor.fetchone()
        if not user:
            error = "Invalid credentials"
            return render_template('index.html', error=error, email=email, signup_error=False)
        session['user_email'] = email
        session['logged_in'] = True
        return redirect(url_for('user_dashboard'))
    finally:
        conn.close()

def get_user_by_email(email):
    conn = get_db_connection()
    if not conn:
        return None
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            return cursor.fetchone()
    except Exception as e:
        print(f"Error fetching user: {e}")
        return None
    finally:
        conn.close()

def add_user(email, password):
    conn = get_db_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding user: {e}")
        return False
    finally:
        conn.close()

@app.route('/register', methods=['POST'])
def register():
    email = request.form.get('email_', '').strip()
    password = request.form.get('password_', '')
    access_token = request.form.get('access_token', '')
    email_error = password_error = access_token_error = error = None

    if not email:
        email_error = "Email is required."
    elif "@" not in email or "." not in email:
        email_error = "Invalid email address."
    elif get_user_by_email(email):
        email_error = "Email already exists."
    if not password:
        password_error = "Password is required."
    elif len(password) < 8:
        password_error = "Password must be at least 8 characters long."
    if not access_token:
        access_token_error = "Access token is required."
    elif access_token != ACCESS_TOKEN:
        access_token_error = "Invalid access token."

    if email_error or password_error or access_token_error:
        return render_template('index.html', email_error=email_error, password_error=password_error, access_token_error=access_token_error, signup_error=True, email=email, access_token=access_token, password=password)

    if not add_user(email, password):
        error = "Failed to register user."
        return render_template('index.html', error=error, signup_error=True)

    session['user_email'] = email
    session['logged_in'] = True
    return redirect(url_for('user_dashboard'))

@app.route('/user_dashboard')
def user_dashboard():
    connection= get_db_connection()
    if not connection:
        return render_template('user_dashboard.html', error="Database connection error.")
    cursor= connection.cursor()
    cursor.execute("SELECT * FROM vaccines")
    vaccines = cursor.fetchall()
    cursor.close()
    session['vaccines'] = vaccines
    return render_template('user_dashboard.html')

@app.route('/tracking', methods=['GET', 'POST'])
def tracking():
    if request.method == 'POST':
        vaccine_type = request.form.get('vaccine')
        latitude = request.form.get('lat')
        longitude = request.form.get('lng')
        vaccine_error=None
        location_error=None
        if not vaccine_type:
            vaccine_error = "Please select a vaccine type."
        if not latitude or not longitude:
            location_error = "Please provide valid latitude and longitude."
        if vaccine_error or location_error:
            return render_template("user_dashboard.html", vaccine_error=vaccine_error, location_error=location_error)
        try:
            lat2 = float(latitude)
            lon2 = float(longitude)
        except (TypeError, ValueError):
            return render_template("user_dashboard.html", error="Invalid coordinates.")

        # Haversine formula
        R = 6371  # Earth radius in kilometers
        dlat = radians(lat2 - HOME_LAT)
        dlon = radians(lon2 - HOME_LNG)
        a = sin(dlat / 2)**2 + cos(radians(HOME_LAT)) * cos(radians(lat2)) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c

        data = {
            "vaccine_type": vaccine_type,
            "latitude": latitude,
            "longitude": longitude,
            "distance": f"{distance:.2f}"
        }

        if distance > 15:
            return render_template("user_dashboard.html", error="Drone is too far from the home location.")
        else:
            # Find vaccine_id from session vaccines
            vaccine_id = None
            for vaccine in session.get('vaccines', []):
                if vaccine['name'] == vaccine_type:
                    vaccine_id = vaccine['id']
                    break
            # Save tracking info to database
            conn = get_db_connection()
            if conn:
                try:
                    with conn.cursor() as cursor:
                        cursor.execute(
                            "INSERT INTO deliveries (user_email, vaccine_id, latitude, longitude, distance_km) VALUES (%s, %s, %s, %s, %s)",
                            (session.get('user_email'), vaccine_id, lat2, lon2, distance)
                        )
                    conn.commit()
                except Exception as e:
                    print(f"Error saving tracking info: {e}")
                finally:
                    conn.close()
            return render_template("tracking.html", data=data)
    return render_template('tracking.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
