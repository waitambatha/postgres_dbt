import psycopg2
import random
import string

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="my_project_db",
    user="postgres",
    password="your_password",  # Replace with your PostgreSQL password
    host="localhost"
)
cur = conn.cursor()

# Function to generate random names and emails
def random_string(length=10):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

# Insert 100 random users
for _ in range(100):
    first_name = random_string(5)
    last_name = random_string(7)
    email = f"{first_name}.{last_name}@example.com"
    age = random.randint(18, 80)
    cur.execute(
        "INSERT INTO users (first_name, last_name, email, age) VALUES (%s, %s, %s, %s)",
        (first_name, last_name, email, age)
    )

# Commit changes and close connection
conn.commit()
cur.close()
conn.close()