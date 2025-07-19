import gradio as gr
from pipeline import nl_to_sql
import sqlite3
import pandas as pd
import os

try:
    import psycopg2
except ImportError:
    psycopg2 = None

try:
    import mysql.connector
    mysql_connector_available = True
except ImportError:
    mysql_connector_available = False

try:
    import pymongo
except ImportError:
    pymongo = None

DB_TYPES = ["Demo (built-in schema)", "SQLite (upload .db)", "PostgreSQL", "MySQL", "MongoDB"]

def run_sql_on_sqlite(db_file, sql):
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        if sql.strip().lower().startswith("select"):
            columns = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
            df = pd.DataFrame(rows, columns=columns)
            result = df.to_markdown(index=False)
        else:
            conn.commit()
            result = f"Query executed successfully. Rows affected: {cur.rowcount}"
        cur.close()
        conn.close()
        return result, None
    except Exception as e:
        return None, str(e)

def run_sql_on_postgres(host, port, user, password, dbname, sql):
    if not psycopg2:
        return None, "psycopg2 is not installed. Cannot connect to PostgreSQL."
    try:
        conn = psycopg2.connect(
            host=host, port=port, user=user, password=password, dbname=dbname
        )
        cur = conn.cursor()
        cur.execute(sql)
        if sql.strip().lower().startswith("select"):
            columns = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
            df = pd.DataFrame(rows, columns=columns)
            result = df.to_markdown(index=False)
        else:
            conn.commit()
            result = f"Query executed successfully. Rows affected: {cur.rowcount}"
        cur.close()
        conn.close()
        return result, None
    except Exception as e:
        return None, str(e)

def run_sql_on_mysql(host, port, user, password, dbname, sql):
    if not mysql_connector_available:
        return None, "mysql-connector-python is not installed. Cannot connect to MySQL."
    try:
        conn = mysql.connector.connect(
            host=host, port=port, user=user, password=password, database=dbname
        )
        cur = conn.cursor()
        cur.execute(sql)
        if sql.strip().lower().startswith("select"):
            columns = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
            df = pd.DataFrame(rows, columns=columns)
            result = df.to_markdown(index=False)
        else:
            conn.commit()
            result = f"Query executed successfully. Rows affected: {cur.rowcount}"
        cur.close()
        conn.close()
        return result, None
    except Exception as e:
        return None, str(e)

def run_query_on_mongodb(connection_string, database_name, collection_name, nl_query):
    if not pymongo:
        return None, "pymongo is not installed. Cannot connect to MongoDB."
    try:
        client = pymongo.MongoClient(connection_string)
        db = client[database_name]
        collection = db[collection_name]
        
        # For now, we'll do a simple find operation
        # In the future, we can implement more complex MongoDB query generation
        if "show" in nl_query.lower() or "list" in nl_query.lower():
            documents = list(collection.find().limit(10))
            if documents:
                df = pd.DataFrame(documents)
                # Remove MongoDB's _id field for display
                if '_id' in df.columns:
                    df = df.drop('_id', axis=1)
                result = df.to_markdown(index=False)
            else:
                result = "No documents found in collection."
        else:
            result = "MongoDB query support is limited. Try 'Show all documents' or 'List documents'."
        
        client.close()
        return result, None
    except Exception as e:
        return None, str(e)

def process_query(nl_query, db_type, sqlite_file, pg_host, pg_port, pg_user, pg_pass, pg_db, mysql_host, mysql_port, mysql_user, mysql_pass, mysql_db, mongo_conn, mongo_db, mongo_collection):
    sql = nl_to_sql(nl_query)
    
    if db_type == "Demo (built-in schema)":
        return sql, "[Demo mode: No live database connected. SQL generated only.]"
    elif db_type == "SQLite (upload .db)":
        if sqlite_file is None:
            return sql, "Please upload a SQLite .db file."
        temp_path = "temp_uploaded.db"
        with open(temp_path, "wb") as f:
            f.write(sqlite_file.read())
        result, error = run_sql_on_sqlite(temp_path, sql)
        os.remove(temp_path)
        if error:
            return sql, f"❌ Error executing SQL on SQLite:\n{error}"
        return sql, result
    elif db_type == "PostgreSQL":
        if not all([pg_host, pg_port, pg_user, pg_pass, pg_db]):
            return sql, "Please provide all PostgreSQL connection details."
        result, error = run_sql_on_postgres(pg_host, pg_port, pg_user, pg_pass, pg_db, sql)
        if error:
            return sql, f"❌ Error executing SQL on PostgreSQL:\n{error}"
        return sql, result
    elif db_type == "MySQL":
        if not all([mysql_host, mysql_port, mysql_user, mysql_pass, mysql_db]):
            return sql, "Please provide all MySQL connection details."
        result, error = run_sql_on_mysql(mysql_host, mysql_port, mysql_user, mysql_pass, mysql_db, sql)
        if error:
            return sql, f"❌ Error executing SQL on MySQL:\n{error}"
        return sql, result
    elif db_type == "MongoDB":
        if not all([mongo_conn, mongo_db, mongo_collection]):
            return sql, "Please provide all MongoDB connection details."
        result, error = run_query_on_mongodb(mongo_conn, mongo_db, mongo_collection, nl_query)
        if error:
            return sql, f"❌ Error executing query on MongoDB:\n{error}"
        return sql, result
    else:
        return sql, "Unknown database type."

examples = [
    ["Show all employees"],
    ["Show employees from Engineering department"],
    ["Show employees earning more than 70000"],
    ["Show employees and their departments"],
    ["Show departments with average salary > 50000"],
    ["Show employees who earn more than average"],
    ["Show departments with more than 2 employees"],
    ["Show employees who earn less than average"],
    ["Show departments with more than 1 employee"],
    ["Rank employees by salary"],
    ["Show employees with row numbers"],
    ["Top 3 employees by salary"],
    ["Show high salary employees"],
    ["Show senior employees"],
    ["Show employees with rollup"],
    ["Show employees with cube"],
    ["Show hierarchical summary"]
]

schema_info = """
## 📊 Database Schema

### Tables:
- **employees**: id, name, email, age, salary, position, city, join_date, department_id
- **departments**: id, name, location, budget
- **projects**: id, name, description, start_date, end_date

### Supported Features:
- **Basic Queries**: SELECT, INSERT, UPDATE, DELETE
- **Filters**: WHERE conditions with operators (>, <, =, >=, <=, LIKE, BETWEEN)
- **JOINs**: INNER JOIN between employees and departments
- **GROUP BY**: Group employees by department, show departments with average salary
- **HAVING**: Show departments with average salary > 50000, departments with total salary > 200000
- **SUBQUERIES**: Show employees who earn more than average, show departments with more than 2 employees
- **WINDOW FUNCTIONS**: Rank employees by salary, show row numbers, top N employees
- **CTEs**: High salary employees, senior employees, department summary
- **ADVANCED AGGREGATIONS**: ROLLUP, CUBE for hierarchical analysis

### Advanced Natural Language Patterns:
- **Subqueries**: "Show employees who earn more than average" → `SELECT * FROM employees WHERE salary > (SELECT AVG(salary) FROM employees)`
- **Window Functions**: "Rank employees by salary" → `SELECT *, RANK() OVER (ORDER BY salary ASC) as rank_num FROM employees`
- **CTEs**: "Show high salary employees" → `WITH high_salary_employees AS (SELECT * FROM employees WHERE salary > 70000) SELECT * FROM employees`
- **Advanced Aggregations**: "Show employees with rollup" → `SELECT * FROM employees GROUP BY ROLLUP(department_id, position)`
"""

with gr.Blocks(
    title="NaturalSQL - Natural Language to SQL Converter (Multi-DB Edition)",
    theme=gr.themes.Soft(),
    css="""
    .main-header {
        text-align: center;
        margin-bottom: 20px;
    }
    .schema-info {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    """
) as demo:
    gr.HTML("""
    <div class="main-header">
        <h1>🚀 NaturalSQL</h1>
        <p><em>Convert natural language queries to SQL statements and run them on your own database!</em></p>
    </div>
    """)
    with gr.Row():
        with gr.Column(scale=2):
            gr.HTML("<h3>📝 Enter Your Query</h3>")
            input_text = gr.Textbox(
                lines=3,
                label="Natural Language Query",
                placeholder="e.g., 'Show all employees in engineering department'",
                show_label=True
            )
            gr.HTML("<h4>🔌 Database Connection</h4>")
            db_type = gr.Radio(DB_TYPES, value=DB_TYPES[0], label="Database Type")
            
            # SQLite
            sqlite_file = gr.File(label="SQLite .db file", visible=False)
            
            # PostgreSQL
            with gr.Row(visible=False) as pg_row:
                pg_host = gr.Textbox(label="Host", placeholder="localhost")
                pg_port = gr.Textbox(label="Port", placeholder="5432")
                pg_user = gr.Textbox(label="Username")
                pg_pass = gr.Textbox(label="Password", type="password")
                pg_db = gr.Textbox(label="Database Name")
            
            # MySQL
            with gr.Row(visible=False) as mysql_row:
                mysql_host = gr.Textbox(label="Host", placeholder="localhost")
                mysql_port = gr.Textbox(label="Port", placeholder="3306")
                mysql_user = gr.Textbox(label="Username")
                mysql_pass = gr.Textbox(label="Password", type="password")
                mysql_db = gr.Textbox(label="Database Name")
            
            # MongoDB
            with gr.Row(visible=False) as mongo_row:
                mongo_conn = gr.Textbox(label="Connection String", placeholder="mongodb://localhost:27017")
                mongo_db = gr.Textbox(label="Database Name")
                mongo_collection = gr.Textbox(label="Collection Name")
            
            def update_db_fields(db_type):
                return {
                    sqlite_file: gr.update(visible=(db_type=="SQLite (upload .db)")),
                    pg_row: gr.update(visible=(db_type=="PostgreSQL")),
                    mysql_row: gr.update(visible=(db_type=="MySQL")),
                    mongo_row: gr.update(visible=(db_type=="MongoDB")),
                }
            
            db_type.change(update_db_fields, inputs=db_type, outputs=[sqlite_file, pg_row, mysql_row, mongo_row])
            
            with gr.Row():
                submit_btn = gr.Button("🔄 Generate & Run SQL", variant="primary")
                clear_btn = gr.Button("🗑️ Clear")
            
            gr.HTML("<h3>💻 Generated SQL</h3>")
            output_sql = gr.Textbox(
                lines=3,
                label="SQL Output",
                show_label=True,
                interactive=False
            )
            gr.HTML("<h3>📊 Query Result</h3>")
            output_result = gr.Textbox(
                lines=10,
                label="Result",
                show_label=True,
                interactive=False
            )
        
        with gr.Column(scale=1):
            gr.HTML("<h3>📚 Example Queries</h3>")
            gr.Examples(
                examples=examples,
                inputs=input_text,
                outputs=output_sql,
                fn=lambda q: (nl_to_sql(q),),
                cache_examples=True
            )
            gr.HTML("<h3>📋 Database Schema</h3>")
            gr.Markdown(schema_info)
    
    submit_btn.click(
        fn=process_query,
        inputs=[input_text, db_type, sqlite_file, pg_host, pg_port, pg_user, pg_pass, pg_db, mysql_host, mysql_port, mysql_user, mysql_pass, mysql_db, mongo_conn, mongo_db, mongo_collection],
        outputs=[output_sql, output_result]
    )
    
    clear_btn.click(
        fn=lambda: ("", ""),
        inputs=[],
        outputs=[output_sql, output_result]
    )
    
    input_text.submit(
        fn=process_query,
        inputs=[input_text, db_type, sqlite_file, pg_host, pg_port, pg_user, pg_pass, pg_db, mysql_host, mysql_port, mysql_user, mysql_pass, mysql_db, mongo_conn, mongo_db, mongo_collection],
        outputs=[output_sql, output_result]
    )

demo.launch() 