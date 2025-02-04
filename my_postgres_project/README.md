
### **Title: End-to-End dbt and PostgreSQL Integration Project**

---

## **1. Introduction**
This document provides a step-by-step guide to setting up a PostgreSQL database, populating it with random data, and integrating it with dbt for data transformation and analysis. The project is executed entirely locally, leveraging dbt Core for transformations and exploring its key features.

---

## **2. Step-by-Step Process**

### **2.1 Setting Up PostgreSQL**
1. **Install PostgreSQL**:
   - Install PostgreSQL on your local machine using package managers (e.g., `apt` for Ubuntu, `brew` for macOS) or download it from the official website.
   
2. **Create a Database and Table**:
   - Use the `psql` command-line tool to create a new database (`my_project_db`) and a table (`users`) to store user data.
   - Example SQL commands:
     ```sql
     CREATE DATABASE my_project_db;
     \c my_project_db;
     CREATE TABLE users (
         id SERIAL PRIMARY KEY,
         first_name VARCHAR(50),
         last_name VARCHAR(50),
         email VARCHAR(100),
         age INT,
         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
     );
     ```

3. **Insert Random Data**:
   - Write a Python script to populate the `users` table with random data. This ensures we have enough data for transformation and analysis.
   - Example Python script:
     ```python
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
     ```

---

### **2.2 Installing and Configuring dbt Core**
1. **Install dbt Core**:
   - Install dbt Core with support for PostgreSQL:
     ```bash
     pip install dbt-postgres
     ```
   - Verify the installation:
     ```bash
     dbt --version
     ```

2. **Initialize a New dbt Project**:
   - Initialize a new dbt project:
     ```bash
     dbt init my_postgres_project
     cd my_postgres_project
     ```
   - Update the `~/.dbt/profiles.yml` file with your PostgreSQL connection details:
     ```yaml
     my_postgres_project:
       target: dev
       outputs:
         dev:
           type: postgres
           host: localhost
           user: postgres
           password: your_password  # Replace with your PostgreSQL password
           port: 5432
           dbname: my_project_db
           schema: public
     ```

3. **Test the Connection**:
   - Test if dbt can connect to your database:
     ```bash
     dbt debug
     ```

---

### **2.3 Writing dbt Models**
1. **Create Staging Models**:
   - In the `models` directory, create a file called `stg_users.sql`:
     ```sql
     -- models/stg_users.sql
     SELECT
         id,
         first_name,
         last_name,
         email,
         age,
         created_at
     FROM users
     WHERE age >= 18
     ```

2. **Create Derived Metrics**:
   - Create another file called `user_metrics.sql`:
     ```sql
     -- models/user_metrics.sql
     SELECT
         COUNT(*) AS total_users,
         AVG(age) AS avg_age
     FROM {{ ref('stg_users') }}
     ```

3. **Add Tests**:
   - Add tests to ensure data quality. For example, test that all email addresses are unique:
     ```yaml
     # models/users.yml
     version: 2

     models:
       - name: stg_users
         columns:
           - name: email
             tests:
               - unique
     ```

---

### **2.4 Running and Testing Models**
1. **Compile the Models**:
   - Compile your models to check for syntax errors:
     ```bash
     dbt compile
     ```

2. **Run the Models**:
   - Run the models to execute the transformations:
     ```bash
     dbt run
     ```

3. **Generate Documentation**:
   - Generate documentation for your project:
     ```bash
     dbt docs generate
     dbt docs serve
     ```
   - Open your browser and navigate to `http://localhost:8080` to view the documentation.

---

### **2.5 Exploring Additional dbt Features**
1. **Snapshots**:
   - Capture historical data using snapshots. Create a snapshot configuration in `snapshots/snapshots.sql`:
     ```sql
     -- snapshots/users_snapshot.sql
     {% snapshot users_snapshot %}
         {{
             config(
                 target_database='my_project_db',
                 target_schema='public',
                 unique_key='id',
                 strategy='timestamp',
                 updated_at='created_at'
             )
         }}
         SELECT * FROM users
     {% endsnapshot %}
     ```
   - Run the snapshot:
     ```bash
     dbt snapshot
     ```

2. **Seeds**:
   - Load static data into your database using seeds. Create a CSV file in the `seeds` directory:
     ```csv
     # seeds/countries.csv
     country_code,country_name
     US,United States
     CA,Canada
     GB,United Kingdom
     ```
   - Load the seed data:
     ```bash
     dbt seed
     ```

3. **Macros**:
   - Reuse SQL logic across models using macros. Create a macro in `macros/macros.sql`:
     ```sql
     -- macros/get_current_timestamp.sql
     {% macro get_current_timestamp() %}
         CURRENT_TIMESTAMP
     {% endmacro %}
     ```
   - Use the macro in your models:
     ```sql
     -- models/example_model.sql
     SELECT
         id,
         {{ get_current_timestamp() }} AS processed_at
     FROM users
     ```

---

### **2.6 Automating Your Workflow**
- Automate your dbt runs using tools like cron (Linux/macOS) or Task Scheduler (Windows). Example cron job to run dbt daily at midnight:
  ```bash
  0 0 * * * cd /path/to/my_postgres_project && dbt run
  ```

---

## **3. Conclusion**
This project demonstrates how to set up a PostgreSQL database, populate it with random data, and integrate it with dbt for data transformation and analysis. By leveraging dbt's features, you can efficiently transform raw data into insights and automate your workflows.

---

### **Appendix: Key dbt Commands**
- `dbt init`: Initialize a new dbt project.
- `dbt debug`: Test the connection to your database.
- `dbt compile`: Compile your models to check for syntax errors.
- `dbt run`: Execute your models.
- `dbt test`: Run tests to validate data quality.
- `dbt docs generate`: Generate documentation for your project.
- `dbt docs serve`: Serve the documentation locally.
- `dbt snapshot`: Run snapshots to capture historical data.
- `dbt seed`: Load static data using seeds.

---
