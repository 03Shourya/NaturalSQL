# NaturalSQL 🚀

A Natural Language to SQL converter that transforms human-readable queries into SQL statements using a modular pipeline approach.

## Features ✨

### Core Functionality
- **Natural Language Processing**: Converts plain English queries to SQL
- **Multiple SQL Operations**: Supports SELECT, INSERT, UPDATE, DELETE, and AGGREGATE operations
- **Schema Mapping**: Intelligent mapping to database schema
- **Filter Support**: Handles complex WHERE conditions including BETWEEN, >, <, = operators

### Supported Operations
- **SELECT**: "Show all employees", "List employees in engineering department"
- **INSERT**: "Insert a new employee named John with salary 60000"
- **UPDATE**: "Update salary to 75000 for employees in marketing"
- **DELETE**: "Delete employees with salary less than 30000"
- **AGGREGATE**: "What is the average salary?", "Count the number of employees"

### User Interfaces
- **CLI Interface**: Interactive command-line tool with history and colorized output
- **Gradio Web UI**: Beautiful web interface with examples and schema documentation

## Quick Start 🏃‍♂️

### Installation
```bash
pip install -r requirements.txt
```

### CLI Usage
```bash
python cli.py
```

### Web Interface
```bash
python gradio_app.py
```

### Run Tests
```bash
python test_pipeline.py
```

## Architecture 🏗️

The project follows a modular pipeline architecture:

```
Natural Language Query
         ↓
   Parser Agent
         ↓
  Intent Classifier
         ↓
   Schema Mapper
         ↓
  Query Generator
         ↓
   SQL Output
```

### Components

1. **Parser Agent** (`parser_agent/parser.py`)
   - Extracts action, table, columns, and filters
   - Handles various natural language patterns
   - Supports complex WHERE conditions

2. **Intent Classifier** (`intent_classifier/classifier.py`)
   - Classifies query intent (SELECT, INSERT, UPDATE, DELETE, AGGREGATE)
   - Maps parsed actions to SQL operations

3. **Schema Mapper** (`schema_mapper/mapper.py`)
   - Maps natural language terms to database schema
   - Handles column normalization
   - Validates against available tables and columns

4. **Query Generator** (`query_generator/generator.py`)
   - Constructs final SQL statements
   - Handles different SQL operations
   - Manages WHERE clauses and conditions

## Database Schema 📊

```sql
employees: id, name, salary, department_id
departments: id, name
projects: id, title, budget, department_id
```

## Example Queries 📝

### SELECT Operations
```sql
Input: "Show all employees"
Output: SELECT * FROM employees;

Input: "List employees in engineering department"
Output: SELECT * FROM employees WHERE department = 'engineering';

Input: "Show employees who earn between 40000 and 80000"
Output: SELECT * FROM employees WHERE salary BETWEEN 40000 AND 80000;
```

### INSERT Operations
```sql
Input: "Insert a new employee named John with salary 60000"
Output: INSERT INTO employees (name, salary) VALUES ('John', 60000);
```

### UPDATE Operations
```sql
Input: "Update salary to 75000 for employees in marketing"
Output: UPDATE employees SET salary = 75000 WHERE department = 'marketing';
```

### DELETE Operations
```sql
Input: "Delete employees with salary less than 30000"
Output: DELETE FROM employees WHERE salary < 30000;
```

### AGGREGATE Operations
```sql
Input: "What is the average salary in employees?"
Output: SELECT AVG(salary) FROM employees;

Input: "Count the number of employees"
Output: SELECT COUNT(salary) FROM employees;
```

## Recent Enhancements 🆕

### 1. Enhanced CLI Interface
- ✅ Command history with arrow key navigation
- ✅ Colorized output using colorama
- ✅ Help system with examples
- ✅ Clear screen functionality
- ✅ Error handling and graceful exit

### 2. Professional Gradio Web UI
- ✅ Modern, responsive design
- ✅ Interactive examples
- ✅ Schema documentation
- ✅ Real-time SQL generation
- ✅ Error handling and validation

### 3. Comprehensive Test Suite
- ✅ 17 test cases covering all operations
- ✅ DELETE operation support
- ✅ Complex WHERE conditions (BETWEEN)
- ✅ Multiple aggregate functions (COUNT, SUM, AVG)
- ✅ Edge cases and error handling

### 4. Improved Parser
- ✅ Better action detection
- ✅ Enhanced filter extraction
- ✅ Support for "between" conditions
- ✅ Case-insensitive processing

## Usage Examples 🎯

### CLI Interface
```bash
$ python cli.py
🚀 Welcome to NaturalSQL CLI!
Type 'help' for usage instructions, 'exit' to quit.

❯ Show all employees
🔄 Processing...
📝 Generated SQL:
SELECT * FROM employees;

❯ help
NaturalSQL CLI - Natural Language to SQL Converter
...
```

### Web Interface
1. Run `python gradio_app.py`
2. Open browser to `http://localhost:7860`
3. Enter natural language queries
4. View generated SQL instantly
5. Try example queries from the sidebar

## Dependencies 📦

- `colorama>=0.4.6` - CLI colorization
- `gradio>=4.0.0` - Web interface
- Standard Python libraries (re, typing, unittest)

## Project Structure 📁

```
NaturalSQL/
├── agents/                    # Agent implementations
├── intent_classifier/         # Intent classification
├── parser_agent/             # Natural language parsing
├── query_generator/          # SQL generation
├── schema_mapper/            # Schema mapping
├── cli.py                    # Command-line interface
├── gradio_app.py             # Web interface
├── pipeline.py               # Main pipeline
├── test_pipeline.py          # Test suite
└── requirements.txt          # Dependencies
```

## Contributing 🤝

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## Future Enhancements 🚀

- [ ] JOIN operations support
- [ ] GROUP BY and HAVING clauses
- [ ] Subquery support
- [ ] More complex aggregate functions
- [ ] Database connection and execution
- [ ] Query optimization suggestions
- [ ] Multi-language support

## License 📄

This project is open source and available under the MIT License.
