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

        # Extract table
        table_match = re.search(r"(?:of|from|in)\s+([a-zA-Z_][a-zA-Z0-9_]*)", query)
        if table_match:
            result["table"] = table_match.group(1).strip()

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
            if "earning more than" in query:
                num = re.search(r"earning more than\s+(\d+)", query)
                if num:
                    result["filters"]["salary"] = {"gt": int(num.group(1))}
            if "who earn more than" in query:
                num = re.search(r"who earn more than\s+(\d+)", query)
                if num:
                    result["filters"]["salary"] = {"gt": int(num.group(1))}

            if "in" in query:
                dept_match = re.search(r"in\s+([a-zA-Z]+)", query)
                if dept_match:
                    result["filters"]["department"] = dept_match.group(1).strip()

        # Extract filters for insert queries
        if result["action"] == "insert":
            name_match = re.search(r"named\s+([a-zA-Z]+)", query)
            if name_match:
                result["filters"]["name"] = name_match.group(1)

            salary_match = re.search(r"salary\s+(\d+)", query)
            if salary_match:
                result["filters"]["salary"] = int(salary_match.group(1))

        # Extract filters for update queries
        if result["action"] == "update":
            salary_update = re.search(r"salary\s+to\s+(\d+)", query)
            if salary_update:
                result["filters"]["salary"] = int(salary_update.group(1))

            dept_update = re.search(r"in\s+([a-zA-Z]+)", query)
            if dept_update:
                result["filters"]["department"] = dept_update.group(1)

        result["nouns"] = result["columns"] + list(result["filters"].keys())

        if "function" in result:
            result["nouns"].append(result["function"])

        print("🧠 Final Parsed Output:", result)
        return result

def parse_natural_language(query: str) -> Dict:
    return ParserAgent().parse(query)