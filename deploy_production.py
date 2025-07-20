#!/usr/bin/env python3
"""
🚀 NaturalSQL Production Deployment Script
==========================================
This script sets up the complete NaturalSQL system for production deployment.
"""

import os
import sys
import sqlite3
import subprocess
import json
from pathlib import Path

def print_banner():
    """Print deployment banner"""
    print("🚀 NaturalSQL Production Deployment")
    print("=" * 50)
    print("Setting up enterprise-grade Natural Language to SQL system...")
    print()

def check_dependencies():
    """Check and install required dependencies"""
    print("📦 Checking dependencies...")
    
    required_packages = [
        "gradio",
        "huggingface_hub", 
        "psycopg2-binary",
        "mysql-connector-python",
        "pymongo",
        "pandas",
        "numpy"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - Missing")
    
    if missing_packages:
        print(f"\n🔧 Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
            print("✅ All dependencies installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            return False
    
    return True

def setup_database():
    """Set up the sample database"""
    print("\n🗄️ Setting up database...")
    
    try:
        # Create sample SQLite database
        conn = sqlite3.connect('mydb.db')
        cursor = conn.cursor()
        
        # Create departments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                location TEXT,
                budget REAL
            )
        ''')
        
        # Create employees table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT,
                age INTEGER,
                salary REAL,
                position TEXT,
                city TEXT,
                join_date TEXT,
                department_id INTEGER,
                FOREIGN KEY (department_id) REFERENCES departments (id)
            )
        ''')
        
        # Insert sample departments
        departments_data = [
            (1, 'Engineering', 'New York', 1000000.0),
            (2, 'Marketing', 'London', 500000.0),
            (3, 'Sales', 'Tokyo', 750000.0),
            (4, 'HR', 'Paris', 300000.0)
        ]
        
        cursor.executemany('INSERT OR REPLACE INTO departments VALUES (?, ?, ?, ?)', departments_data)
        
        # Insert sample employees
        employees_data = [
            (1, 'John Smith', 'john@company.com', 35, 75000.0, 'Software Engineer', 'New York', '2020-01-15', 1),
            (2, 'Alice Johnson', 'alice@company.com', 28, 65000.0, 'Marketing Manager', 'London', '2019-03-20', 2),
            (3, 'Bob Wilson', 'bob@company.com', 42, 85000.0, 'Senior Engineer', 'New York', '2018-07-10', 1),
            (4, 'Jane Brown', 'jane@company.com', 31, 70000.0, 'Sales Representative', 'Tokyo', '2021-02-28', 3),
            (5, 'Mike Davis', 'mike@company.com', 29, 60000.0, 'HR Specialist', 'Paris', '2020-11-05', 4),
            (6, 'Sarah Miller', 'sarah@company.com', 33, 72000.0, 'Product Manager', 'New York', '2019-09-12', 1),
            (7, 'David Garcia', 'david@company.com', 38, 80000.0, 'Lead Developer', 'New York', '2017-05-18', 1),
            (8, 'Lisa Anderson', 'lisa@company.com', 26, 55000.0, 'Marketing Assistant', 'London', '2021-06-30', 2),
            (9, 'Tom Martinez', 'tom@company.com', 45, 90000.0, 'Senior Manager', 'New York', '2016-12-01', 1),
            (10, 'Emma Taylor', 'emma@company.com', 27, 58000.0, 'Sales Assistant', 'Tokyo', '2022-01-15', 3)
        ]
        
        cursor.executemany('INSERT OR REPLACE INTO employees VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', employees_data)
        
        conn.commit()
        conn.close()
        
        print("✅ Database setup completed!")
        print(f"   - Created {len(departments_data)} departments")
        print(f"   - Created {len(employees_data)} employees")
        
        return True
        
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

def validate_system():
    """Validate the complete system"""
    print("\n🔍 Validating system...")
    
    try:
        # Test pipeline
        from pipeline import nl_to_sql
        
        test_queries = [
            "Show all employees",
            "Show employees who earn more than average",
            "Rank employees by salary",
            "Show high salary employees",
            "Show employees with rollup"
        ]
        
        print("Testing core functionality:")
        for query in test_queries:
            try:
                sql = nl_to_sql(query)
                print(f"✅ '{query}' → SQL generated successfully")
            except Exception as e:
                print(f"❌ '{query}' → Failed: {e}")
                return False
        
        # Test database connection
        conn = sqlite3.connect('mydb.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM employees")
        count = cursor.fetchone()[0]
        conn.close()
        
        print(f"✅ Database connection: {count} employees found")
        
        return True
        
    except Exception as e:
        print(f"❌ System validation failed: {e}")
        return False

def create_config():
    """Create production configuration"""
    print("\n⚙️ Creating configuration...")
    
    config = {
        "database": {
            "sqlite": {
                "path": "mydb.db"
            },
            "postgresql": {
                "host": "localhost",
                "port": 5432,
                "database": "naturalsql",
                "user": "postgres",
                "password": ""
            },
            "mysql": {
                "host": "localhost",
                "port": 3306,
                "database": "naturalsql",
                "user": "root",
                "password": ""
            },
            "mongodb": {
                "uri": "mongodb://localhost:27017/",
                "database": "naturalsql"
            }
        },
        "features": {
            "subqueries": True,
            "window_functions": True,
            "ctes": True,
            "advanced_aggregations": True,
            "joins": True,
            "group_by": True,
            "having": True
        },
        "ui": {
            "theme": "default",
            "examples": True,
            "history": True,
            "export": True
        }
    }
    
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ Configuration created: config.json")

def main():
    """Main deployment function"""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Deployment failed: Dependencies not satisfied")
        return False
    
    # Setup database
    if not setup_database():
        print("❌ Deployment failed: Database setup failed")
        return False
    
    # Create configuration
    create_config()
    
    # Validate system
    if not validate_system():
        print("❌ Deployment failed: System validation failed")
        return False
    
    print("\n🎉 NaturalSQL Production Deployment Complete!")
    print("=" * 50)
    print("✅ All dependencies installed")
    print("✅ Database configured")
    print("✅ System validated")
    print("✅ Configuration created")
    print("\n🚀 To start the application:")
    print("   python app.py")
    print("\n🌐 Access the web interface at:")
    print("   http://127.0.0.1:7860")
    print("\n📚 Available features:")
    print("   - Basic SQL queries (SELECT, INSERT, UPDATE, DELETE)")
    print("   - Advanced JOINs and GROUP BY")
    print("   - Subqueries and window functions")
    print("   - CTEs and advanced aggregations")
    print("   - Multi-database support")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 