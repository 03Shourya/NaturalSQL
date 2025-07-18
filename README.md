# 🚀 NaturalSQL - Natural Language to SQL Converter

Convert natural language queries into SQL statements with ease! This AI-powered tool understands complex queries and generates accurate SQL code.

## 🌟 Features

- **Natural Language Processing**: Convert plain English to SQL
- **Multiple SQL Operations**: SELECT, INSERT, UPDATE, DELETE, AGGREGATE
- **Complex Filters**: Age, city, join date, position, and salary filters
- **Smart Schema Mapping**: Automatic field detection and normalization
- **Beautiful Web Interface**: User-friendly Gradio interface
- **Example Queries**: Pre-built examples to get you started

## 🗄️ Database Schema

### Tables:
- **employees**: id, name, salary, department_id, city, age, join_date, position, email
- **departments**: id, name, location, budget  
- **projects**: id, title, budget, department_id, start_date, end_date, status

## 📝 Supported Query Types

### Basic Operations:
- **SELECT**: "Show all employees", "List employees in engineering"
- **INSERT**: "Insert a new employee named John with salary 60000"
- **UPDATE**: "Update salary to 75000 for employees in marketing"
- **DELETE**: "Delete employees younger than 25"

### Advanced Filters:
- **Age**: "Show employees older than 30"
- **City**: "Show employees in New York"
- **Join Date**: "Show employees who joined after 2020-01-01"
- **Position**: "Show employees with position Software Engineer"
- **Complex**: "Show employees in New York who are older than 25 and earn more than 50000"

### Aggregates:
- **Average**: "What is the average salary?"
- **Count**: "How many employees are there?"
- **Sum**: "What is the total salary budget?"

## 🎯 Example Queries

Try these examples to get started:

1. `Show all employees`
2. `List employees in engineering department`
3. `What is the average salary in employees?`
4. `Insert a new employee named John with salary 60000`
5. `Update salary to 75000 for employees in marketing`
6. `Show employees older than 30`
7. `Show employees in New York`
8. `Show employees who joined after 2020-01-01`
9. `Show employees with position Software Engineer`
10. `Show employees in New York who are older than 25 and earn more than 50000`

## 🛠️ How to Use

1. **Enter your query** in natural language
2. **Click "Generate SQL"** or press Enter
3. **Copy the generated SQL** for your database

## 🔧 Technical Details

This application uses:
- **Gradio**: Web interface framework
- **Custom NLP Pipeline**: Natural language processing
- **Schema Mapping**: Intelligent field detection
- **Query Generation**: SQL statement creation

## 🚀 Deployment

This app is deployed on Hugging Face Spaces for:
- ✅ **Public Access**: Available to everyone
- ✅ **Permanent Hosting**: Always online
- ✅ **GPU Availability**: Fast processing
- ✅ **Free Hosting**: No cost to users

## 📞 Support

If you encounter any issues or have questions:
1. Check the schema information in the sidebar
2. Try the example queries
3. Make sure your query follows the supported patterns

## 🎉 Enjoy!

Start converting your natural language queries to SQL today! 🎯
