import re
from typing import Dict, List

class ParserAgent:
    def __init__(self):
        pass

    def parse(self, query: str) -> Dict:
        query = query.lower()

        result = {
            "action": "select",
            "table": "",
            "columns": [],
            "filters": {}
        }

        # Extract columns
        col_match = re.search(r"(?:show|list|give|display)\s+(.*?)\s+(?:of|from|in)", query)
        if col_match:
            cols = col_match.group(1)
            result["columns"] = [c.strip() for c in re.split(r",|and", cols)]
        if not result["columns"] and "salaries" in query and "names" in query:
            result["columns"] = ["salary", "name"]

        # Extract table
        table_match = re.search(r"(?:of|from)\s+([a-zA-Z_][a-zA-Z0-9_]*)", query)
        if table_match:
            result["table"] = table_match.group(1).strip()

        # Extract filters
        if "earning more than" in query:
            num = re.search(r"earning more than\s+(\d+)", query)
            if num:
                result["filters"]["salary"] = {"gt": int(num.group(1))}

        if "in" in query:
            dept_match = re.search(r"in\s+([a-zA-Z]+)", query)
            if dept_match:
                result["filters"]["department"] = dept_match.group(1).strip()

        result["nouns"] = result["columns"] + list(result["filters"].keys())

        return result

def parse_natural_language(query: str) -> Dict:
    return ParserAgent().parse(query)