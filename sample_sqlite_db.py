import sqlite3
import os

def create_sample_database():
    """Create a sample SQLite database with employees and departments tables"""
    
    # Remove existing database if it exists
    if os.path.exists('mydb.db'):
        os.remove('mydb.db')
    
    # Create connection
    conn = sqlite3.connect('mydb.db')
    cursor = conn.cursor()
    
    # Create departments table
    cursor.execute('''
        CREATE TABLE departments (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            location TEXT,
            budget REAL
        )
    ''')
    
    # Create employees table with department_id foreign key
    cursor.execute('''
        CREATE TABLE employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER,
            city TEXT,
            salary REAL,
            position TEXT,
            email TEXT,
            join_date TEXT,
            department_id INTEGER,
            FOREIGN KEY (department_id) REFERENCES departments (id)
        )
    ''')
    
    # Insert sample departments
    departments = [
        (1, 'Engineering', 'New York', 1000000),
        (2, 'Marketing', 'London', 500000),
        (3, 'Sales', 'Tokyo', 750000),
        (4, 'HR', 'Paris', 300000),
        (5, 'Finance', 'Berlin', 600000)
    ]
    
    cursor.executemany('INSERT INTO departments VALUES (?, ?, ?, ?)', departments)
    
    # Insert sample employees with department_id
    employees = [
        (1, 'John Smith', 30, 'New York', 75000, 'Software Engineer', 'john@company.com', '2020-01-15', 1),
        (2, 'Alice Johnson', 28, 'London', 65000, 'Data Scientist', 'alice@company.com', '2019-03-20', 1),
        (3, 'Bob Wilson', 35, 'Tokyo', 85000, 'Product Manager', 'bob@company.com', '2018-07-10', 1),
        (4, 'Jane Brown', 32, 'Paris', 70000, 'Marketing Manager', 'jane@company.com', '2021-02-28', 2),
        (5, 'Mike Davis', 29, 'Berlin', 60000, 'Sales Representative', 'mike@company.com', '2020-11-15', 3),
        (6, 'Sarah Miller', 31, 'New York', 55000, 'HR Specialist', 'sarah@company.com', '2021-05-10', 4),
        (7, 'David Garcia', 33, 'London', 80000, 'Financial Analyst', 'david@company.com', '2019-09-01', 5),
        (8, 'Lisa Anderson', 27, 'Tokyo', 70000, 'Software Engineer', 'lisa@company.com', '2021-08-20', 1),
        (9, 'Tom Martinez', 34, 'Paris', 90000, 'Senior Engineer', 'tom@company.com', '2017-12-05', 1),
        (10, 'Emma Taylor', 26, 'Berlin', 65000, 'Marketing Coordinator', 'emma@company.com', '2022-01-15', 2)
    ]
    
    cursor.executemany('INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', employees)
    
    # Commit and close
    conn.commit()
    conn.close()
    
    print("✅ Sample database created successfully!")
    print("📊 Tables created:")
    print("   - departments (id, name, location, budget)")
    print("   - employees (id, name, age, city, salary, position, email, join_date, department_id)")
    print("🔗 Foreign key: employees.department_id -> departments.id")
    print("📁 Database file: mydb.db")

if __name__ == "__main__":
    create_sample_database() 