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
            "filters": {}
        }

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
        else:
            # Default to select for queries that don't match other patterns
            result["action"] = "select"

        # Extract columns
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