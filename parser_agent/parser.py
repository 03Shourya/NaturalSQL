import re
from typing import Dict, List

class ParserAgent:
    def __init__(self):
        pass

    def parse(self, query: str) -> Dict:
        query = query.lower()
        print("📝 Query:", query)

        result = {
            "action": "",
            "table": "",
            "columns": [],
            "filters": {},
            "joins": [],  # New field for JOIN operations
            "group_by": None,  # New field for GROUP BY
            "having": {},  # New field for HAVING conditions
            "subqueries": [],  # New field for subqueries
            "window_functions": [],  # New field for window functions
            "ctes": [],  # New field for CTEs
            "advanced_aggregations": []  # New field for advanced aggregations
        }

        # Detect GROUP BY operations first
        group_by_patterns = [
            r"group\s+employees?\s+by\s+(\w+)",
            r"group\s+by\s+(\w+)",
            r"show\s+(\w+)\s+with\s+(?:average|avg|total|sum|count)\s+(\w+)",
            r"(\w+)\s+with\s+(?:average|avg|total|sum|count)\s+(\w+)",
            r"show\s+(\w+)\s+grouped\s+by\s+(\w+)",
            r"(\w+)\s+grouped\s+by\s+(\w+)",
            r"group\s+(\w+)\s+by\s+(\w+)",
            r"show\s+(\w+)\s+and\s+their\s+(?:average|avg|total|sum|count)\s+(\w+)",
            r"(\w+)\s+and\s+their\s+(?:average|avg|total|sum|count)\s+(\w+)",
            r"group\s+employees?\s+by\s+(\w+)\s+and\s+show\s+count",
            r"show\s+employee\s+count\s+by\s+(\w+)",
            r"count\s+employees?\s+by\s+(\w+)",
            r"(\w+)\s+count\s+by\s+(\w+)",
            r"show\s+(\w+)\s+count\s+by\s+(\w+)"
        ]
        
        for pattern in group_by_patterns:
            match = re.search(pattern, query)
            if match:
                if len(match.groups()) == 2:
                    result["group_by"] = match.group(1)
                    # Extract the aggregation function and column
                    agg_match = re.search(r"(average|avg|total|sum|count)\s+(\w+)", query)
                    if agg_match:
                        agg_func = agg_match.group(1)
                        agg_col = agg_match.group(2)
                        result["columns"] = [f"{agg_func}({agg_col})"]
                        print(f"📊 GROUP BY Detected: {result['group_by']} with {agg_func}({agg_col})")
                elif len(match.groups()) == 1:
                    # Handle patterns like "group employees by department and show count"
                    result["group_by"] = match.group(1)
                    if "count" in query:
                        result["columns"] = ["count(*)"]
                        print(f"📊 GROUP BY Detected: {result['group_by']} with count(*)")
                break

        # Detect HAVING conditions
        having_patterns = [
            r"(?:average|avg|total|sum|count)\s+(\w+)\s*(>|<|=|>=|<=)\s*(\d+)",
            r"(\w+)\s*(>|<|=|>=|<=)\s*(\d+)",
            r"with\s+(?:average|avg|total|sum|count)\s+(\w+)\s*(>|<|=|>=|<=)\s*(\d+)"
        ]
        
        for pattern in having_patterns:
            match = re.search(pattern, query)
            if match and result["group_by"]:  # Only if we have GROUP BY
                col = match.group(1)
                op = match.group(2)
                val = int(match.group(3))
                result["having"] = {
                    "column": col,
                    "operator": op,
                    "value": val
                }
                print(f"🔍 HAVING Detected: {col} {op} {val}")
                break

        # Detect Subqueries
        subquery_patterns = [
            r"who\s+earn\s+more\s+than\s+average",
            r"who\s+earn\s+less\s+than\s+average",
            r"with\s+more\s+than\s+(\d+)\s+employees?",
            r"with\s+less\s+than\s+(\d+)\s+employees?",
            r"in\s+departments?\s+with\s+high\s+budgets?",
            r"in\s+departments?\s+with\s+low\s+budgets?",
            r"who\s+earn\s+more\s+than\s+(\w+)\s+(\w+)",
            r"who\s+earn\s+less\s+than\s+(\w+)\s+(\w+)",
            r"departments?\s+with\s+budget\s+(>|<|=|>=|<=)\s*(\d+)",
            r"employees?\s+in\s+departments?\s+with\s+(\w+)\s+(>|<|=|>=|<=)\s*(\d+)",
            r"departments?\s+with\s+more\s+than\s+(\d+)\s+employees?",
            r"departments?\s+with\s+less\s+than\s+(\d+)\s+employees?"
        ]
        
        for pattern in subquery_patterns:
            match = re.search(pattern, query)
            if match:
                if "average" in pattern:
                    result["subqueries"].append({
                        "type": "comparison",
                        "operator": "more than" if "more" in pattern else "less than",
                        "comparison": "average",
                        "column": "salary"
                    })
                    print(f"🔍 Subquery Detected: salary {result['subqueries'][-1]['operator']} average")
                elif "employees" in pattern and match.groups():
                    count = match.group(1)
                    if count:
                        result["subqueries"].append({
                            "type": "count",
                            "operator": "more than" if "more" in pattern else "less than",
                            "value": int(count),
                            "table": "employees"
                        })
                        print(f"🔍 Subquery Detected: {result['subqueries'][-1]['operator']} {count} employees")
                elif "budget" in pattern:
                    if match.groups():
                        op = match.group(1)
                        val = int(match.group(2))
                        result["subqueries"].append({
                            "type": "budget",
                            "operator": op,
                            "value": val,
                            "column": "budget"
                        })
                        print(f"🔍 Subquery Detected: budget {op} {val}")
                break

        # Detect Window Functions
        window_patterns = [
            r"show\s+employees?\s+with\s+row\s+numbers?",
            r"show\s+row\s+numbers?",
            r"add\s+row\s+numbers?",
            r"list\s+employees?\s+with\s+row\s+numbers?",
            r"with\s+row\s+numbers?",
            r"dense\s+rank\s+by\s+(\w+)",
            r"rank\s+employees?\s+by\s+salary\s+desc",
            r"rank\s+employees?\s+by\s+salary\s+asc",
            r"rank\s+employees?\s+by\s+(\w+)",
            r"rank\s+by\s+(\w+)",
            r"show\s+employees?\s+with\s+rank",
            r"top\s+(\d+)\s+employees?\s+by\s+(\w+)",
            r"bottom\s+(\d+)\s+employees?\s+by\s+(\w+)",
            r"rank\s+departments?\s+by\s+(\w+)",
            r"show\s+ranked\s+(\w+)",
            r"employees?\s+ranked\s+by\s+(\w+)",
            r"with\s+rank"
        ]
        
        for pattern in window_patterns:
            match = re.search(pattern, query)
            if match:
                print(f"🔍 Window pattern matched: {pattern}")
                if r"row\s+numbers?" in pattern:
                    result["window_functions"].append({
                        "type": "row_number",
                        "order_by": "id",
                        "order": "ASC"
                    })
                    print(f"🔍 Window Function Detected: ROW_NUMBER()")
                    break
                elif "rank" in pattern and "dense" not in pattern and match.groups():
                    column = match.group(1)
                    order = "DESC" if "desc" in pattern else "ASC"
                    result["window_functions"].append({
                        "type": "rank",
                        "order_by": column,
                        "order": order
                    })
                    print(f"🔍 Window Function Detected: RANK() by {column} {order}")
                elif r"dense\s+rank" in pattern and match.groups():
                    column = match.group(1)
                    result["window_functions"].append({
                        "type": "dense_rank",
                        "order_by": column,
                        "order": "DESC"
                    })
                    print(f"🔍 Window Function Detected: DENSE_RANK() by {column}")
                    break
                elif "top" in pattern and match.groups():
                    limit = int(match.group(1))
                    column = match.group(2)
                    result["window_functions"].append({
                        "type": "rank",
                        "order_by": column,
                        "order": "DESC",
                        "limit": limit
                    })
                    print(f"🔍 Window Function Detected: TOP {limit} by {column}")
                elif "bottom" in pattern and match.groups():
                    limit = int(match.group(1))
                    column = match.group(2)
                    result["window_functions"].append({
                        "type": "rank",
                        "order_by": column,
                        "order": "ASC",
                        "limit": limit
                    })
                    print(f"🔍 Window Function Detected: BOTTOM {limit} by {column}")
                break

        # Detect CTEs (Common Table Expressions)
        cte_patterns = [
            r"with\s+(\w+)\s+as\s+\((.+?)\)",
            r"using\s+cte",
            r"common\s+table\s+expression",
            r"with\s+recursive",
            r"with\s+(\w+)\s+as",
            r"define\s+(\w+)\s+as",
            r"create\s+(\w+)\s+as",
            r"high\s+salary\s+employees?",
            r"senior\s+employees?",
            r"junior\s+employees?",
            r"department\s+summary",
            r"employee\s+summary"
        ]
        
        for pattern in cte_patterns:
            match = re.search(pattern, query)
            if match:
                print(f"🔍 CTE pattern matched: {pattern}")
                if "with" in pattern and "as" in pattern and match.groups():
                    cte_name = match.group(1)
                    cte_query = match.group(2) if len(match.groups()) > 1 else ""
                    result["ctes"].append({
                        "name": cte_name,
                        "query": cte_query,
                        "type": "with_clause"
                    })
                    print(f"🔍 CTE Detected: {cte_name}")
                elif r"high\s+salary" in pattern:
                    result["ctes"].append({
                        "name": "high_salary_employees",
                        "query": "SELECT * FROM employees WHERE salary > 70000",
                        "type": "high_salary"
                    })
                    print(f"🔍 CTE Detected: high_salary_employees")
                elif "senior" in pattern:
                    result["ctes"].append({
                        "name": "senior_employees",
                        "query": "SELECT * FROM employees WHERE age > 30",
                        "type": "senior"
                    })
                    print(f"🔍 CTE Detected: senior_employees")
                elif "junior" in pattern:
                    result["ctes"].append({
                        "name": "junior_employees",
                        "query": "SELECT * FROM employees WHERE age <= 30",
                        "type": "junior"
                    })
                    print(f"🔍 CTE Detected: junior_employees")
                elif r"department\s+summary" in pattern:
                    result["ctes"].append({
                        "name": "department_summary",
                        "query": "SELECT department_id, COUNT(*) as emp_count, AVG(salary) as avg_salary FROM employees GROUP BY department_id",
                        "type": "department_summary"
                    })
                    print(f"🔍 CTE Detected: department_summary")
                break

        # Detect Advanced Aggregations (ROLLUP, CUBE)
        advanced_agg_patterns = [
            r"with\s+rollup",
            r"with\s+cube",
            r"hierarchical\s+summary",
            r"multi\s+level\s+summary",
            r"department\s+and\s+position\s+summary",
            r"rollup\s+by\s+(\w+)",
            r"cube\s+by\s+(\w+)",
            r"grouping\s+sets",
            r"hierarchical\s+grouping",
            r"multi\s+dimensional\s+analysis",
            r"department\s+position\s+rollup",
            r"salary\s+rollup\s+by\s+department"
        ]
        
        for pattern in advanced_agg_patterns:
            match = re.search(pattern, query)
            if match:
                if "rollup" in pattern:
                    if match.groups():
                        column = match.group(1)
                        result["advanced_aggregations"].append({
                            "type": "rollup",
                            "columns": [column],
                            "operation": "ROLLUP"
                        })
                        print(f"🔍 Advanced Aggregation Detected: ROLLUP by {column}")
                    else:
                        result["advanced_aggregations"].append({
                            "type": "rollup",
                            "columns": ["department_id", "position"],
                            "operation": "ROLLUP"
                        })
                        print(f"🔍 Advanced Aggregation Detected: ROLLUP")
                elif "cube" in pattern:
                    if match.groups():
                        column = match.group(1)
                        result["advanced_aggregations"].append({
                            "type": "cube",
                            "columns": [column],
                            "operation": "CUBE"
                        })
                        print(f"🔍 Advanced Aggregation Detected: CUBE by {column}")
                    else:
                        result["advanced_aggregations"].append({
                            "type": "cube",
                            "columns": ["department_id", "position"],
                            "operation": "CUBE"
                        })
                        print(f"🔍 Advanced Aggregation Detected: CUBE")
                elif "hierarchical" in pattern:
                    result["advanced_aggregations"].append({
                        "type": "rollup",
                        "columns": ["department_id", "position"],
                        "operation": "ROLLUP"
                    })
                    print(f"🔍 Advanced Aggregation Detected: Hierarchical ROLLUP")
                elif "multi" in pattern and "dimensional" in pattern:
                    result["advanced_aggregations"].append({
                        "type": "cube",
                        "columns": ["department_id", "position", "city"],
                        "operation": "CUBE"
                    })
                    print(f"🔍 Advanced Aggregation Detected: Multi-dimensional CUBE")
                break

        # Detect JOIN operations
        join_patterns = [
            r"employees?\s+and\s+their\s+departments?",
            r"employees?\s+with\s+department\s+names?",
            r"employees?\s+and\s+departments?",
            r"show\s+employees?\s+and\s+departments?",
            r"list\s+employees?\s+and\s+departments?",
            r"employees?\s+with\s+their\s+department\s+info",
            r"employees?\s+joined\s+with\s+departments?",
            r"employees?\s+along\s+with\s+departments?",
            r"employees?\s+including\s+department\s+details",
            r"employees?\s+plus\s+department\s+information",
            r"employee\s+names?\s+and\s+department\s+names?",
            r"show\s+employee\s+names?\s+and\s+department\s+names?",
            r"list\s+employee\s+names?\s+and\s+department\s+names?",
            r"names?\s+and\s+departments?",
            r"employee\s+names?\s+with\s+department\s+names?"
        ]
        
        for pattern in join_patterns:
            if re.search(pattern, query):
                result["joins"].append({
                    "type": "INNER",
                    "table": "departments",
                    "on": {
                        "left": "employees.department_id",
                        "right": "departments.id"
                    }
                })
                print("🔗 JOIN Detected: employees INNER JOIN departments")
                break

        # Detect action first
        if "insert" in query or "add" in query:
            result["action"] = "insert"
            print("🔍 Action Detected: INSERT")
        elif "update" in query or "set" in query:
            result["action"] = "update"
            print("🔍 Action Detected: UPDATE")
        elif "delete" in query or "remove" in query:
            result["action"] = "delete"
            print("🔍 Action Detected: DELETE")
        elif result["subqueries"]:  # If subquery is detected, it's a SELECT query
            result["action"] = "select"
            print("🔍 Action Detected: SELECT (with subquery)")
        elif "average" in query or "avg" in query:
            result["action"] = "aggregate"
            result["function"] = "avg"
            print("🔍 Action Detected: AGGREGATE (AVG)")
        elif "total" in query or "sum" in query:
            result["action"] = "aggregate"
            result["function"] = "sum"
            print("🔍 Action Detected: AGGREGATE (SUM)")
        elif "count" in query:
            result["action"] = "aggregate"
            result["function"] = "count"
            print("🔍 Action Detected: AGGREGATE (COUNT)")
        elif result["group_by"]:  # If GROUP BY is detected, it's an aggregate query
            result["action"] = "aggregate"
            print("🔍 Action Detected: AGGREGATE (GROUP BY)")
        else:
            # Default to select for queries that don't match other patterns
            result["action"] = "select"

        # Extract columns (only if not already set by GROUP BY)
        if not result["columns"]:
            col_match = re.search(r"(?:show|list|give|display)\s+(.*?)\s+(?:of|from|in)", query)
            if col_match:
                cols = col_match.group(1)
                result["columns"] = [c.strip() for c in re.split(r",|and", cols)]
            if not result["columns"] and "salaries" in query and "names" in query:
                result["columns"] = ["salary", "name"]
            
            # Handle "List the salaries and names" pattern
            if "list the" in query and ("salaries" in query or "names" in query):
                cols = []
                if "salaries" in query:
                    cols.append("salary")
                if "names" in query:
                    cols.append("name")
                result["columns"] = cols
            
            # Handle "Show employee names, cities, and ages" pattern
            if "employee" in query and ("names" in query or "cities" in query or "ages" in query):
                cols = []
                if "names" in query:
                    cols.append("name")
                if "cities" in query:
                    cols.append("city")
                if "ages" in query:
                    cols.append("age")
                if cols:
                    result["columns"] = cols
            
            # Handle more column patterns
            if "cities" in query:
                result["columns"].append("city")
            if "ages" in query:
                result["columns"].append("age")
            if "positions" in query or "titles" in query:
                result["columns"].append("position")
            if "emails" in query:
                result["columns"].append("email")
            if "join dates" in query or "joined" in query:
                result["columns"].append("join_date")

        # Extract table
        table_match = re.search(r"(?:of|from|in)\s+([a-zA-Z_][a-zA-Z0-9_]*)", query)
        if table_match:
            potential_table = table_match.group(1).strip()
            # Don't treat cities as table names
            cities = ["new", "york", "london", "tokyo", "paris", "berlin", "mumbai", "delhi", "bangalore"]
            if potential_table.lower() not in cities:
                result["table"] = potential_table

        if result["action"] == "insert":
            if not result["table"]:
                result["table"] = "employees"

        if result["action"] == "update":
            if not result["table"]:
                result["table"] = "employees"

        if result["action"] == "aggregate":
            if not result["columns"]:
                result["columns"] = ["salary"]

        if not result["table"]:
            result["table"] = "employees"

        # Extract filters for select queries
        if result["action"] == "select":
            # Salary filters
            if "earning more than" in query:
                num = re.search(r"earning more than\s+(\d+)", query)
                if num:
                    result["filters"]["salary"] = {"gt": int(num.group(1))}
            if "who earn more than" in query:
                num = re.search(r"who earn more than\s+(\d+)", query)
                if num:
                    result["filters"]["salary"] = {"gt": int(num.group(1))}
            if "earn more than" in query:
                num = re.search(r"earn more than\s+(\d+)", query)
                if num:
                    result["filters"]["salary"] = {"gt": int(num.group(1))}
            if "earn between" in query:
                between_match = re.search(r"earn between\s+(\d+)\s+and\s+(\d+)", query)
                if between_match:
                    min_val = int(between_match.group(1))
                    max_val = int(between_match.group(2))
                    result["filters"]["salary"] = {"between": [min_val, max_val]}
            
            # Age filters
            if "older than" in query:
                num = re.search(r"older than\s+(\d+)", query)
                if num:
                    result["filters"]["age"] = {"gt": int(num.group(1))}
            if "younger than" in query:
                num = re.search(r"younger than\s+(\d+)", query)
                if num:
                    result["filters"]["age"] = {"lt": int(num.group(1))}
            if "age between" in query:
                between_match = re.search(r"age between\s+(\d+)\s+and\s+(\d+)", query)
                if between_match:
                    min_val = int(between_match.group(1))
                    max_val = int(between_match.group(2))
                    result["filters"]["age"] = {"between": [min_val, max_val]}
            
            # City filters - check this before department filters
            if "in" in query and any(city in query.lower() for city in ["new york", "london", "tokyo", "paris", "berlin", "mumbai", "delhi", "bangalore"]):
                # Look for city patterns more specifically
                for city in ["new york", "london", "tokyo", "paris", "berlin", "mumbai", "delhi", "bangalore"]:
                    if city in query.lower():
                        result["filters"]["city"] = city
                        break
            
            # Department filters (only if no city was found)
            if "in" in query and "city" not in result["filters"]:
                dept_match = re.search(r"in\s+([a-zA-Z]+)", query)
                if dept_match:
                    dept = dept_match.group(1).strip()
                    if dept.lower() in ["engineering", "marketing", "sales", "hr", "finance", "it", "operations"]:
                        result["filters"]["department"] = dept
            
            # Join date filters
            if "joined after" in query:
                date_match = re.search(r"joined after\s+(\d{4}-\d{2}-\d{2})", query)
                if date_match:
                    result["filters"]["join_date"] = {"gt": date_match.group(1)}
            if "joined before" in query:
                date_match = re.search(r"joined before\s+(\d{4}-\d{2}-\d{2})", query)
                if date_match:
                    result["filters"]["join_date"] = {"lt": date_match.group(1)}
            if "joined in" in query:
                year_match = re.search(r"joined in\s+(\d{4})", query)
                if year_match:
                    year = year_match.group(1)
                    result["filters"]["join_date"] = {"like": f"{year}%"}
            
            # Position filters
            if "position" in query or "title" in query:
                pos_match = re.search(r"(?:position|title)\s+(?:is\s+)?([a-zA-Z\s]+)", query)
                if pos_match:
                    result["filters"]["position"] = pos_match.group(1).strip()

        # Extract filters for insert queries
        if result["action"] == "insert":
            name_match = re.search(r"named\s+([a-zA-Z]+)", query)
            if name_match:
                result["filters"]["name"] = name_match.group(1)

            salary_match = re.search(r"salary\s+(\d+)", query)
            if salary_match:
                result["filters"]["salary"] = int(salary_match.group(1))
            
            # Age
            age_match = re.search(r"age\s+(\d+)", query)
            if age_match:
                result["filters"]["age"] = int(age_match.group(1))
            
            # City
            city_match = re.search(r"(?:from|in)\s+([a-zA-Z\s]+)", query)
            if city_match:
                city = city_match.group(1).strip()
                if city.lower() in ["new york", "london", "tokyo", "paris", "berlin", "mumbai", "delhi", "bangalore"]:
                    result["filters"]["city"] = city
            
            # Position
            pos_match = re.search(r"(?:as|position|title)\s+([a-zA-Z\s]+)", query)
            if pos_match:
                result["filters"]["position"] = pos_match.group(1).strip()
            
            # Email
            email_match = re.search(r"email\s+([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})", query)
            if email_match:
                result["filters"]["email"] = email_match.group(1)

        # Extract filters for update queries
        if result["action"] == "update":
            salary_update = re.search(r"salary\s+to\s+(\d+)", query)
            if salary_update:
                result["filters"]["salary"] = int(salary_update.group(1))
            
            age_update = re.search(r"age\s+to\s+(\d+)", query)
            if age_update:
                result["filters"]["age"] = int(age_update.group(1))

            dept_update = re.search(r"in\s+([a-zA-Z]+)", query)
            if dept_update:
                result["filters"]["department"] = dept_update.group(1).strip()

        # Extract filters for delete queries
        if result["action"] == "delete":
            # Salary filters
            if "salary less than" in query:
                num = re.search(r"salary less than\s+(\d+)", query)
                if num:
                    result["filters"]["salary"] = {"lt": int(num.group(1))}
            elif "salary greater than" in query:
                num = re.search(r"salary greater than\s+(\d+)", query)
                if num:
                    result["filters"]["salary"] = {"gt": int(num.group(1))}
            
            # Age filters
            if "younger than" in query:
                num = re.search(r"younger than\s+(\d+)", query)
                if num:
                    result["filters"]["age"] = {"lt": int(num.group(1))}
            elif "older than" in query:
                num = re.search(r"older than\s+(\d+)", query)
                if num:
                    result["filters"]["age"] = {"gt": int(num.group(1))}
            
            # City filters
            if "in" in query and any(city in query.lower() for city in ["new york", "london", "tokyo", "paris", "berlin", "mumbai", "delhi", "bangalore"]):
                city_match = re.search(r"in\s+([a-zA-Z\s]+)", query)
                if city_match:
                    city = city_match.group(1).strip()
                    if city.lower() in ["new york", "london", "tokyo", "paris", "berlin", "mumbai", "delhi", "bangalore"]:
                        result["filters"]["city"] = city
            
            # Department filters
            if "in" in query and not any(city in query.lower() for city in ["new york", "london", "tokyo", "paris", "berlin", "mumbai", "delhi", "bangalore"]):
                dept_match = re.search(r"in\s+([a-zA-Z]+)", query)
                if dept_match:
                    dept = dept_match.group(1).strip()
                    if dept.lower() in ["engineering", "marketing", "sales", "hr", "finance", "it", "operations"]:
                        result["filters"]["department"] = dept

        result["nouns"] = result["columns"] + list(result["filters"].keys())

        if "function" in result:
            result["nouns"].append(result["function"])

        print("🧠 Final Parsed Output:", result)
        return result

def parse_natural_language(query: str) -> Dict:
    return ParserAgent().parse(query)