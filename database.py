import pymysql

timeout = 10
connection = pymysql.connect(
  charset="utf8mb4",
  connect_timeout=timeout,
  cursorclass=pymysql.cursors.DictCursor,
  db="defaultdb",
  host="drone-dispatch-system-thapar-a4f3.c.aivencloud.com",
  password="AVNS_jjQPJ7jxq9aVaNDMFBE",
  read_timeout=timeout,
  port=23916,
  user="avnadmin",
  write_timeout=timeout,
)

def delete_tables():
    try:
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS deliveries")
        # cursor.execute("DROP TABLE IF EXISTS users")
        # cursor.execute("DROP TABLE IF EXISTS vaccines")
        connection.commit()
    except Exception as e:
        print(f"Error deleting tables: {e}")
    finally:
        cursor.close()
def show_contents():
    try:
        cursor = connection.cursor()
        print("Users table:")
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        for row in users:
            print(row)
        print("\nVaccines table:")
        cursor.execute("SELECT * FROM vaccines")
        vaccines = cursor.fetchall()
        for row in vaccines:
            print(row)
        print("\nDeliveries table:")
        cursor.execute("SELECT * FROM deliveries")
        deliveries = cursor.fetchall()
        for row in deliveries:
            print(row)
    except Exception as e:
        print(f"Error fetching data: {e}")
    finally:
        cursor.close()

def create_tables():
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                email VARCHAR(100) PRIMARY KEY,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vaccines (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                image_url TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS deliveries (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_mail VARCHAR(100) NOT NULL,
                vaccine_id INT,
                latitude DECIMAL(10,6) NOT NULL,
                longitude DECIMAL(10,6) NOT NULL,
                distance_km DECIMAL(6,2),
                status VARCHAR(20) DEFAULT 'created',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_mail) REFERENCES users(email),
                FOREIGN KEY (vaccine_id) REFERENCES vaccines(id)
            )
        """)
        connection.commit()
    except Exception as e:
        print(f"Error creating tables: {e}")
    finally:
        cursor.close()
def add_vaccine(name, description, image_url):
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO vaccines (name, description, image_url) VALUES (%s, %s, %s)", (name, description, image_url))
        connection.commit()
    except Exception as e:
        print(f"Error adding vaccine: {e}")
    finally:
        cursor.close()
if __name__ == "__main__":
    # delete_tables()
    # print("Existing tables deleted successfully.")
    create_tables()
    # print("Database tables created successfully.")
    # add_vaccine("Anti Venom", "Used to treat venomous bites and stings from snakes and insects.", "https://tse1.mm.bing.net/th/id/OIP.pwW7kr8TEt3-jXFVhp1RugHaE8?w=1024&h=683&rs=1&pid=ImgDetMain&o=7&rm=3")
    # add_vaccine("Measles Vaccine", "Prevents measles, a highly contagious viral disease.", "https://today.uconn.edu/wp-content/uploads/2024/02/AdobeStock_283415438-scaled.jpeg")
    # add_vaccine("Polio Vaccine", "Protects against poliovirus, preventing paralysis and complications.", "https://w.ndtvimg.com/sites/3/2023/06/15175352/polio.jpg")
    # add_vaccine("Rabies Vaccine", "Prevents rabies infection after animal bites or exposure.", "https://www.annapharmacy.com/wp-content/uploads/2023/08/How-Long-Does-An-Anti-Rabies-Vaccine-Provide-Immunity-In-Humans-scaled.webp")
    # add_vaccine("Tetanus Vaccine", "Protects against tetanus, a serious bacterial infection.", "https://komonews.com/resources/media/7f9d1abc-2cdb-4622-8ebe-5e87bcafb623-TetanusShot_August.jpg")
    # add_vaccine("Hepatitis B Vaccine", "Prevents hepatitis B virus infection and liver complications.", "https://medicaldialogues.in/h-upload/2025/03/25/280095-hepatitis-b-vaccine.webp")
    show_contents()
    print("Contents of the users table:")