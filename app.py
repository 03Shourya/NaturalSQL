import gradio as gr
from pipeline import nl_to_sql
import sqlite3
import pandas as pd
import os
import base64

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
    title="NaturalSQL - Futuristic NL to SQL",
    theme=gr.themes.Soft(),
    css="""
    body {
        font-family: 'Segoe UI', sans-serif;
        transition: all 0.3s ease;
        position: relative;
        background: linear-gradient(135deg, 
            #87CEEB 0%, 
            #FFB6C1 20%, 
            #FFE4B5 40%, 
            #98FB98 60%, 
            #DDA0DD 80%, 
            #87CEEB 100%) !important;
        min-height: 100vh;
        margin: 0;
        padding: 0;
        background-size: 400% 400% !important;
        animation: gradientShift 15s ease infinite !important;
    }
    
    /* Force background on all theme modes */
    .dark body,
    .light body,
    body.dark,
    body.light {
        background: linear-gradient(135deg, 
            #87CEEB 0%, 
            #FFB6C1 20%, 
            #FFE4B5 40%, 
            #98FB98 60%, 
            #DDA0DD 80%, 
            #87CEEB 100%) !important;
        background-size: 400% 400% !important;
        animation: gradientShift 15s ease infinite !important;
    }
    
    @keyframes gradientShift {
        0% {
            background-position: 0% 50%;
        }
        50% {
            background-position: 100% 50%;
        }
        100% {
            background-position: 0% 50%;
        }
    }
    
    /* Common header styles - same for both themes */
    .main-header h1 {
        font-size: 3em;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 0;
    }
    
    .main-header p {
        text-align: center;
        font-size: 1.2em;
        margin-bottom: 30px;
        margin-top: 0;
    }
    
    .icon-container {
        text-align: center;
        margin-bottom: 20px;
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
    }
    
    .project-icon {
        width: 80px;
        height: 80px;
        filter: drop-shadow(0 0 10px currentColor);
        animation: iconGlow 2s ease-in-out infinite alternate;
    }
    
    @keyframes iconGlow {
        0% {
            filter: drop-shadow(0 0 10px currentColor);
        }
        100% {
            filter: drop-shadow(0 0 20px currentColor);
        }
    }
    
    /* Dark theme styles */
    .dark body {
        color: white !important;
    }
    
    .dark .project-icon {
        color: #00ffff;
    }
    
    .dark .main-header h1 {
        color: #ccf2ff;
        text-shadow: 0px 0px 15px #00fff7;
    }
    
    .dark .main-header p {
        color: #ccc;
    }
    
    .dark .footer-note {
        text-align: center;
        margin-top: 40px;
        color: #ccc;
        font-size: 0.9em;
    }
    
    .dark .gr-textbox textarea {
        background-color: #222;
        color: #0ff;
        border: 1px solid #555;
        border-radius: 12px;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.5), 0 4px 6px rgba(0,255,255,0.2);
    }
    
    .dark label {
        color: #b2fefa !important;
    }
    
    .dark .gr-box, .dark .gr-block, .dark .gr-panel {
        border-radius: 24px !important;
        box-shadow: 0 6px 16px rgba(0, 255, 255, 0.1), inset 0 2px 4px rgba(0,0,0,0.3);
        background-color: #1b1b2f !important;
        padding: 16px;
    }
    
    /* Light theme styles - same layout, different colors */
    .light body {
        color: #1e3a8a !important;
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 50%, #93c5fd 100%) !important;
    }
    
    .light .project-icon {
        color: #3b82f6;
    }
    
    .light .main-header h1 {
        color: #1e40af;
        text-shadow: 0px 0px 15px #3b82f6;
    }
    
    .light .main-header p {
        color: #3b82f6;
    }
    
    .light .footer-note {
        text-align: center;
        margin-top: 40px;
        color: #60a5fa;
        font-size: 0.9em;
    }
    
    /* Enhanced 3D effects for light mode */
    .light .gr-textbox textarea,
    .light .gr-textbox input,
    .light .gr-input textarea,
    .light .gr-input input {
        background-color: #f0f9ff !important;
        color: #1e40af !important;
        border: 2px solid #3b82f6 !important;
        border-radius: 12px !important;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.1), 0 4px 6px rgba(59, 130, 246, 0.2), 0 0 15px rgba(59, 130, 246, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .light .gr-textbox textarea:focus,
    .light .gr-textbox input:focus,
    .light .gr-input textarea:focus,
    .light .gr-input input:focus {
        border-color: #1d4ed8 !important;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.1), 0 4px 6px rgba(59, 130, 246, 0.4), 0 0 20px rgba(59, 130, 246, 0.5) !important;
        outline: none !important;
    }
    
    .light label {
        color: #1e40af !important;
    }
    
    /* Enhanced 3D card effects for light mode */
    .light .gr-box,
    .light .gr-block,
    .light .gr-panel,
    .light .gr-form,
    .light .gr-container {
        border-radius: 24px !important;
        border: 2px solid #3b82f6 !important;
        box-shadow: 0 6px 16px rgba(59, 130, 246, 0.2), inset 0 2px 4px rgba(0,0,0,0.05), 0 0 20px rgba(59, 130, 246, 0.3) !important;
        background-color: rgba(240, 249, 255, 0.95) !important;
        padding: 16px !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
    }
    
    .light .gr-box:hover,
    .light .gr-block:hover,
    .light .gr-panel:hover,
    .light .gr-form:hover,
    .light .gr-container:hover {
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.3), inset 0 2px 4px rgba(0,0,0,0.05), 0 0 25px rgba(59, 130, 246, 0.4) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Force light mode styles with higher specificity */
    body.light .gr-textbox textarea,
    body.light .gr-textbox input,
    body.light .gr-input textarea,
    body.light .gr-input input {
        background-color: #f0f9ff !important;
        color: #1e40af !important;
        border: 2px solid #3b82f6 !important;
        border-radius: 12px !important;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.1), 0 4px 6px rgba(59, 130, 246, 0.2), 0 0 15px rgba(59, 130, 246, 0.3) !important;
    }
    
    body.light .gr-box,
    body.light .gr-block,
    body.light .gr-panel,
    body.light .gr-form,
    body.light .gr-container {
        border-radius: 24px !important;
        border: 2px solid #3b82f6 !important;
        box-shadow: 0 6px 16px rgba(59, 130, 246, 0.2), inset 0 2px 4px rgba(0,0,0,0.05), 0 0 20px rgba(59, 130, 246, 0.3) !important;
        background-color: rgba(240, 249, 255, 0.95) !important;
    }
    
    /* Common styles */
    .gr-button-primary {
        background: linear-gradient(90deg, #00ffff, #a64dff);
        color: black;
        font-weight: bold;
        border: none;
        box-shadow: 0px 0px 10px #00ffff;
    }
    
    #component-0 {
        border-radius: 24px !important;
        box-shadow: 0 6px 20px rgba(0, 255, 255, 0.15);
        overflow: hidden;
    }
    
    #component-0 {
        margin: 40px auto !important;
        max-width: 1000px;
        padding: 32px;
    }
    
    /* Ensure text is always visible */
    .gr-text, .gr-label, .gr-markdown {
        color: inherit !important;
    }
    """
) as demo:
    gr.HTML("""
    <div class="main-header">
        <div class="icon-container">
            <svg class="project-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M4 7C4 5.89543 4.89543 5 6 5H18C19.1046 5 20 5.89543 20 7V17C20 18.1046 19.1046 19 18 19H6C4.89543 19 4 18.1046 4 17V7Z" stroke="currentColor" stroke-width="2"/>
                <path d="M8 9H16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <path d="M8 12H16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <path d="M8 15H12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <circle cx="16" cy="15" r="1" fill="currentColor"/>
                <path d="M12 3L14 5L12 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M12 17L14 19L12 21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
        <h1>NaturalSQL</h1>
        <p>Natural language to SQL converter.<br>Type your question and get instant SQL!</p>
    </div>
    """)

    gr.HTML("""
    <script>
    // Force background to apply
    function applyBackground() {
        const body = document.body;
        body.style.background = 'linear-gradient(135deg, #87CEEB 0%, #FFB6C1 20%, #FFE4B5 40%, #98FB98 60%, #DDA0DD 80%, #87CEEB 100%) !important';
        body.style.backgroundSize = '400% 400% !important';
        body.style.animation = 'gradientShift 15s ease infinite !important';
    }
    
    // Apply on page load
    document.addEventListener('DOMContentLoaded', function() {
        setTimeout(applyBackground, 100);
    });
    
    // Apply when Gradio loads
    if (window.gradio_config) {
        setTimeout(applyBackground, 500);
    }
    
    // Listen for Gradio's dynamic content updates
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                setTimeout(applyBackground, 50);
            }
        });
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
    
    // Also listen for Gradio's specific events
    document.addEventListener('gradio:loaded', applyBackground);
    </script>
    """)

    input_text = gr.Textbox(
        lines=2,
        label="",
        placeholder="e.g., Show all customers from New York"
    )

    db_type = gr.Radio(DB_TYPES, value=DB_TYPES[0], label="")

    sqlite_file = gr.File(label="Choose file", visible=False)

    with gr.Row(visible=False) as pg_row:
        pg_host = gr.Textbox(label="Host")
        pg_port = gr.Textbox(label="Port")
        pg_user = gr.Textbox(label="Username")
        pg_pass = gr.Textbox(label="Password", type="password")
        pg_db = gr.Textbox(label="Database")

    with gr.Row(visible=False) as mysql_row:
        mysql_host = gr.Textbox(label="Host")
        mysql_port = gr.Textbox(label="Port")
        mysql_user = gr.Textbox(label="Username")
        mysql_pass = gr.Textbox(label="Password", type="password")
        mysql_db = gr.Textbox(label="Database")

    with gr.Row(visible=False) as mongo_row:
        mongo_conn = gr.Textbox(label="Connection URI")
        mongo_db = gr.Textbox(label="Database")
        mongo_collection = gr.Textbox(label="Collection")

    def update_db_fields(db_type):
        return {
            sqlite_file: gr.update(visible=(db_type=="SQLite (upload .db)")),
            pg_row: gr.update(visible=(db_type=="PostgreSQL")),
            mysql_row: gr.update(visible=(db_type=="MySQL")),
            mongo_row: gr.update(visible=(db_type=="MongoDB")),
        }

    db_type.change(update_db_fields, inputs=db_type, outputs=[sqlite_file, pg_row, mysql_row, mongo_row])

    with gr.Row():
        submit_btn = gr.Button("Run Query", variant="primary")

    output_sql = gr.Textbox(
        label="Generated SQL:",
        lines=2,
        interactive=False
    )

    output_result = gr.Textbox(
        label="Query Result:",
        lines=8,
        interactive=False
    )

    gr.HTML("<div class='footer-note'>Built with ❤️ by Shourya Sharma</div>")

    submit_btn.click(
        fn=process_query,
        inputs=[input_text, db_type, sqlite_file, pg_host, pg_port, pg_user, pg_pass, pg_db, mysql_host, mysql_port, mysql_user, mysql_pass, mysql_db, mongo_conn, mongo_db, mongo_collection],
        outputs=[output_sql, output_result]
    )

demo.launch()