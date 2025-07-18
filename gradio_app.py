import gradio as gr
from pipeline import nl_to_sql

def generate_sql(query):
    """Generate SQL from natural language query."""
    if not query.strip():
        return "Please enter a query."
    try:
        return nl_to_sql(query)
    except Exception as e:
        return f"Error: {str(e)}"

# Example queries
examples = [
    ["Show all employees"],
    ["List employees in engineering department"],
    ["What is the average salary in employees?"],
    ["Insert a new employee named John with salary 60000"],
    ["Update salary to 75000 for employees in marketing"],
    ["List the salaries and names of employees in engineering who earn more than 50000"],
    ["Show employees older than 30"],
    ["Show employees in New York"],
    ["Show employees who joined after 2020-01-01"],
    ["Show employees with position Software Engineer"],
    ["Insert a new employee named Alice with salary 55000, age 28, from London"],
    ["Delete employees younger than 25"],
    ["Show employees in New York who are older than 25 and earn more than 50000"]
]

# Schema information
schema_info = """
## Database Schema

### Tables:
- **employees**: id, name, salary, department_id, city, age, join_date, position, email
- **departments**: id, name, location, budget  
- **projects**: id, title, budget, department_id, start_date, end_date, status

### Supported Operations:
- **SELECT**: Show, list, display, get
- **INSERT**: Insert, add, create
- **UPDATE**: Update, modify, change
- **DELETE**: Delete, remove
- **AGGREGATE**: Average, sum, count, total

### New Natural Language Patterns:

#### Age Filters:
- "Show employees older than 30"
- "Show employees younger than 25"
- "Show employees with age between 25 and 40"

#### City Filters:
- "Show employees in New York"
- "Show employees in London"
- "Show employees in Tokyo"

#### Join Date Filters:
- "Show employees who joined after 2020-01-01"
- "Show employees who joined before 2019-12-31"
- "Show employees who joined in 2021"

#### Position Filters:
- "Show employees with position Software Engineer"
- "Show employees with title Manager"

#### Complex Combinations:
- "Show employees in New York who are older than 25 and earn more than 50000"
- "Insert a new employee named Alice with salary 55000, age 28, from London, as Software Engineer"

### Examples:
- "Show all employees"
- "List employees in engineering department"
- "What is the average salary?"
- "Insert a new employee named John with salary 60000"
- "Update salary to 75000 for employees in marketing"
- "Show employees older than 30"
- "Show employees in New York"
- "Show employees who joined after 2020-01-01"
"""

# Create the interface
with gr.Blocks(
    title="NaturalSQL - Natural Language to SQL Converter",
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
        <p><em>Convert natural language queries to SQL statements</em></p>
    </div>
    """)
    
    with gr.Row():
        with gr.Column(scale=2):
            # Input section
            gr.HTML("<h3>📝 Enter Your Query</h3>")
            input_text = gr.Textbox(
                lines=3,
                label="Natural Language Query",
                placeholder="e.g., 'Show all employees in engineering department'",
                show_label=True
            )
            
            with gr.Row():
                submit_btn = gr.Button("🔄 Generate SQL", variant="primary")
                clear_btn = gr.Button("🗑️ Clear")
            
            # Output section
            gr.HTML("<h3>💻 Generated SQL</h3>")
            output_text = gr.Textbox(
                lines=5,
                label="SQL Output",
                show_label=True,
                interactive=False
            )
        
        with gr.Column(scale=1):
            # Examples section
            gr.HTML("<h3>📚 Example Queries</h3>")
            gr.Examples(
                examples=examples,
                inputs=input_text,
                outputs=output_text,
                fn=generate_sql,
                cache_examples=True
            )
    
    # Schema information
    gr.HTML(f"""
    <div class="schema-info">
        {schema_info}
    </div>
    """)
    
    # Event handlers
    submit_btn.click(
        fn=generate_sql,
        inputs=input_text,
        outputs=output_text
    )
    
    clear_btn.click(
        fn=lambda: ("", ""),
        inputs=[],
        outputs=[input_text, output_text]
    )
    
    # Enter key support
    input_text.submit(
        fn=generate_sql,
        inputs=input_text,
        outputs=output_text
    )

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    ) 